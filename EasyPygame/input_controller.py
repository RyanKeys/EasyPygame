import pygame

class KeyboardController:
    
    def __init__(self,movement_speed=2):
        self.movement_speed = movement_speed
    
    def handle_keys(self, player, canvas):
      """ Handles Keys """
      key = pygame.key.get_pressed()
      if key[pygame.K_s] and player.box_collider.y < canvas.screen_size[1]-player.size: # down key
            player.box_collider.y += self.movement_speed # move down
      if key[pygame.K_w] and player.box_collider.y > 0: # up ke
            player.box_collider.y -= self.movement_speed # move up
      if key[pygame.K_d] and player.box_collider.x < canvas.screen_size[0]-player.size: #move right
            player.box_collider.x += self.movement_speed 
      if key[pygame.K_a] and player.box_collider.x > 0: # left key
            player.box_collider.x -= self.movement_speed # move left