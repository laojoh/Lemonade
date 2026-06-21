import pygame

SHAPES = {
    "I0" : [(0, -1), (0, 0), (0, 1), (0, 2)],
    "I1" : [(-1, 0), (0, 0), (1, 0), (2, 0)],
    "I2" : [(0, 1), (0, 0), (0, -1), (0, -2)],
    "I3" : [(1, 0), (0, 0), (-1, 0), (-2, 0)],
    "T0" : [(-1, 0), (0, 0), (1, 0), (0, 1)],
    "T1" : [(0, 1), (0, 0), (0, -1), (1, 0)],
    "T2" : [(1, 0), (0, 0), (-1, 0), (0, -1)],
    "T3" : [(0, -1), (0, 0), (0, 1), (-1, 0)],
    "J0" : [(0, -1), (0, 0), (0, 1), (-1, 1)],
    "J1" : [(-1, 0), (0, 0), (1, 0), (1, 1)],
    "J2" : [(0, -1), (0, 0), (0, 1), (1, -1)],
    "J3" : [(1, 0), (0, 0), (-1, 0), (-1. -1)],
    "L0" : [(0, -1), (0, 0), (0, 1), (1, 1)],
    "L1" : [(-1, 0), (0, 0), (1, 0), (1, -1)],
    "L2" : [(-1, -1), (0, -1), (0, 0), (0, 1)],
    "L3" : [(-1, 1), (-1, 0), (0, 0), (1, 0)],
    "S0" : [(-1, 0), (0, 0), (0, -1), (1, -1)],
    "S1" : [(0, -1), (0, 0), (1, 0), (1, 1)],
    "S2" : [(-1, 1), (0, 1), (0, 0), (1, 0)],
    "S3" : [(-1, -1), (-1, 0), (0, 0), (0, 1)],
    "Z0" : [(-1, -1), (0, -1), (0, 0), (1, 0)],
    "Z1" : [(-1, 1), (-1, 0), (0, 0), (0, -1)],
    "Z2" : [(-1, 0), (0, 0), (0, 1), (1, 1)],
    "Z3" : [(0, 1), (0, 0), (1, 0), (1, -1)],
    "O0" : [(0, 0), (1, 0), (1, 1), (0, 1)],
    "O1" : [(0, 0), (1, 0), (1, 1), (0, 1)],
    "O2" : [(0, 0), (1, 0), (1, 1), (0, 1)],
    "O3" : [(0, 0), (1, 0), (1, 1), (0, 1)],
    }

class Piece:
    def __init__(self, type, x, y, rotation, tile_size):
        self.type = type
        self.x = x
        self.y = y
        self.shape = SHAPES[type + str(rotation)]
        self.rotation = rotation
        self.tile_size = tile_size

    def blocks(self):
        blocc = list()
        for block in self.shape:
            x = block[0] + self.x
            y = block[1] + self.y
            blocc.append([x, y])
        return blocc

    
    def move(self, board, direction):
        test = Piece(self.type, self.x + direction, self.y, self.rotation, self.tile_size)
        if board.valid(test):
            self.x += direction

    def rotate(self, board):
        test = Piece(self.type, self.x, self.y, self.rotation + 1 if self.rotation < 3 else 0, self.tile_size)
        if board.valid(test):
            if self.rotation < 3:
                self.rotation += 1
                self.shape = SHAPES[self.type + str(self.rotation)]
            else: 
                self.rotation = 0
                self.shape = SHAPES[self.type + str(self.rotation)]

    def render(self, surf, board):
        blocks = list()
        for block in self.shape:
            x = block[0] + self.x
            y = block[1] + self.y
            blocks.append([x, y])
        for block in blocks:
            blocc = pygame.Rect((surf.get_width() / 2 - board.width * self.tile_size / 2 - 4) + (9 * block[0]),  1 + 9 * block[1], self.tile_size, self.tile_size)
            pygame.draw.rect(surf, (255, 255, 0), blocc)