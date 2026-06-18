import pygame
import math
import numpy as np
import mmap
import os
import sys

from gpiozero import Button
from scripts.tile import Tile
import g1.Game1 as g1

class Home:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("lemonade")
        self.screen = pygame.display.set_mode((480, 320))
        self.display = pygame.Surface((240, 160))

        fb = open("/dev/fb0", "r+b")
        self.fbmem = mmap.mmap(fb.fileno(), self.screen.get_width() * self.screen.get_height() * 4)

        self.button1 = Button(12)
        self.button2 = Button(16)
        self.button3 = Button(20)
        self.button4 = Button(21)
        self.button5 = Button(19)
        self.button6 = Button(26)

        self.clock = pygame.time.Clock()

        self.game_button_w = 100
        self.game_button_h = 50

        self.banner_thick = 20

        self.banner = pygame.Surface((self.display.get_width(), self.banner_thick))

        self.gapx = (self.display.get_width() - self.game_button_w * 2) / 3
        self.gapy = (self.display.get_height() - self.banner_thick - self.game_button_h * 2) / 3

        self.page_1 = {
                Tile((self.game_button_w, self.game_button_h), (self.gapx, self.gapy + self.banner_thick), 0),
                Tile((self.game_button_w, self.game_button_h), (self.game_button_w +  2 * self.gapx, self.gapy + self.banner_thick), 1),
                Tile((self.game_button_w, self.game_button_h), (self.gapx, self.game_button_h + 2 * self.gapy + self.banner_thick), 2),
                Tile((self.game_button_w, self.game_button_h), (self.game_button_w + 2 * self.gapx, self.game_button_h + 2 * self.gapy + self.banner_thick), 3)
        }

        self.highlighted = 0

    def run(self):
        while True:

            self.display.fill((250, 250, 250))
            self.banner.fill((240, 240, 0))

            for button in self.page_1:
                button.highlight(self.highlighted)
                button.render(self.display)


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        g1.Game1().run()
                    if event.key == pygame.K_RIGHT:
                        if self.highlighted == 0 or self.highlighted == 2:
                            self.highlighted += 1
                    if event.key == pygame.K_LEFT:
                        if self.highlighted == 1 or self.highlighted == 3:
                            self.highlighted -= 1
                    if event.key == pygame.K_DOWN:
                        if self.highlighted == 0 or self.highlighted == 1:
                            self.highlighted += 2
                    if event.key == pygame.K_UP:
                        if self.highlighted == 2 or self.highlighted == 3:
                            self.highlighted -= 2

            self.display.fill((35, 35, 35) special_flags=pygame.BLEND_RGB_ADD)
            self.display.blit(self.banner, (0, 0))
            bgra_frame = bytes(pygame.transform.scale(self.display, self.screen.get_size()).get_buffer())

            self.fbmem.seek(0)

            self.fbmem.write(bgra_frame)

            self.clock.tick(60)

Home().run()
