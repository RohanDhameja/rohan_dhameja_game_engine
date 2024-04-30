# This file was created by: Rohan Dhameja

# import necessary modules
import pygame as pg
import sys
from settings import *
from sprites import *
from utils import *
from random import randint
from os import path
from time import sleep

# Create a game class to make a video game
class Game:
    #Defining the game class
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.coinCount = 0
        self.gamestage = "start"
        self.shop_open = False
        self.shop = Shop(self)
    
    #load save game data etc...
    def load_data(self):
        self.level = 1

        game_folder = path.dirname(__file__)
        self.img_folder = path.join(game_folder, 'images')

        # Add the images files
        self.speed_powerup_img = pg.image.load(path.join(self.img_folder, 'speed_powerup.jpg')).convert_alpha()
        self.enemy_img = pg.image.load(path.join(self.img_folder, 'enemy.jpg')).convert_alpha()
        self.player_img = pg.image.load(path.join(self.img_folder, 'hero.jpg')).convert_alpha()
        self.coin_img = pg.image.load(path.join(self.img_folder, 'coin.jpg')).convert_alpha()


        self.map_data = []
        with open(path.join(game_folder, 'map' + str(self.level) + '.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
                # print(self.map1_data)
                # print(enumerate(self.map1_data))
    
    # Changing the map level
    def change_levels(self):
        game_folder = path.dirname(__file__)

        # Destroy the sprites from the past map
        if self.player.next_map == True:
            self.level += 1
            self.player.next_map = False
            for i in self.all_sprites:
                i.kill()

            # load the new map, and create all the sprites
            self.map_data = []
            with open(path.join(game_folder, 'map' + str(self.level) + '.txt'), 'rt') as f:
                for line in f:
                    self.map_data.append(line)
            for row, tiles in enumerate(self.map_data):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        Wall(self, col, row)
                    if tile == 'P':
                        self.player = Player(self, col, row)
                    if tile == 'U':
                        SpeedPowerUp(self, col, row)
                    if tile == 'C':
                        Coins(self, col, row)
                    if tile == 'E':
                        Enemies(self, col, row)
                    if tile == 'S':
                        Stairs(self, col, row)
                    if tile == 'B':
                        Shield(self, col, row)
                    if tile == 'R':
                        Enemies2(self, col, row)

    def new(self):
        self.countdown = Timer(self)
        # init all variables, setup groups, instantiate classes
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.stairs = pg.sprite.Group()
        self.shield = pg.sprite.Group()
        self.enemies2 = pg.sprite.Group()
        self.shop = Shop(g)
        self.button = Button(self, "BUY", (self.shop.x + 55, self.shop.y + 100), (150, 50), GREEN, RED, action=self.button_action, clickable = True)
        #self.player = Player(self, 10, 10)
        #for x in range(10, 20):
        #    Wall(self, x, 5)
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'U':
                    SpeedPowerUp(self, col, row)
                if tile == 'C':
                    Coins(self, col, row)
                if tile == 'E':
                    Enemies(self, col, row)
                if tile == 'S':
                    Stairs(self, col, row)
                if tile == 'B':
                    Shield(self, col, row)
                if tile == 'R':
                        Enemies2(self, col, row)

    def run(self):
        self.playing = True
        while self.playing: 
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if self.gamestage == "start":
                self.show_start_screen()
            if self.gamestage == "playing":
                self.update()
                self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()
        self.countdown.ticking()
        self.change_levels()

    # Create a grid with dimensions WIDTH and HEIGHT
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    # draw text on self
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('stencil')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    # call the draw_text function with parameters
    def draw(self):
        self.screen.fill(BGCOLOR)
        # self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_text(self.screen, "Coins: " + str(self.coinCount), 42, BLACK, 1, 1)
        self.draw_text(self.screen, "Hitpoints: " + str(self.player.hitpoints), 42, BLACK, 8, 1)
        if self.player.status == "Invincible":
            self.draw_text(self.screen, "You are invincible for 5 seconds", 42, BLACK, 5, 9)
        if self.player.status == "Flash":
            self.draw_text(self.screen, "You are speedy for 10 seconds", 42, BLACK, 5, 9)

        if self.shop.visible:
                self.shop.draw_shop(self.screen)
                self.button.draw(self.screen)
                self.draw_text(self.screen, "Speed - 5", 60, BLACK, (self.shop.x + 50) / TILESIZE , (self.shop.y + 20) / TILESIZE)

        # shop only opens if player has money
        if self.coinCount > 0:
            self.draw_text(self.screen, "Press r to open shop", 30, BLACK, 20, 1)
        pg.display.flip()
    
    def button_action(self):
        if self.coinCount >= 5:
            self.coinCount -= 5
        self.player.speed += 100
    
    # Take input from keyboard and move player
    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if (event.key == pg.K_LEFT):
            #         self.player.move(dx = -1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx = 1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy = 1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy = -1)
            if event.type == pg.KEYDOWN:
                if self.coinCount > 0:             
                    if event.key == pg.K_r:
                        self.shop.toggle_visibility()
            self.button.handle_event(event)
    

    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        keys = pg.key.get_pressed()
        self.draw_text(self.screen, "Escape the creatures and collect coins!", 42, BLACK, 2, 8)
        self.draw_text(self.screen, "Open doors to new levels!", 42, BLACK, 6, 10)
        self.draw_text(self.screen, "Find powerups for extra speed and shields!", 42, BLACK, 1, 12)
        self.draw_text(self.screen, "Press the spacebar to begin!", 42, BLACK, 6, 20)

        if keys[pg.K_SPACE]:
            self.gamestage = "playing"
        pg.display.flip()
        self.run()

    def show_go_screen(self):
        pass

#Making and running the video game
g = Game()
# g.show_start_screen()
while (True):
    g.new()
    g.run()
    # g.show_go_screen()

