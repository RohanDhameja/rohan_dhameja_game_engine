#loop through a list

import pygame as pg
from settings import *

clock = pg.time.Clock()

frames = ["frame1", "frame2", "frame3", "frame4"]

# print(len(frames))

frames_length = len(frames)

current_frame = 0

then = 0

# print(frames[frames_length])

while True:
    clock.tick(FPS)
    now = pg.time.get_ticks()
    if now - then > 1000:
        print("now")
        then = now
        current_frame += 1
        print(frames[current_frame%frames_length])
