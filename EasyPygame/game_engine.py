import sys
import pygame


class Canvas:

    def __init__(self, screen_size = (600,600), background_color = (255,255,255)):
        self.screen_size = screen_size
        self.background_color = background_color
        self.surface = pygame.display.set_mode(self.screen_size)
        self.surface.fill(self.background_color)

    def reset(self, screen_size = (600,600), background_color = (255,255,255)):
        """
        Remakes the canvas with the desired parameters:
        
        screen_size Type: Tuple
        Example: (200,200)

        background_color Type: Tuple
        Example: (255,255,255)
        
        """
        self.background_color = background_color
        self.screen_size = screen_size
        self.surface = pygame.display.set_mode(screen_size)
        self.surface.fill(background_color)



class Engine:
    """
    The Engine class creates your EzPygame window, and handles runtime events. 
    """
    def __init__(self, game_title="EzPygame Window", fps=60, canvas=Canvas()):
        pygame.init()
        self.game_title = game_title
        self.clock = pygame.time.Clock() # The clock will be used to control how fast the screen updates
        self.fps = fps
        self.canvas = canvas
        pygame.display.set_caption(self.game_title)

    def await_closure(self):
        """Checks if user input any commands to close the window."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                running = False
                break

    def game_loop(self, func):
        """
        Handles the game on runtime. Must come before your gameplay code. Whatever comes below this will happen inside your created game window.
        """
        while True:
            self.await_closure()
            func()
            pygame.display.update()
            self.canvas.surface.fill(self.canvas.background_color)
            self.clock.tick(self.fps)