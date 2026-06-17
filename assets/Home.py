import pygame
import sys

import g1.Game1 as g1

class Home:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("lemonade")
        self.screen = pygame.display.set_mode((480, 320))
        self.display = pygame.Surface((240, 160))

        self.clock = pygame.time.Clock()

        self.gap = 10

        self.game_list = list()


        

    def run(self):
        while True:

            self.display.fill((255, 255, 255))

            for tile in self.game_list:
                pygame.draw.rect()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        g1.Game1().run()

            

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()))
            pygame.display.update()
            self.clock.tick(60)


Home().run()
