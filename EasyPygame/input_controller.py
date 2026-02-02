from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .actors import Player
    from .game_engine import Canvas


class KeyboardController:
    """Handles keyboard input for player movement."""
    
    movement_speed: int

    def __init__(self, movement_speed: int = 2) -> None:
        self.movement_speed = movement_speed

    def handle_keys(self, player: Player, canvas: Canvas) -> None:
        """
        Process keyboard input and move the player accordingly.
        
        Uses WASD keys for movement, respecting canvas boundaries.
        
        Args:
            player: The player character to move
            canvas: The game canvas (for boundary checking)
        """
        key = pygame.key.get_pressed()
        
        # Down (S key)
        if key[pygame.K_s] and player.box_collider.y < canvas.screen_size[1] - player.size:
            player.box_collider.y += self.movement_speed
        
        # Up (W key)
        if key[pygame.K_w] and player.box_collider.y > 0:
            player.box_collider.y -= self.movement_speed
        
        # Right (D key)
        if key[pygame.K_d] and player.box_collider.x < canvas.screen_size[0] - player.size:
            player.box_collider.x += self.movement_speed
        
        # Left (A key)
        if key[pygame.K_a] and player.box_collider.x > 0:
            player.box_collider.x -= self.movement_speed
