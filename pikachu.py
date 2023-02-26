import pygame

from settings import *

class Pikachu(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        scale_coef =  1 / (WIDTH // 90)
        self.run = []
        for i in range(1, 5):
            run = pygame.image.load(f"graphics/pikachu/pikachu_run{i}.png").convert_alpha()
            run = pygame.transform.rotozoom(run, 0, scale_coef)
            self.run.append(run)

        self.jump1 = pygame.image.load("graphics/pikachu/pikachu_jump1.png").convert_alpha()
        self.jump1 = pygame.transform.rotozoom(self.jump1, 0, scale_coef)
        self.jump2 = pygame.image.load("graphics/pikachu/pikachu_jump2.png").convert_alpha()
        self.jump2 = pygame.transform.rotozoom(self.jump2, 0, scale_coef)

        self.index = 0
        self.image = self.run[self.index]

        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.rect = self.image.get_rect(midbottom=(self.pos_x, self.pos_y))
        
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound("sound/jump.mp3")
        self.jump_sound.set_volume(0.5)

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= self.pos_y:
            self.gravity = -30
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 3
        self.rect.y += self.gravity
        
        if self.gravity > -5:
            self.jump = self.jump2
        elif self.gravity < -20:
            self.jump = self.jump1

        if self.rect.bottom > self.pos_y:
            self.gravity = 0
            self.rect.bottom = self.pos_y

    def animate(self):
        if self.rect.bottom < self.pos_y:
            self.image = self.jump
        else:
            self.index += 0.5
            if self.index >= len(self.run): self.index = 0
            self.image = self.run[int(self.index)]

    def set_pos(self, pos):
        self.pos_x = pos[0]
        self.pos_y = pos[1]
        self.rect = self.image.get_rect(midbottom=(self.pos_x, self.pos_y))

    def get_pos(self):
        return self.pos_x, self.pos_y
    
    def update(self):
        self.input()
        self.apply_gravity()
        self.animate()
