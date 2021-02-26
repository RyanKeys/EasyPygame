import pygame
from EasyPygame.input_controller import KeyboardController

class Character(object):
    
    def __init__(self, spawn_coordinates=(0,0), size=20, sprite=None):
        self.size = size
        self.check_for_sprite(sprite)
        self.box_collider = self.image.get_rect()
        self.spawn_coordinates = spawn_coordinates
        self.box_collider.x, self.box_collider.y = spawn_coordinates[0], spawn_coordinates[1]

    def check_for_sprite(self, sprite):
        if sprite is None:
            self.image = pygame.Surface((self.size,self.size))
            self.image.fill((128,70,128))
        else:
            self.image = pygame.image.load(sprite)
            self.image= pygame.transform.scale(self.image, (self.size, self.size))
       
    def draw(self, surface):
        """ Draw on surface """
        # blit yourself at your current position
        surface.blit(self.image, (self.box_collider.x, self.box_collider.y))

    def check_collision(self, other_sprites):
        for enemy_sprite in other_sprites:
            if self.box_collider.colliderect(enemy_sprite.box_collider):
                return True


class Player(Character):

    def __init__(self, spawn_coordinates=(0,0), size=20, sprite=None):
        super().__init__(spawn_coordinates, size, sprite)
        self.controller = KeyboardController(movement_speed=10)


    def handle_keys(self,canvas):
        return self.controller.handle_keys(self, canvas)
