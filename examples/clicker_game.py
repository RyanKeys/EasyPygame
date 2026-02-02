#!/usr/bin/env python3
"""
Clicker Game Example
====================
Click on targets to score points! Demonstrates mouse input with EasyPygame.

Controls:
- Left click on targets to score
- ESC to quit
"""

import random
from EasyPygame import Character, Engine, Canvas, MouseController

# Game settings
SCREEN_SIZE = (800, 600)
TARGET_SIZE = 50
FPS = 60

# Initialize game
canvas = Canvas(screen_size=SCREEN_SIZE, background_color=(30, 30, 40))
engine = Engine(game_title="Clicker Game", fps=FPS, canvas=canvas)
mouse = MouseController()

# Game state
score = 0
targets: list[Character] = []
click_cooldown = 0


def spawn_target() -> Character:
    """Spawn a target at a random position."""
    x = random.randint(TARGET_SIZE, SCREEN_SIZE[0] - TARGET_SIZE)
    y = random.randint(TARGET_SIZE, SCREEN_SIZE[1] - TARGET_SIZE)
    target = Character(spawn_coordinates=(x, y), size=TARGET_SIZE)
    # Give it a random color
    color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
    target.image.fill(color)
    return target


def draw_score(surface) -> None:
    """Draw the score on screen."""
    import pygame
    font = pygame.font.Font(None, 48)
    text = font.render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(text, (10, 10))


# Spawn initial targets
for _ in range(5):
    targets.append(spawn_target())


@engine.game_loop
def game_loop():
    global score, click_cooldown
    
    # Reduce click cooldown
    if click_cooldown > 0:
        click_cooldown -= 1
    
    # Check for clicks on targets
    if mouse.is_left_pressed() and click_cooldown == 0:
        for target in targets[:]:  # Copy list to allow removal during iteration
            if mouse.is_clicking(target):
                targets.remove(target)
                targets.append(spawn_target())
                score += 1
                click_cooldown = 10  # Prevent multiple clicks per frame
                break
    
    # Draw all targets
    for target in targets:
        # Highlight if mouse is over
        if mouse.is_over(target):
            import pygame
            pygame.draw.rect(
                engine.canvas.surface,
                (255, 255, 0),
                target.box_collider.inflate(6, 6),
                3
            )
        target.draw(engine.canvas.surface)
    
    # Draw score
    draw_score(engine.canvas.surface)
