import pygame
from math import sin, cos, radians, atan2


class Sprite(pygame.sprite.Sprite):
    def __init__(self, costume_filepaths):
        super(Sprite, self).__init__()
        self.angle = 0
        self.scale = 1
        self.costumes = [pygame.image.load(costume_filepath) for costume_filepath in costume_filepaths]
        if self.costumes:
            self.image = self.costumes[0]
        else:
            self.image = pygame.Surface()
        self.rect = self.image.get_rect()
        self._layer = self.rect.bottom


# MOTION ----------------------------------------------------------------------

    def move(self, num_steps=10):
        dx, dy = num_steps * cos(radians(self.angle)), num_steps * sin(radians(self.angle))
        self.change_x_by(dx)
        self.change_y_by(dy)
    
    def turn_clockwise(self, num_degrees=15):
        self.angle += num_degrees
    
    def turn_counterclockwise(self, num_degrees=15):
        self.angle -= num_degrees
    
    def point_in_direction(self, degrees):
        self.angle = degrees
    
    def point_towards_mouse_pointer(self):
        x, y = pygame.mouse.get_pos()
        self.point_towards_position(x, y)
        
    def point_towards_sprite(self, other_sprite):
        self.point_towards_position(other_sprite.x(), other_sprite.y())
        
    def point_towards_position(self, x, y):
        self.angle = atan2(x-self.x(), y-self.y())
    
    def go_to_random_position(self):
        pass
    
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

    def bring_to_front(self):
        pass
    
    def bring_to_back(self):
        pass
    
    def go_forward_layers(self, num_layers):
        pass
    
    def go_backward_layers(self, num_layers):
        pass

# LOOKS -----------------------------------------------------------------------

    def switch_costume_to(self, costume_number):
        old_center = self.center()
        self.image = self.costumes[costume_number - 1]
        self.rect = self.image.get_rect(center=old_center)

    def change_size_by(self, percent):
        self.set_size_to(self.scale, percent / 100)
        
    def set_size_to(self, percent):
        self.scale = percent / 100

# EVENTS ----------------------------------------------------------------------

    def when_game_begins(self):
        pass
    
    def when_key_pressed(self, key):
        pass
    
    def when_sprite_clicked(self):
        pass

# SENSING ---------------------------------------------------------------------

    def touching_mouse_pointer(self):
        pass
    
    def touching_sprite(self, other_sprite):
        pass

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

    def draw(self, screen):
        new_size = self.scale * self.width(), self.scale * self.height()
        scaled_image = pygame.transform.scale(self.image, new_size)
        
        rotated_image = pygame.transform.rotate(scaled_image, -self.angle)
        new_rect = rotated_image.get_rect(center=self.center())
        
        screen.blit(rotated_image, new_rect)