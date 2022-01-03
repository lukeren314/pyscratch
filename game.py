import pygame
import sys
from .constants import CODE_TO_KEY, DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT
from .sprite import Sprite

class Game:
    def __init__(self, backdrop_filepaths, screen_size = (DEFAULT_SCREEN_WIDTH, DEFAULT_SCREEN_HEIGHT)):
        self.screen_size = screen_size
        self.screen = pygame.display.set_mode(self.screen_size)
        self.clock = pygame.time.Clock()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.hidden_sprites = pygame.sprite.Group()
        self.backdrops = [pygame.transform.scale(pygame.image.load(backdrop_filepath), self.screen_size) for backdrop_filepath in backdrop_filepaths]
        self.backdrop_index = 0
        if self.backdrops:
            self.backdrop = self.backdrops[self.backdrop_index]
        else:
            self.backdrop = pygame.Surface(self.screen_size)
            self.backdrop.fill((255, 255, 255))
        
        for SpriteClass in Sprite.__subclasses__():
            print(f"Added sprite {SpriteClass.__name__} to game")
            sprite = SpriteClass(self)
            self.add_sprite(sprite)

    def set_backdrop(self, backdrop_number):
        self.backdrop_index = backdrop_number - 1
        self.update_backdrop()

    def next_backdrop(self):
        self.set_backdrop((self.backdrop_index % len(self.backdrops)) + 1)

    def update_backdrop(self):
        self.backdrop = self.backdrops[self.backdrop_index]
    
# GAME LOOP -------------------------------------------------------------------

    def run(self):
        while True:
            self.loop()

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pass
            elif event.type == pygame.KEYUP:
                if event.key in CODE_TO_KEY:
                    char = CODE_TO_KEY[event.key]
                    for sprite in self.all_sprites.sprites():
                        sprite.when_key_pressed(char)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for sprite in self.all_sprites.sprites():
                    if sprite.rect.collidepoint(event.pos):
                        sprite.when_this_sprite_clicked()
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
        self.all_sprites.draw(self.screen)
        pygame.display.flip()

# SPRITES ----------------------------------------------------------------------

    def add_sprite(self, sprite):
        self.all_sprites.add(sprite)

    def show_sprite(self, sprite):
        if sprite in self.hidden_sprites and sprite not in self.all_sprites:
            self.hidden_sprites.remove(sprite)
            self.all_sprites.add(sprite)

    def hide_sprite(self, sprite):
        if sprite in self.all_sprites and sprite not in self.hidden_sprites:
            self.all_sprites.remove(sprite)
            self.hidden_sprites.add(sprite)
    
    def is_sprite_hidden(self, sprite):
        return sprite in self.hidden_sprites

    def get_next_layer(self):
        if len(self.all_sprites) == 0:
            return 0
        return self.all_sprites.get_top_layer() + 1

    def bring_to_front(self, sprite):
        self.all_sprites.move_to_front(sprite)
    
    def bring_to_back(self, sprite):
        self.all_sprites.move_to_back(sprite)
    
    def go_forward_layers(self, sprite, num_layers):
        if self.all_sprites.get_layer_of_sprite(sprite) == self.all_sprites.get_top_layer() and len(self.all_sprites.get_sprites_from_layer(self.all_sprites.get_top_layer())) == 1:
            return
        target_layer = min(self.all_sprites.get_top_layer() + 1, self.all_sprites.get_layer_of_sprite(sprite) + num_layers)
        self.all_sprites.change_layer(sprite, target_layer)
    
    def go_backward_layers(self, sprite, num_layers):
        if self.all_sprites.get_layer_of_sprite(sprite) == self.all_sprites.get_bottom_layer()and len(self.all_sprites.get_sprites_from_layer(self.all_sprites.get_bottom_layer())) == 1:
            return
        target_layer = min(self.all_sprites.get_top_layer() - 1, self.all_sprites.get_layer_of_sprite(sprite) - num_layers)
        self.all_sprites.change_layer(sprite, target_layer)

