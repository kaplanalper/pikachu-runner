import pygame

from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        self.type = type
        self.frames = []
        if self.type == "skeleton":
            scale_coef =  1 / (WIDTH // 200)

            for i in range(0, 21, 3):  # load every third frame to reduce the fps drop
                skeleton = pygame.image.load(f"graphics/enemies/skeleton/skeleton{i}.png").convert_alpha()
                skeleton = pygame.transform.rotozoom(skeleton, 0, scale_coef)
                self.frames.append(skeleton)

            self.pos_y = HEIGHT * 0.775
        elif self.type == "fly":
            scale_coef = 1 / (WIDTH // 125)

            for i in range(10):
                fly = pygame.image.load(f"graphics/enemies/fly/fly{i}.png").convert_alpha()
                fly = pygame.transform.rotozoom(fly, 0, scale_coef)
                self.frames.append(fly)

            self.pos_y = HEIGHT * 0.55

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(midbottom=(WIDTH + 100, self.pos_y))

    def animate(self):
        if self.type == "skeleton":
            self.index += 3
        elif self.type == "fly":
            self.index += 0.2

        if self.index >= len(self.frames): self.index = 0
        self.image = self.frames[int(self.index)]

    def update(self):
        self.animate()

        if self.type == "skeleton":
            self.rect.x -= 15
        elif self.type == "fly":
            self.rect.x -= 15
        self.destroy()

    def destroy(self):
        if self.rect.x <= -50:
            self.kill()
