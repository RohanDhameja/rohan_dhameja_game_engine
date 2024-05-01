# This file was created by: Rohan Dhameja

# Import modules
import pygame as pg
from pygame.sprite import Sprite
from settings import *
from os import path


vec = pg.math.Vector2

SPRITESHEET = "stoopid.png"

game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, 'images')

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg.transform.scale(image, (width * 1, height * 1))
        return image


# Create a player class
class Player(Sprite):
    def __init__(self, game, x, y):
        # initialize all variables for self
        self.groups = game.all_sprites
        Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.player_img
        self.spritesheet = Spritesheet(path.join(img_folder, SPRITESHEET))
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 300
        self.cooling = False
        self.status = ""
        self.next_map = False
        self.current_frame = 0
        self.last_update = 0
        self.material = True
        self.jumping = False
        self.walking = False

    # def move(self, dx = 0, dy = 0):
    #     self.x += dx
    #     self.y += dy
    
    # take keyboard input from user
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

    # function with commands for when player collides with another sprite
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "SpeedPowerUp":
                self.game.countdown.cd = 10
                self.cooling = True
                # print(effect)
                # print(self.cooling)
                self.status = "Flash"
            if str(hits[0].__class__.__name__) == "Coins":
                self.game.coinCount += 1
            if str(hits[0].__class__.__name__) == "Enemies":
                if self.status != "Invincible":
                    self.game.hitpoints -= 1
            if str(hits[0].__class__.__name__) == "Stairs":
                self.next_map = True
            if str(hits[0].__class__.__name__) == "Shield":
                self.game.countdown.cd = 5
                self.cooling = True
                self.status = "Invincible"
            if str(hits[0].__class__.__name__) == "Enemies2":
                if self.status != "Invincible":
                    self.game.hitpoints -= 1

    # makes it so that, when player collides with walls, the player does not move into the wall
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    def load_images(self):
        self.standing_frames = [self.spritesheet.get_image(0,0, 32, 32), 
                                self.spritesheet.get_image(32,0, 32, 32),

                                ]
        self.walking_frames = [
                                self.spritesheet.get_image(64,0, 32, 32),
                                self.spritesheet.get_image(96,0, 32, 32),
                                ]
    
    def animate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 350:
            self.last_update = now
            self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
            bottom = self.rect.bottom
            if not self.walking:
                self.image = self.standing_frames[self.current_frame]
            else:
                self.image = self.walking_frames[self.current_frame]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom

    def update(self):
        self.animate()
        # self.rect.x = self.x * TILESIZE
        # self.rect.y = self.y * TILESIZE
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add x collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add y collision later
        self.collide_with_walls('y')

        # adds a cooldown to the speed powerup
        if self.game.countdown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.status = ""
            self.speed = 300
        if self.status == "Flash":
            self.speed = 600
        
        # choose to kill or not kill the sprite when colliding with other groups
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.enemies, False)
        self.collide_with_group(self.game.stairs, False)
        self.collide_with_group(self.game.shield, True)
        self.collide_with_group(self.game.enemies2, False)
        self.rect.width = self.rect.width
        self.rect.height = self.rect.height

        # end game if player has 0 hitpoints
        if (self.game.hitpoints == 0):
            pg.quit()

# Create a wall
class Wall(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Create a speed powerup with an image
class SpeedPowerUp(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.speed_powerup_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Create a coin sprite with an image
class Coins(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.coin_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Create an enemy with an image
class Enemies(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 100
    
    # Make the enemies unable to pass through walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    # Update the enemy
    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        # Make the enemy follow the player
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

# Create a stairs sprite - to go to the next level
class Stairs(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.stairs
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Create a shield powerup
class Shield(Sprite):
    def __init__(self, game, x, y):
        # add powerup groups later....
        self.groups = game.all_sprites, game.shield
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# Enemies that move around in the same area
class Enemies2(Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.enemies2
        Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.enemy_img
        self.rect = self.image.get_rect()
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.vx, self.vy = ENEMY_SPEED, ENEMY_SPEED
        self.speed = 1
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071


    # wall collisions; horizontally based
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right 
                self.vx = -self.vx
                self.rect.x = self.x
        
    # wall collisions; vertically based
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = -self.vy
                self.rect.y = self.y

    def update(self):
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

# Shop for player to buy speed boost (used ChatGPT)
class Shop(Sprite):
    def __init__(self, game):
        self.game = game 
        self.visible = False
        self.width = 260
        self.height = 160
        self.color = YELLOW
        self.x = 50
        self.y = 550
        self.shop_surface = pg.Surface((self.width, self.height), flags=pg.SRCALPHA)
        self.shop_surface.fill(YELLOW)

    # create a box with a shop on the screen
    def draw_shop(self, screen):
        if self.visible:
            self.shop_surface.fill(YELLOW)
            pg.draw.rect(self.shop_surface, self.color, (self.x, self.y, TILESIZE * 8, TILESIZE * 5))
            screen.blit(self.shop_surface, (self.x, self.y))

    # toggles if the shop is on the screen or not
    def toggle_visibility(self):
        self.visible = not self.visible
    
# allows player to click (used ChatGPT)
class Button:
    #Initialize button
    def __init__(self, game, text, position, size, color, color2, action = None, clickable = True):
        self.game = game
        self.text = text
        self.position = position
        self.size = size
        self.font = pg.font.Font(None, 32)
        self.color = color
        self.color2 = color2
        self.action = action
        self.hovered = False
        self.clickable = clickable

    # draw the object
    def draw(self, screen):
        clickable = self.is_clickable()
        button_rect = pg.Rect(self.position, self.size)

        # Change button color
        if self.hovered and self.clickable:
            color = self.color2
        else:
            color = self.color

        pg.draw.rect(screen, color, button_rect)
        text_surface = self.font.render(self.text, True, pg.Color('white'))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)

    # check for click
    def handle_event(self, event):
        # only changes color or is clicked if conditions are met
        if self.clickable:
            if event.type == pg.MOUSEMOTION:
                # Check if mouse is hovering over the button
                self.hovered = self.is_hovered(event.pos)
            elif event.type == pg.MOUSEBUTTONDOWN:
                if self.hovered and self.action:
                    # Execute button action if clicked
                    self.action()

    # Function to check mouse position
    def is_hovered(self, mouse_pos):
        button_rect = pg.Rect(self.position, self.size)
        return button_rect.collidepoint(mouse_pos)

    # Boolean that tells if the player can click the button
    def is_clickable(self):
        if self.game.coinCount >= 6:
            self.clickable = True
        else:
            self.clickable = False  