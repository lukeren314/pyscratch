import pygame
from math import sin, cos, radians, atan2, dist
from random import random

from pyscratch.constants import DEFAULT_SCREEN_CENTER_X, DEFAULT_SCREEN_CENTER_Y, KEY_TO_CODE

class Sprite(pygame.sprite.Sprite):
    def __init__(self, game, costume_filepaths=[], x=DEFAULT_SCREEN_CENTER_X, y=DEFAULT_SCREEN_CENTER_Y):
        super(Sprite, self).__init__()
        self.game = game
        self.angle = 0
        self.scale = 1
        self.costume_index = 0
        if costume_filepaths:
            self.costumes = [pygame.image.load(costume_filepath) for costume_filepath in costume_filepaths]
            self.raw_image = self.costumes[self.costume_index]
        else:
            self.raw_image = pygame.Surface()
        self.image = self.raw_image
        self.rect = self.image.get_rect()
        self._layer = self.game.get_next_layer()
        
        self.go_to(x, y)

# MOTION ----------------------------------------------------------------------

    def move(self, num_steps=10):
        dx, dy = num_steps * cos(radians(self.angle)), num_steps * sin(radians(self.angle))
        self.change_x_by(dx)
        self.change_y_by(dy)
    
    def turn_clockwise(self, num_degrees=15):
        self.set_angle(self.angle+num_degrees)
    
    def turn_counterclockwise(self, num_degrees=15):
        self.set_angle(self.angle-num_degrees)
    
    def set_angle(self, angle):
        self.angle = angle
        self.update_image()

    def point_in_direction(self, degrees):
        self.set_angle(degrees)
    
    def point_towards_mouse_pointer(self):
        x, y = pygame.mouse.get_pos()
        self.point_towards_position(x, y)
        
    def point_towards_sprite(self, other_sprite):
        self.point_towards_position(other_sprite.x(), other_sprite.y())
        
    def point_towards_position(self, x, y):
        self.angle = atan2(x-self.x(), y-self.y())
    
    def go_to_random_position(self):
        width, height = self.game.screen_size
        self.go_to(random() * width, random() * height)
    
    def go_to_mouse_pointer(self):
        x, y = pygame.mouse.get_pos()
        self.go_to(x, y)
    
    def go_to_sprite(self, other_sprite):
        self.go_to(other_sprite.x(), other_sprite.y())

    def go_to(self, x, y):
        self.set_x_to(x)
        self.set_y_to(y)

    def change_x_by(self, x_value):
        self.set_x_to(self.x()+x_value)

    def change_y_by(self, y_value):
        self.set_y_to(self.y()+y_value)

    def set_x_to(self, x_value):
        self.rect.centerx = x_value

    def set_y_to(self, y_value):
        self.rect.centery = y_value

# LOOKS -----------------------------------------------------------------------

    def next_costume(self):
        self.switch_costume_to((self.costume_index % len(self.costumes)) + 1)

    def switch_costume_to(self, costume_number):
        self.costume_index = costume_number - 1
        self.update_costume()

    def update_costume(self):
        old_center = self.center()
        self.raw_image = self.costumes[self.costume_index]
        self.rect = self.raw_image.get_rect(center=old_center)
        self.update_image()

    def change_size_by(self, percent):
        self.set_size_to(self.scale, percent / 100)
        
    def set_size_to(self, percent):
        self.set_scale_to(percent / 100)

    def set_scale_to(self, scale):
        self.scale = scale
        self.update_image()

    def show(self):
        self.game.show_sprite(self)
    
    def hide(self):
        self.game.hide_sprite(self)
    
    def is_hidden(self):
        return self.game.is_sprite_hidden(self)

    def bring_to_front(self):
        self.game.bring_to_front(self)
    
    def bring_to_back(self):
        self.game.bring_to_back(self)
    
    def go_forward_layers(self, num_layers):
        self.game.go_forward_layers(self, num_layers)
    
    def go_backward_layers(self, num_layers):
        self.game.go_backward_layers(self, num_layers)

# EVENTS ----------------------------------------------------------------------

    def when_game_begins(self):
        pass
    
    def when_key_pressed(self, key):
        pass
    
    def when_this_sprite_clicked(self):
        pass

# CONTROL ---------------------------------------------------------------------

    def when_i_start_as_a_clone(self):
        pass

    def create_clone_of_myself(self):
        clone = self.__class__(self.game)

        clone.switch_costume_to(self.costume_index + 1)
        clone.go_to(self.x(), self.y())
        clone.point_in_direction(self.angle)
        clone.set_scale_to(self.scale)

        clone.when_i_start_as_a_clone()
        self.game.add_sprite(clone)

    def create_clone_of_sprite(self, other_sprite):
        other_sprite.create_clone_of_myself()

# SENSING ---------------------------------------------------------------------

    def touching_mouse_pointer(self):
        return self.rect.collidepoint(pygame.mouse.get_pos())
    
    def touching_sprite(self, other_sprite):
        return self.rect.colliderect(other_sprite.rect)

    def distance_from_mouse(self):
        return dist((self.x(), self.y()), pygame.mouse.get_pos())
    
    def key_pressed(self, key):
        assert key in KEY_TO_CODE, f"Key: {key} does not exist...yet?"
        return pygame.key.get_pressed()[KEY_TO_CODE[key]]
    
    def mouse_down(self):
        return pygame.mouse.get_pressed()[0]
    
    def mouse_position(self):
        return pygame.mouse.get_pos()

# RECT ------------------------------------------------------------------------

    def x(self):
        return self.rect.centerx

    def y(self):
        return self.rect.centery

    def width(self):
        return self.rect.width
    
    def height(self):
        return self.rect.height

    def center(self):
        return self.rect.center

# GAME_LOOP -------------------------------------------------------------------

    def update(self):
        pass

    def update_image(self):
        new_size = self.scale * self.width(), self.scale * self.height()
        scaled_image = pygame.transform.scale(self.raw_image, new_size)
        
        rotated_image = pygame.transform.rotate(scaled_image, -self.angle)
        old_center = self.center()
        self.image = rotated_image
        self.rect = self.raw_image.get_rect(center=old_center)

