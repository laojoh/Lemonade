import pygame
import sys
import random
import mmap

from gpiozero import Button
from g4.scripts.board import Board
from g4.scripts.piece import Piece

class Game4:
    def __init__(self):
        pygame.display.set_caption("lemonade")
        self.screen = pygame.display.set_mode((480, 320))
        self.display = pygame.Surface((240, 160))
        
        fb = open("/dev/fb0", "r+b")
        self.fbmem = mmap.mmap(fb.fileno(), self.screen.get_width() * self.screen.get_height() * 4)

        self.button1 = Button(12, bounce_time = 0.1)
        self.button2 = Button(16, bounce_time = 0.1)
        self.button3 = Button(20, bounce_time = 0.1)
        self.button4 = Button(21)
        self.button5 = Button(19)
        self.button6 = Button(26)

        self.clock = pygame.time.Clock()
        self.tile_size = 8

        self.board = Board(10, 16, self.tile_size)

        self.piece = Piece(random.choice(["I", "T", "J", "L", "S", "Z", "O"]), random.choice([4, 5]), 0, 0, self.tile_size)
        self.timer = 0

    def run(self):
        while True:
            self.timer += 1
            self.display.fill((255, 255, 255))

            self.board.render(self.display)

            self.piece.render(self.display, self.board)
            test = Piece(self.piece.type, self.piece.x, self.piece.y + 1, self.piece.rotation, self.tile_size)
            if self.board.valid(test):
                if self.timer == 20:
                    self.timer = 0
                    self.piece.y += 1
            else:
                self.board.lock(self.piece)
                lines = self.board.clearLines()
                self.piece = Piece(random.choice(["I", "T", "J", "L", "S", "Z", "O"]), random.choice([4, 5]), 0, 0, self.tile_size)
                self.timer = 0

            if self.button1.is_pressed and self.timer % 5 == 0:
                self.piece.rotate(self.board)
            if self.button2.is_pressed and self.timer % 5 == 0:
                self.piece.move(self.board, 1)
            if self.button3.is_pressed and self.timer % 5 == 0:
                self.piece.move(self.board, -1)
            if self.button4.is_pressed and self.timer % 3 == 0:
                test = Piece(self.piece.type, self.piece.x, self.piece.y + 1, self.piece.rotation, self.tile_size)
                if self.board.valid(test):
                    self.piece.y += 1

            self.display.fill((35, 35, 35), special_flags=pygame.BLEND_RGB_ADD)
            bgra_frame = bytes(pygame.transform.scale(self.display, self.screen.get_size()).get_buffer())

            self.fbmem.seek(0)

            self.fbmem.write(bgra_frame)

            self.clock.tick(60)
