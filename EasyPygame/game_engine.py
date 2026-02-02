from __future__ import annotations

import sys
from typing import Callable, TypeVar

import pygame

# Type aliases
ScreenSize = tuple[int, int]
Color = tuple[int, int, int]

F = TypeVar('F', bound=Callable[[], None])


class Canvas:
    """Manages the game window and drawing surface."""
    
    screen_size: ScreenSize
    background_color: Color
    surface: pygame.Surface

    def __init__(
        self,
        screen_size: ScreenSize = (600, 600),
        background_color: Color = (255, 255, 255)
    ) -> None:
        self.screen_size = screen_size
        self.background_color = background_color
        self.surface = pygame.display.set_mode(self.screen_size)
        self.surface.fill(self.background_color)

    def reset(
        self,
        screen_size: ScreenSize = (600, 600),
        background_color: Color = (255, 255, 255)
    ) -> None:
        """
        Remake the canvas with new parameters.
        
        Args:
            screen_size: Window dimensions as (width, height)
            background_color: RGB color tuple, e.g. (255, 255, 255)
        """
        self.background_color = background_color
        self.screen_size = screen_size
        self.surface = pygame.display.set_mode(screen_size)
        self.surface.fill(background_color)


class Engine:
    """
    The Engine class creates your EasyPygame window and handles runtime events.
    """
    
    game_title: str
    clock: pygame.time.Clock
    fps: int
    canvas: Canvas

    def __init__(
        self,
        game_title: str = "EasyPygame Window",
        fps: int = 60,
        canvas: Canvas | None = None
    ) -> None:
        pygame.init()
        self.game_title = game_title
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.canvas = canvas if canvas is not None else Canvas()
        pygame.display.set_caption(self.game_title)

    def await_closure(self) -> None:
        """Check if user input any commands to close the window."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

    def game_loop(self, func: F) -> F:
        """
        Decorator that handles the game loop at runtime.
        
        The decorated function will be called repeatedly each frame.
        
        Args:
            func: The game logic function to run each frame
            
        Returns:
            The decorated function (runs the game loop)
        """
        while True:
            self.await_closure()
            func()
            pygame.display.update()
            self.canvas.surface.fill(self.canvas.background_color)
            self.clock.tick(self.fps)
