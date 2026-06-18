import pygame

class Tile:
    def __init__(self, size, pos, num):
        self.size = list(size)
        self.pos = list(pos)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.highlight_rect = pygame.Rect(pos[0] - 2, pos[1] - 2, size[0] + 4, size[1] + 4)
        self.highlighted = False
        self.num = num

    def highlight(self, num):
        if self.num == num:
            self.highlighted = True
        else: 
            self.highlighted = False

    def render(self, surf, offset = (0, 0)):
        if (self.highlighted):
            pygame.draw.rect(surf, (217, 217, 217), self.highlight_rect, border_radius=7)
        
        pygame.draw.rect(surf, (210, 210, 210), self.rect, border_radius=5)