"""
EasyPygame - A package designed to simplify your Pygame development!

This package provides easy-to-use classes and functions for creating games with Pygame.
"""

from .actors import Player, Character, Coordinate
from .game_engine import Engine, Canvas, ScreenSize, Color
from .input_controller import KeyboardController

__version__ = "0.1.2"
__author__ = "Ryan Keys"
__email__ = "r.keys1998@gmail.com"

# Make the main classes easily accessible
__all__ = [
    'Player',
    'Character',
    'Engine',
    'Canvas',
    'KeyboardController',
    # Type aliases
    'Coordinate',
    'ScreenSize',
    'Color',
]