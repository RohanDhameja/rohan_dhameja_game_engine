class Character:
    def __init__(self, name, speed, health, spritesheet):
        self.name = name
        self.speed = speed
        self.health = health
        self.spritesheet = spritesheet

# Define different characters with a dictionary
CHARACTER_DATA = {
    "Speedster": Character(name="Speedster", speed=600, health=3, spritesheet="speedster.png"),
    "Tank": Character(name="Tank", speed=300, health=5, spritesheet="tank.png"),
    "Balanced": Character(name="Balanced", speed=400, health=4, spritesheet="balanced.png"),
}
