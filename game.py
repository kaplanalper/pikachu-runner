import pygame
import sys

from pikachu import Pikachu
from enemy import Enemy
from random import choice
from settings import *

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pikachu Runner")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()

        # fonts
        self.info_font = pygame.font.Font("fonts/info_font.ttf", 50)
        self.score_font = pygame.font.Font("fonts/info_font.ttf", 30)
        self.fps_font = pygame.font.Font("fonts/fps_font.ttf", 30)

        # background
        self.background_surf = pygame.image.load("graphics/other/background.png").convert_alpha()
        self.background_surf = pygame.transform.scale(self.background_surf, (WIDTH, HEIGHT))

        # pikachu
        self.pikachu = pygame.sprite.GroupSingle()
        self.pikachu.add(Pikachu((WIDTH / 8, HEIGHT * 0.775)))
        self.pikachu_sprite = self.pikachu.sprites()[0]

        # enemies
        self.obstacle_group = pygame.sprite.Group()

        # death sound
        self.death_sound = pygame.mixer.Sound("sound/death.wav")
        self.death_sound.set_volume(0.5)

        # info texts
        # title
        self.pokemon_title = pygame.image.load("graphics/other/pokemon.png").convert_alpha()
        self.pokemon_title = pygame.transform.scale(self.pokemon_title, (self.pokemon_title.get_width() // 4, self.pokemon_title.get_height() // 4.25))
        self.pokemon_title_rect = self.pokemon_title.get_rect(midbottom=(WIDTH // 2, HEIGHT // 5))

        # game name
        self.game_name = self.info_font.render("Pikachu Runner", False, "#ffcc01")
        self.game_name_rect = self.game_name.get_rect(center=(WIDTH // 2, self.pokemon_title_rect.midbottom[1] + 75))

        # game info
        self.game_info = self.info_font.render("Press enter to start", False, (164, 140, 49))
        self.game_info_rect = self.game_info.get_rect(center=(WIDTH // 2, self.pikachu_sprite.get_pos()[1] + 50))

        self.start_time = 0
        self.score = 0

        self.running = False

        # timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1500)

    def run(self):
        while True:
            display_score_pos_y = 50
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()

                if event.type == self.obstacle_timer:
                    # 25% chance of spawning a fly
                    self.obstacle_group.add(Enemy(choice(["skeleton", "skeleton", "skeleton", "fly"])))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                self.quit()

            if self.running:
                self.score = int(pygame.time.get_ticks() / 1000) - self.start_time

                if self.pikachu_sprite.get_pos()[0] == WIDTH // 2:
                    self.pikachu_sprite.set_pos((WIDTH // 8, HEIGHT * 0.775))

                self.screen.blit(self.background_surf, (0, 0))
                
                self.pikachu.draw(self.screen)
                self.pikachu.update()

                self.obstacle_group.draw(self.screen)
                self.obstacle_group.update()

                self.running = self.check_collision()
            else:
                self.screen.fill("#063970")
                display_score_pos_y = self.game_info_rect.midbottom[1] - 100

                self.pikachu_sprite.set_pos((WIDTH // 2, self.game_name_rect.midbottom[1] + HEIGHT // 4))
                self.pikachu.draw(self.screen)
                self.pikachu_sprite.animate()

                self.screen.blit(self.pokemon_title, self.pokemon_title_rect)
                self.screen.blit(self.game_name, self.game_name_rect)
                self.screen.blit(self.game_info, self.game_info_rect)

                if keys[pygame.K_KP_ENTER] or keys[pygame.K_RETURN]:
                    self.start_time = int(pygame.time.get_ticks() / 1000)
                    self.running = True
            
            self.display_fps()
            self.display_score(display_score_pos_y)

            pygame.display.update()
            self.clock.tick(FPS)

    def display_score(self, pos_y):
        self.score_surf = self.score_font.render(f"Score: {self.score}", False, (164, 140, 49))
        self.score_rect = self.score_surf.get_rect(midbottom=(WIDTH // 2, pos_y))
        self.screen.blit(self.score_surf, self.score_rect)

    def display_fps(self):
        self.fps_info = self.fps_font.render(f"FPS: {int(self.clock.get_fps())}", False, (164, 140, 49))
        self.fps_info_rect = self.fps_info.get_rect(topleft=(10, 10))
        self.screen.blit(self.fps_info, self.fps_info_rect)

    def check_collision(self):
        if pygame.sprite.spritecollide(self.pikachu.sprite, self.obstacle_group, False):
            self.obstacle_group.empty()
            self.death_sound.play()
            return False
        else:
            return True
    
    def quit(self):
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
