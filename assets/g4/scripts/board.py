import pygame
import sys

class Board:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.tile_size = tile_size

        self.board = list()
        
        for i in range(self.height):
                row = list()
                for j in range(self.width):
                    row.append(0)
                self.board.append(row)
                
    def print(self):
        for i in self.board:
            print(i)

    def clear(self):
        for i in len(self.board):
            for j in len(i):
                self.board[i][j] = 0

    def inBounds(self, x, y):
        return x < self.width and x >= 0 and y < self.height and y >= 0
    
    def occupied(self, x, y):
        return self.board[y][x] != 0
    
    def valid(self, piece):
        for block in piece.blocks():
            if not self.inBounds(block[0], block[1]) or self.occupied(block[0], block[1]):
                return False
        return True
    
    def lock(self, piece):
        for block in piece.blocks():
            self.board[block[1]][block[0]] = piece.type

    def rowFull(self, row):
        for i in row:
            if i == 0:
                return False
        return True
    
    def clearLines(self):
        new_board = []
        lines_cleared = 0

        for row in self.board:
            if self.rowFull(row):
                lines_cleared += 1
            else:
                new_board.append(row)

        while len(new_board) < self.height:
            new_board.insert(0, [0] * self.width)

        self.board = new_board
        return lines_cleared

    # 1 : I, 2: T, 3: J, 4: L, 5: S, 6: Z, 7: O
    def render(self, surf):
            x = surf.get_width() / 2
            y = 1

            for i in range(self.height):
                x = surf.get_width() / 2 - self.width * self.tile_size / 2 - 4
                for j in range(self.width):
                    tile = pygame.Rect(x, y, self.tile_size, self.tile_size)
                    if self.board[i][j] == 0:
                        pygame.draw.rect(surf, (219, 219, 219), tile)
                    else: 
                        pygame.draw.rect(surf, (255, 255, 0), tile)
                    x += self.tile_size + 1
                y += self.tile_size + 1