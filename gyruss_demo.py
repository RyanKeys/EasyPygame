#!/usr/bin/env python3
"""
EasyPygame Gyruss Demo
======================

A classic Gyruss-style arcade game implementation using EasyPygame framework.

Gyruss is a shoot-em-up game where the player controls a ship that moves around
the perimeter of a circular playing field, shooting at enemies that spiral
outward from the center.

Features:
- Player ship that moves around the screen perimeter in a circle
- Enemies that spiral outward from the center
- Projectile shooting system with radial trajectory
- Collision detection between projectiles and enemies
- Player-enemy collision (game over)
- Score tracking with on-screen display
- Classic arcade-style gameplay

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


class GyrusController(KeyboardController):
    """Custom controller for Gyruss-style circular movement and shooting"""
    
    def __init__(self, movement_speed=0.05):
        self.angular_speed = movement_speed
        self.last_shot_time = 0
        self.shot_cooldown = 0.2
    
    def handle_keys(self, player, canvas):
        """Handle circular movement and shooting"""
        key = pygame.key.get_pressed()
        current_time = time.time()
        
        # Circular movement around perimeter
        if key[pygame.K_a]:
            player.angle -= self.angular_speed
        if key[pygame.K_d]:
            player.angle += self.angular_speed
            
        # Keep angle in [0, 2π] range
        player.angle = player.angle % (2 * math.pi)
        
        # Update player position based on angle
        player.update_position(canvas)
        
        # Shooting
        can_shoot = current_time - self.last_shot_time > self.shot_cooldown
        if (key[pygame.K_w] or key[pygame.K_SPACE]) and can_shoot:
            self.last_shot_time = current_time
            return "shoot"
        
        return None


class GyrusPlayer(Character):
    """Player ship that moves around the screen perimeter"""
    
    def __init__(self, canvas):
        self.angle = math.pi / 2  # Start at bottom
        self.radius = min(canvas.screen_size[0], canvas.screen_size[1]) // 2 - 30
        self.center_x = canvas.screen_size[0] // 2
        self.center_y = canvas.screen_size[1] // 2
        
        # Calculate initial position
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        
        super().__init__(spawn_coordinates=(int(x) - 10, int(y) - 10), size=20)
        self.image.fill((0, 255, 0))
        self.controller = GyrusController()
    
    def update_position(self, canvas):
        """Update position based on current angle"""
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        self.box_collider.centerx = int(x)
        self.box_collider.centery = int(y)
    
    def handle_keys(self, canvas):
        return self.controller.handle_keys(self, canvas)
    
    def get_shot_trajectory(self):
        """Calculate direction vector for shooting toward center"""
        dx = self.center_x - self.box_collider.centerx
        dy = self.center_y - self.box_collider.centery
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            return (dx / distance, dy / distance)
        return (0, 0)
    
    def reset(self, canvas):
        """Reset player to starting position"""
        self.angle = math.pi / 2
        self.update_position(canvas)


class Projectile(Character):
    """Projectile fired by the player toward the center"""
    
    def __init__(self, start_x, start_y, direction_x, direction_y, speed=10):
        super().__init__(spawn_coordinates=(int(start_x), int(start_y)), size=6)
        self.image.fill((255, 255, 0))
        
        # Track float position for smooth movement
        self.float_x = float(start_x)
        self.float_y = float(start_y)
        self.velocity_x = direction_x * speed
        self.velocity_y = direction_y * speed
        self.lifetime = 60
    
    def update(self, canvas):
        """Update projectile position using float coordinates"""
        # Update float position
        self.float_x += self.velocity_x
        self.float_y += self.velocity_y
        
        # Sync to box_collider
        self.box_collider.centerx = int(self.float_x)
        self.box_collider.centery = int(self.float_y)
        
        self.lifetime -= 1
        
        # Remove if out of bounds or lifetime expired
        if (self.lifetime <= 0 or 
            self.box_collider.right < 0 or self.box_collider.left > canvas.screen_size[0] or
            self.box_collider.bottom < 0 or self.box_collider.top > canvas.screen_size[1]):
            return False
        return True


class Enemy(Character):
    """Enemy that spirals outward from the center"""
    
    def __init__(self, canvas, spawn_angle=None):
        self.center_x = canvas.screen_size[0] // 2
        self.center_y = canvas.screen_size[1] // 2
        
        self.angle = spawn_angle if spawn_angle is not None else random.uniform(0, 2 * math.pi)
        self.radius = 10
        self.spiral_speed = 1.2
        self.angular_speed = 0.03
        
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        
        super().__init__(spawn_coordinates=(int(x), int(y)), size=18)
        self.image.fill((255, 50, 50))
        
        self.max_radius = min(canvas.screen_size[0], canvas.screen_size[1]) // 2 + 20
    
    def update(self, canvas):
        """Update enemy position in spiral pattern"""
        self.radius += self.spiral_speed
        self.angle += self.angular_speed
        
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        self.box_collider.centerx = int(x)
        self.box_collider.centery = int(y)
        
        if self.radius > self.max_radius:
            return False
        return True


def draw_ui(surface, score, font):
    """Draw score on screen"""
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    surface.blit(score_text, (10, 10))


def draw_game_over(surface, score, font_large, font_small):
    """Draw game over screen"""
    overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    cx, cy = surface.get_width() // 2, surface.get_height() // 2
    
    title = font_large.render("GAME OVER", True, (255, 80, 80))
    surface.blit(title, (cx - title.get_width() // 2, cy - 60))
    
    score_text = font_small.render(f"Final Score: {score}", True, (255, 255, 255))
    surface.blit(score_text, (cx - score_text.get_width() // 2, cy))
    
    restart = font_small.render("Press R to restart", True, (180, 180, 180))
    surface.blit(restart, (cx - restart.get_width() // 2, cy + 50))


def main():
    """Main Gyruss game function"""
    print("Gyruss Demo - EasyPygame")
    print("A/D: Move around perimeter")
    print("W/SPACE: Shoot toward center")
    print("Avoid the red enemies!")
    
    canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 20))
    engine = Engine(fps=60, canvas=canvas, game_title="Gyruss Demo - EasyPygame")
    
    # Fonts
    font = pygame.font.Font(None, 36)
    font_large = pygame.font.Font(None, 64)
    
    # Game objects
    player = GyrusPlayer(canvas)
    projectiles = []
    enemies = []
    
    # Game state
    score = 0
    enemy_spawn_timer = 0
    enemy_spawn_interval = 75
    game_over = False
    
    @engine.game_loop
    def game_loop():
        nonlocal score, enemy_spawn_timer, game_over, projectiles, enemies
        
        keys = pygame.key.get_pressed()
        
        if game_over:
            if keys[pygame.K_r]:
                # Reset game
                score = 0
                enemy_spawn_timer = 0
                game_over = False
                projectiles = []
                enemies = []
                player.reset(canvas)
        else:
            # Player input
            action = player.handle_keys(canvas)
            if action == "shoot":
                direction = player.get_shot_trajectory()
                proj_x = player.box_collider.centerx
                proj_y = player.box_collider.centery
                projectiles.append(Projectile(proj_x, proj_y, direction[0], direction[1]))
            
            # Update projectiles
            for projectile in projectiles[:]:
                if not projectile.update(canvas):
                    projectiles.remove(projectile)
            
            # Spawn enemies
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= enemy_spawn_interval:
                enemy_spawn_timer = 0
                enemies.append(Enemy(canvas))
            
            # Update enemies
            for enemy in enemies[:]:
                if not enemy.update(canvas):
                    enemies.remove(enemy)
            
            # Check projectile-enemy collisions
            for projectile in projectiles[:]:
                for enemy in enemies[:]:
                    if projectile.check_collision([enemy]):
                        if projectile in projectiles:
                            projectiles.remove(projectile)
                        if enemy in enemies:
                            enemies.remove(enemy)
                        score += 10
                        break
            
            # Check player-enemy collision (game over)
            if player.check_collision(enemies):
                game_over = True
        
        # Draw everything
        player.draw(canvas.surface)
        
        for projectile in projectiles:
            projectile.draw(canvas.surface)
        
        for enemy in enemies:
            enemy.draw(canvas.surface)
        
        draw_ui(canvas.surface, score, font)
        
        if game_over:
            draw_game_over(canvas.surface, score, font_large, font)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted")
    finally:
        pygame.quit()
