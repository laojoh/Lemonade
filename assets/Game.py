import numpy as np
import mmap
import os
import pygame
import sys
from scripts.entities import PhysicsEntity, Player
from scripts.utils import Animation, load_image, load_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("lemonade")
        self.screen = pygame.display.set_mode((480, 320))
        self.display = pygame.Surface((240, 160))

        fb = open("/dev/fb0", "r+b")
        self.fbmem = mmap.mmap(fb.fileno(), self.screen.get_width, self.screen.get_height() * 4, offset = 0)

        self.clock = pygame.time.Clock()

        self.movement = [False, False]

        self.assets = {
            "decor" : load_images("/tiles/decor"),
            "grass" : load_images("/tiles/grass"),
            "large_decor" : load_images("/tiles/large_decor"),
            "stone" : load_images("/tiles/stone"),
            "player" : load_image("/entities/player.png"),
            "background" : load_image("/background.png"),
            "clouds" : load_images("/clouds"),
            "player/idle" : Animation(load_images("/entities/player/idle"), img_dur = 6),
            "player/run" : Animation(load_images("/entities/player/run"), img_dur = 4),
            "player/jump" : Animation(load_images("/entities/player/jump")),
            "player/slide" : Animation(load_images("/entities/player/slide")),
            "player/wall_slide" : Animation(load_images("/entities/player/wall_slide"))



        }

        self.clouds = Clouds(self.assets["clouds"], count = 16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size = 16)

        self.scroll = [0, 0]

    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset = render_scroll)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = True
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = True
                    if event.key == pygame.K_UP:
                        self.player.velocity[1] = -3

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.movement[0] = False
                    if event.key == pygame.K_RIGHT:
                        self.movement[1] = False
            
            arr = pygame.surfarray.array3d(pygame.transform.scale(self.display, self.screen.get_size()))
            frame = np.empty((self.screen.get_width(), self.screen.get_height(), 4), dtype = np.uint8)

            frame[:, :, 0] = arr[:, :, 2].T
            frame[:, :, 1] = arr[:, :, 1].T
            frame[:, :, 2] = arr[:, :, 0].T
            frame[:, :, 3] = 255

            self.fbmem.seek(0)
            self.fbmem.write(frame.tobytes())

            self.clock.tick(60)

Game().run()    