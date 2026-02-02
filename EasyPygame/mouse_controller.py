from __future__ import annotations

from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from .actors import Character

# Type alias for position
Position = tuple[int, int]


class MouseController:
    """Handles mouse input for games."""

    def __init__(self) -> None:
        """Initialize the mouse controller."""
        pass

    @staticmethod
    def get_position() -> Position:
        """
        Get the current mouse position.
        
        Returns:
            Tuple of (x, y) coordinates
        """
        return pygame.mouse.get_pos()

    @staticmethod
    def is_pressed(button: int = 0) -> bool:
        """
        Check if a mouse button is currently pressed.
        
        Args:
            button: 0 = left, 1 = middle, 2 = right
            
        Returns:
            True if the button is pressed
        """
        return pygame.mouse.get_pressed()[button]

    @staticmethod
    def is_left_pressed() -> bool:
        """Check if left mouse button is pressed."""
        return pygame.mouse.get_pressed()[0]

    @staticmethod
    def is_right_pressed() -> bool:
        """Check if right mouse button is pressed."""
        return pygame.mouse.get_pressed()[2]

    @staticmethod
    def is_over(character: Character) -> bool:
        """
        Check if the mouse is hovering over a character.
        
        Args:
            character: The character to check
            
        Returns:
            True if mouse is over the character's hitbox
        """
        mouse_pos = pygame.mouse.get_pos()
        return character.box_collider.collidepoint(mouse_pos)

    @staticmethod
    def is_clicking(character: Character, button: int = 0) -> bool:
        """
        Check if the mouse is clicking on a character.
        
        Args:
            character: The character to check
            button: 0 = left, 1 = middle, 2 = right
            
        Returns:
            True if mouse is over character AND button is pressed
        """
        return (
            MouseController.is_over(character) 
            and pygame.mouse.get_pressed()[button]
        )
