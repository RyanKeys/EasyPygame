#!/usr/bin/env python3
"""
Shooter Demo
============
Move with WASD, aim and shoot with mouse. Demonstrates combining keyboard
and mouse input with EasyPygame.

Controls:
- WASD to move
- Mouse to aim
- Left click to shoot
- ESC to quit
"""

import math
from EasyPygame import Player, Character, Engine, Canvas, MouseController

# Game settings
SCREEN_SIZE = (800, 600)
FPS = 60
BULLET_SPEED = 15

# Initialize game
canvas = Canvas(screen_size=SCREEN_SIZE, background_color=(20, 20, 30))
engine = Engine(game_title="Shooter Demo", fps=FPS, canvas=canvas)
mouse = MouseController()

# Create player in center
player = Player(
    spawn_coordinates=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2),
    size=40
)
player.image.fill((0, 200, 100))  # Green player

# Bullets list
bullets: list[dict] = []
shoot_cooldown = 0


def shoot_bullet(start_x: int, start_y: int, target_x: int, target_y: int) -> dict:
    """Create a bullet moving toward the target position."""
    # Calculate direction
    dx = target_x - start_x
    dy = target_y - start_y
    distance = math.sqrt(dx * dx + dy * dy)
    
    if distance == 0:
        return None
    
    # Normalize and scale by speed
    vx = (dx / distance) * BULLET_SPEED
    vy = (dy / distance) * BULLET_SPEED
    
    return {
        'x': float(start_x),
        'y': float(start_y),
        'vx': vx,
        'vy': vy,
        'size': 8
    }


def draw_bullet(surface, bullet: dict) -> None:
    """Draw a bullet on the surface."""
    import pygame
    pygame.draw.circle(
        surface,
        (255, 255, 0),
        (int(bullet['x']), int(bullet['y'])),
        bullet['size']
    )


def draw_crosshair(surface) -> None:
    """Draw a crosshair at mouse position."""
    import pygame
    mx, my = mouse.get_position()
    color = (255, 100, 100)
    pygame.draw.line(surface, color, (mx - 10, my), (mx + 10, my), 2)
    pygame.draw.line(surface, color, (mx, my - 10), (mx, my + 10), 2)


def draw_info(surface) -> None:
    """Draw control info."""
    import pygame
    font = pygame.font.Font(None, 28)
    text = font.render("WASD: Move | Click: Shoot | ESC: Quit", True, (150, 150, 150))
    surface.blit(text, (10, SCREEN_SIZE[1] - 35))
    
    bullet_count = font.render(f"Bullets: {len(bullets)}", True, (255, 255, 255))
    surface.blit(bullet_count, (10, 10))


@engine.game_loop
def game_loop():
    global shoot_cooldown
    
    # Handle player movement
    player.handle_keys(canvas)
    
    # Shooting cooldown
    if shoot_cooldown > 0:
        shoot_cooldown -= 1
    
    # Shoot on click
    if mouse.is_left_pressed() and shoot_cooldown == 0:
        mx, my = mouse.get_position()
        # Shoot from player center
        px = player.box_collider.centerx
        py = player.box_collider.centery
        bullet = shoot_bullet(px, py, mx, my)
        if bullet:
            bullets.append(bullet)
            shoot_cooldown = 10
    
    # Update bullets
    for bullet in bullets[:]:
        bullet['x'] += bullet['vx']
        bullet['y'] += bullet['vy']
        
        # Remove bullets that go off screen
        if (bullet['x'] < 0 or bullet['x'] > SCREEN_SIZE[0] or
            bullet['y'] < 0 or bullet['y'] > SCREEN_SIZE[1]):
            bullets.remove(bullet)
    
    # Draw everything
    player.draw(engine.canvas.surface)
    
    for bullet in bullets:
        draw_bullet(engine.canvas.surface, bullet)
    
    draw_crosshair(engine.canvas.surface)
    draw_info(engine.canvas.surface)
