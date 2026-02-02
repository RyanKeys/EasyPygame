from __future__ import annotations

import pygame
from .input_controller import KeyboardController

# Type alias for coordinate tuples
Coordinate = tuple[int, int]


class Character:
    """A game character that can be drawn and checked for collisions."""
    
    size: int
    image: pygame.Surface
    box_collider: pygame.Rect
    spawn_coordinates: Coordinate

    def __init__(
        self,
        spawn_coordinates: Coordinate = (0, 0),
        size: int = 20,
        sprite: str | None = None
    ) -> None:
        self.size = size
        self.check_for_sprite(sprite)
        self.box_collider = self.image.get_rect()
        self.spawn_coordinates = spawn_coordinates
        self.box_collider.x, self.box_collider.y = spawn_coordinates[0], spawn_coordinates[1]

    def check_for_sprite(self, sprite: str | None) -> None:
        """Load a sprite image or create a default colored surface."""
        if sprite is None:
            self.image = pygame.Surface((self.size, self.size))
            self.image.fill((128, 70, 128))
        else:
            self.image = pygame.image.load(sprite)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))

    def draw(self, surface: pygame.Surface) -> None:
        """Draw the character on the given surface."""
        surface.blit(self.image, (self.box_collider.x, self.box_collider.y))

    def check_collision(self, other_sprites: list[Character]) -> bool:
        """Check if this character collides with any sprite in the list."""
        for enemy_sprite in other_sprites:
            if self.box_collider.colliderect(enemy_sprite.box_collider):
                return True
        return False


class Player(Character):
    """A player-controlled character with keyboard input handling."""
    
    controller: KeyboardController

    def __init__(
        self,
        spawn_coordinates: Coordinate = (0, 0),
        size: int = 20,
        sprite: str | None = None
    ) -> None:
        super().__init__(spawn_coordinates, size, sprite)
        self.controller = KeyboardController(movement_speed=10)

    def handle_keys(self, canvas: "Canvas") -> None:
        """Process keyboard input for player movement."""
        from .game_engine import Canvas  # Avoid circular import
        return self.controller.handle_keys(self, canvas)
