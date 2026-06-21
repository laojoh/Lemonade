import pygame
import sys
import random

from scripts.board import Board
from scripts.piece import Piece

class Game4:
    def __init__(self):
        pygame.display.set_caption("lemonade")
        self.screen = pygame.display.set_mode((1200, 800))
        self.display = pygame.Surface((240, 160))

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

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.piece.move(self.board, -1)
                    if event.key == pygame.K_RIGHT:
                        self.piece.move(self.board, 1)
                    if event.key == pygame.K_UP:
                        self.piece.rotate(self.board)
                    if event.key == pygame.K_q:
                        return

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        pass

            keys = pygame.key.get_pressed()
            if keys[pygame.K_DOWN] and self.timer % 3 == 0:
                test = Piece(self.piece.type, self.piece.x, self.piece.y + 1, self.piece.rotation, self.tile_size)
                if self.board.valid(test):
                    self.piece.y += 1

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))
            pygame.display.update()
            self.clock.tick(60)
