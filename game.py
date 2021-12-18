import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from sprite import Sprite

class Game:
    def __init__(self):
        self.screen_size = (SCREEN_WIDTH, SCREEN_HEIGHT-20)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.backdrop = pygame.Surface(self.screen_size)
        self.backdrop.fill((255, 255, 255))
        

    def create_sprite(self, costume_filepaths):
        sprite = Sprite(costume_filepaths)
        self.all_sprites.add(sprite)
        return sprite
    
    def key_pressed(self, key):
        assert key in keys, f"Key: {key} does not exist...yet?"
        return pygame.key.get_pressed()[keys[key]]
    
    def set_backdrop(self, image_filename):
        self.backdrop = pygame.image.load(image_filename)
        self.backdrop = pygame.transform.scale(self.backdrop, self.screen_size)
    
    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pass
            elif event.type == pygame.MOUSEBUTTONUP:
                pass
            
        self.update()
        self.draw()
        
    def update(self):
        dt = self.clock.tick(30)
        self.all_sprites.update()
        
    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.backdrop, self.backdrop.get_rect())
        for sprite in self.all_sprites.sprites():
            sprite.draw(self.screen)
        pygame.display.flip()
        

keys = {
    'a': pygame.K_a,
    'b': pygame.K_b,
    'c': pygame.K_c,
    'd': pygame.K_d,
    'e': pygame.K_e,
    'f': pygame.K_f,
    'g': pygame.K_g,
    'h': pygame.K_h,
    'i': pygame.K_i,
    'j': pygame.K_j,
    'k': pygame.K_k,
    'l': pygame.K_l,
    'm': pygame.K_m,
    'n': pygame.K_n,
    'o': pygame.K_o,
    'p': pygame.K_p,
    'q': pygame.K_q,
    'r': pygame.K_r,
    's': pygame.K_s,
    't': pygame.K_t,
    'u': pygame.K_u,
    'v': pygame.K_v,
    'w': pygame.K_w,
    'x': pygame.K_x,
    'y': pygame.K_y,
    'z': pygame.K_z
}
