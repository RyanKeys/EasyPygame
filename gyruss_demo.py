#!/usr/bin/env python3
"""
EasyPygame Gyruss Demo
======================

A classic Gyruss-style arcade game implementation using EasyPygame framework.

Controls:
- A: Move counterclockwise around the perimeter
- D: Move clockwise around the perimeter  
- W or SPACE: Fire projectile toward center
- R: Restart (when game over)
- ESC or close window: Exit game
"""

import pygame
import math
import random
import time
from EasyPygame import Character, Engine, Canvas
from EasyPygame.input_controller import KeyboardController


# Screen center - bullets aim here
SCREEN_CENTER = (400, 300)


class Bullet:
    """Simple bullet that travels in a straight line."""
    
    def __init__(self, start_x: float, start_y: float, target_x: float, target_y: float, speed: float = 12):
        # Store start position for debug drawing
        self.start_x = start_x
        self.start_y = start_y
        
        # Current position (floats for precision)
        self.x = start_x
        self.y = start_y
        
        # Calculate direction ONCE (normalized vector toward target)
        dx = target_x - start_x
        dy = target_y - start_y
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            self.vx = (dx / dist) * speed
            self.vy = (dy / dist) * speed
        else:
            self.vx = 0
            self.vy = -speed  # Default: shoot up
        
        # Store velocity for debug (should NEVER change)
        self.debug_vx = self.vx
        self.debug_vy = self.vy
        
        # Track path for debug visualization
        self.path = [(start_x, start_y)]
        
        self.alive = True
        self.radius = 4
    
    def update(self):
        """Move bullet in straight line."""
        # ONLY these two lines affect position
        self.x += self.vx
        self.y += self.vy
        
        # Track path
        self.path.append((self.x, self.y))
        
        # Die if reached center
        dist_to_center = math.sqrt((self.x - SCREEN_CENTER[0])**2 + (self.y - SCREEN_CENTER[1])**2)
        if dist_to_center < 15:
            self.alive = False
        
        # Die if off screen
        if self.x < -50 or self.x > 850 or self.y < -50 or self.y > 650:
            self.alive = False
    
    def draw(self, surface):
        """Draw bullet and its path."""
        # Draw path trail (should be perfectly straight)
        if len(self.path) > 1:
            pygame.draw.lines(surface, (100, 100, 0), False, 
                            [(int(p[0]), int(p[1])) for p in self.path], 1)
        
        # Draw line from start to current (should be straight)
        pygame.draw.line(surface, (0, 100, 100), 
                        (int(self.start_x), int(self.start_y)),
                        (int(self.x), int(self.y)), 1)
        
        # Draw bullet
        pygame.draw.circle(surface, (255, 255, 0), (int(self.x), int(self.y)), self.radius)
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rect."""
        return pygame.Rect(int(self.x) - self.radius, int(self.y) - self.radius, 
                          self.radius * 2, self.radius * 2)


class Enemy:
    """Enemy that spirals outward from center."""
    
    def __init__(self):
        self.angle = random.uniform(0, 2 * math.pi)
        self.radius = 20  # Distance from center
        self.spiral_speed = 1.0
        self.rotation_speed = 0.025
        self.size = 16
        self.alive = True
    
    def update(self):
        """Spiral outward."""
        self.radius += self.spiral_speed
        self.angle += self.rotation_speed
        
        if self.radius > 350:
            self.alive = False
    
    @property
    def x(self) -> float:
        return SCREEN_CENTER[0] + self.radius * math.cos(self.angle)
    
    @property
    def y(self) -> float:
        return SCREEN_CENTER[1] + self.radius * math.sin(self.angle)
    
    def draw(self, surface):
        """Draw enemy."""
        pygame.draw.circle(surface, (255, 50, 50), (int(self.x), int(self.y)), self.size)
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rect."""
        return pygame.Rect(int(self.x) - self.size, int(self.y) - self.size,
                          self.size * 2, self.size * 2)


class Player:
    """Player that moves around the perimeter."""
    
    def __init__(self):
        self.angle = math.pi / 2  # Start at bottom
        self.orbit_radius = 250
        self.speed = 0.05
        self.size = 15
    
    @property
    def x(self) -> float:
        return SCREEN_CENTER[0] + self.orbit_radius * math.cos(self.angle)
    
    @property
    def y(self) -> float:
        return SCREEN_CENTER[1] + self.orbit_radius * math.sin(self.angle)
    
    def update(self, keys):
        """Handle movement."""
        if keys[pygame.K_a]:
            self.angle -= self.speed
        if keys[pygame.K_d]:
            self.angle += self.speed
    
    def draw(self, surface):
        """Draw player."""
        pygame.draw.circle(surface, (0, 255, 100), (int(self.x), int(self.y)), self.size)
    
    def get_rect(self) -> pygame.Rect:
        """Get collision rect."""
        return pygame.Rect(int(self.x) - self.size, int(self.y) - self.size,
                          self.size * 2, self.size * 2)


def check_collision(rect1: pygame.Rect, rect2: pygame.Rect) -> bool:
    """Check if two rects collide."""
    return rect1.colliderect(rect2)


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Gyruss Demo - EasyPygame")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 64)
    
    player = Player()
    bullets: list[Bullet] = []
    enemies: list[Enemy] = []
    
    score = 0
    spawn_timer = 0
    game_over = False
    last_shot = 0
    shot_cooldown = 1.0
    
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        keys = pygame.key.get_pressed()
        
        if game_over:
            if keys[pygame.K_r]:
                # Reset
                player = Player()
                bullets = []
                enemies = []
                score = 0
                spawn_timer = 0
                game_over = False
        else:
            # Update player
            player.update(keys)
            
            # Shooting
            now = time.time()
            if (keys[pygame.K_w] or keys[pygame.K_SPACE]) and now - last_shot > shot_cooldown:
                last_shot = now
                # Fire bullet from player toward center
                bullets.append(Bullet(player.x, player.y, SCREEN_CENTER[0], SCREEN_CENTER[1]))
            
            # Update bullets
            for bullet in bullets:
                bullet.update()
            bullets = [b for b in bullets if b.alive]
            
            # Spawn enemies
            spawn_timer += 1
            if spawn_timer >= 60:
                spawn_timer = 0
                enemies.append(Enemy())
            
            # Update enemies
            for enemy in enemies:
                enemy.update()
            enemies = [e for e in enemies if e.alive]
            
            # Bullet-enemy collision
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if check_collision(bullet.get_rect(), enemy.get_rect()):
                        bullet.alive = False
                        enemy.alive = False
                        score += 10
            bullets = [b for b in bullets if b.alive]
            enemies = [e for e in enemies if e.alive]
            
            # Player-enemy collision
            player_rect = player.get_rect()
            for enemy in enemies:
                if check_collision(player_rect, enemy.get_rect()):
                    game_over = True
        
        # Draw
        screen.fill((0, 0, 20))
        
        # Draw orbit circle (visual guide)
        pygame.draw.circle(screen, (30, 30, 50), SCREEN_CENTER, player.orbit_radius, 1)
        
        # Draw center point
        pygame.draw.circle(screen, (50, 50, 80), SCREEN_CENTER, 5)
        
        # Draw game objects
        for enemy in enemies:
            enemy.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        player.draw(screen)
        
        # Draw UI
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        if game_over:
            # Overlay
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            title = font_large.render("GAME OVER", True, (255, 80, 80))
            screen.blit(title, (400 - title.get_width() // 2, 240))
            
            final = font.render(f"Final Score: {score}", True, (255, 255, 255))
            screen.blit(final, (400 - final.get_width() // 2, 320))
            
            restart = font.render("Press R to restart", True, (150, 150, 150))
            screen.blit(restart, (400 - restart.get_width() // 2, 380))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    main()
