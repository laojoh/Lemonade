import pygame

class Button:
    def __init__(self, size, pos, num, banner_img):
        self.size = list(size)
        self.pos = list(pos)
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.highlight_rect = pygame.Rect(pos[0] - 2, pos[1] - 2, size[0] + 4, size[1] + 4)
        self.highlighted = False
        self.num = num
        self.banner_img = banner_img

    def highlight(self, num):
        if self.num == num:
            self.highlighted = True
        else: 
            self.highlighted = False

    def render(self, surf, offset = (0, 0)):
        if (self.highlighted):
            pygame.draw.rect(surf, (170, 170, 170), self.highlight_rect, border_radius=7)
        
        surf.blit(self.banner_img, self.rect)
        print(self.rect.size)
