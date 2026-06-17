import math
import numpy as np
import mmap
import os
import pygame
import sys
import random
from gpiozero import Button
from scripts.entities import PhysicsEntity, Player, Enemy
from scripts.utils import Animation, load_image, load_images
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds
from scripts.particle import Particle
from scripts.spark import Spark

class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("lemonade")
        self.screen = pygame.display.set_mode((480, 320))
        self.display = pygame.Surface((240, 160))

        self.shake_surface = pygame.Surface(self.display.get_size())

        fb = open("/dev/fb0", "r+b")
        self.fbmem = mmap.mmap(fb.fileno(), self.screen.get_width() * self.screen.get_height() * 4)

        self.button1 = Button(12)
        self.button2 = Button(16)
        self.button3 = Button(20)
        self.button4 = Button(21)

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
            "player/wall_slide" : Animation(load_images("/entities/player/wall_slide")),
            "particle/leaf" : Animation(load_images("/particles/leaf"), img_dur = 15, loop = False),
            "particle/particle" : Animation(load_images("/particles/particle"), img_dur = 6, loop = False),
            "enemy/idle" : Animation(load_images("/entities/enemy/idle"), img_dur = 6),
            "enemy/run" : Animation(load_images("/entities/enemy/run"), img_dur = 4),
            "gun" : load_image("/gun.png"),
            "projectile" : load_image("/projectile.png"),
        }

        self.clouds = Clouds(self.assets["clouds"], count = 16)

        self.player = Player(self, (50, 50), (8, 15))

        self.tilemap = Tilemap(self, tile_size = 16)

        self.level = 0
        self.load_level(self.level)

        self.screenshake = 0

    def load_level(self, map_id):
        self.tilemap.load("data/maps/" + str(map_id) + ".json")
        self.leaf_spawners = []
        for tree in self.tilemap.extract([("large_decor", 3)], keep = True):
            self.leaf_spawners.append(pygame.Rect(4 + tree["pos"][0], 4 + tree["pos"][1], 23, 13))

        self.enemies = []
        for spawner in self.tilemap.extract([("spawners", 0), ("spawners", 1)]):
            if spawner["variant"] == 0:
                self.player.pos = spawner["pos"]
                self.player.air_time = 0
            else:
                self.enemies.append(Enemy(self, spawner["pos"], (8, 15)))

        self.projectiles = []
        self.particles = []
        self.sparks = []

        self.scroll = [0, 0]
        self.dead = 0
        self.transition = -30
        self.jump_times = 0

        self.cloud = self.assets["clouds"][0]
        pygame.image.save(self.cloud, "cloud_reencoded.bmp")

        self.cloud = pygame.image.load("cloud_reencoded.bmp").convert()

    def run(self):
        while True:
            self.display.blit(self.assets["background"], (0, 0))

            self.screenshake = max(0, self.screenshake - 0.5)

            if not len(self.enemies):
                self.transition += 0.5
                if self.transition > 30:
                    self.level = min(self.level + 1, len(os.listdir("data/maps")) - 1)
                    self.load_level(self.level)
            if self.transition < 0:
                self.transition += 0.5

            if self.dead:
                self.dead += 1
                if self.dead == 30:
                    self.trsnsition = min(30, self.transition + 1)
                if self.dead > 40:
                    self.load_level(self.level)

            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))

            for rect in self.leaf_spawners:
                if random.random() * 49999 < rect.width * rect.height:
                    pos = (rect.x + random.random() * rect.width, rect.y + random.random() * rect.height)
                    self.particles.append(Particle(self, "leaf", pos, velocity = [random.random() * 0.5 - 0.25, random.random() * 0.2 + 0.25], frame = random.randint(0, 20)))


            self.clouds.update()
            self.clouds.render(self.display, offset = render_scroll)

            self.tilemap.render(self.display, offset = render_scroll)

            for enemy in self.enemies.copy():
                kill = enemy.update(self.tilemap, (0, 0))
                enemy.render(self.display, offset = render_scroll)
                if kill:
                    self.enemies.remove(enemy)

            if not self.dead:    
                self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
                self.player.render(self.display, offset = render_scroll)

            # [[x, y], direction, timer]
            for projectile in self.projectiles.copy():
                projectile[0][0] += projectile[1]
                projectile[2] += 1
                img = self.assets["projectile"]
                self.display.blit(img, (projectile[0][0] - img.get_width() / 2 - render_scroll[0], projectile[0][1] - img.get_height() / 2 - render_scroll[1]))
                if self.tilemap.solid_check(projectile[0]):
                    self.projectiles.remove(projectile)
                    for i in range(4):
                        self.sparks.append(Spark(projectile[0], random.random() - 0.5 + (math.pi if projectile[1] > 0 else 0), 2 + random.random()))
                elif projectile[2] > 360:
                    self.projectiles.remove(projectile)
                elif abs(self.player.dashing) < 50:
                    if self.player.rect().collidepoint(projectile[0]):
                        self.projectiles.remove(projectile)
                        self.dead += 1
                        self.screenshake = max(20, self.screenshake)
                        for i in range(20):
                            angle = random.random() * math.pi * 2
                            speed = random.random() * 5
                            self.sparks.append(Spark(self.player.rect().center, angle, 2 + random.random()))
                            self.particles.append(Particle(self, "particle", self.player.rect().center, velocity = [math.cos(angle + math.pi) * speed * 0.5, math.sin(angle + math.pi) * speed * 0.5], frame = random.randint(0, 7)))

            for spark in self.sparks.copy():
                kill = spark.update()
                spark.render(self.display, offset = render_scroll)
                if kill:
                    self.sparks.remove(spark)


            for particle in self.particles.copy():
                kill = particle.update()
                particle.render(self.display, offset = render_scroll)
                if particle.type == "leaf":
                    particle.pos[0] += math.sin(particle.animation.frame * 0.035) * 0.3
                if kill:
                    self.particles.remove(particle)


            if self.button1.is_pressed and self.jump_times == 0:
                self.player.jump()
                self.jump_times = 1
            elif not self.button1.is_pressed:
                self.jump_times = 0
            if self.button2.is_pressed:
                self.movement[1] = True
            else: 
                self.movement[1] = False
            if self.button3.is_pressed:
                self.movement[0] = True
            else:
                self.movement[0] = False
            if self.button4.is_pressed:
                self.player.dash()


            if self.transition:
                transition_surf = pygame.Surface(self.display.get_size())
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2, self.display.get_height() // 2), (30 - abs(self.transition)) * 8)
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2 + ((30 - abs(self.transition)) * 8) * 0.6, self.display.get_height() // 2 - ((30 - abs(self.transition)) * 8) * 0.6), (30 - abs(self.transition)) * 3)
                pygame.draw.circle(transition_surf, (255, 255, 255), (self.display.get_width() // 2 - ((30 - abs(self.transition)) * 8) * 0.6, self.display.get_height() // 2 + ((30 - abs(self.transition)) * 8) * 0.6), (30 - abs(self.transition)) * 3)
                transition_surf.set_colorkey((255, 255, 255))
                self.display.blit(transition_surf, (0, 0))

            screenshake_offset = (random.random() * self.screenshake - self.screenshake / 2, random.random() * self.screenshake - self.screenshake / 2)

            self.display.blit(self.cloud, (0, 0))

            self.shake_surface.fill((0, 0, 0))
            self.display.fill((0, 255, 0))
            self.shake_surface.blit(self.display, screenshake_offset)

            scaled_surf = pygame.transform.scale(self.shake_surface, self.screen.get_size())

            bgra_frame = bytes(scaled_surf.get_buffer())

            self.fbmem.seek(0)

            self.fbmem.write(bgra_frame)

            self.clock.tick(60)

Game().run()
