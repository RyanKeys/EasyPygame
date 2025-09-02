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
- Score tracking
- Classic arcade-style gameplay

Controls:
- A: Move counterclockwise around the perimeter
- D: Move clockwise around the perimeter  
- W or SPACE: Fire projectile toward center
- ESC or close window: Exit game

This demo showcases the EasyPygame framework's capabilities for creating
classic arcade-style games with circular movement and trigonometric calculations.
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
        # Movement speed is in radians per frame for angular movement
        self.angular_speed = movement_speed
        self.shoot_key_pressed = False
        self.last_shot_time = 0
        self.shot_cooldown = 0.2  # Seconds between shots
    
    def handle_keys(self, player, canvas):
        """Handle circular movement and shooting"""
        key = pygame.key.get_pressed()
        current_time = time.time()
        
        # Circular movement around perimeter
        if key[pygame.K_a]:  # Move counterclockwise
            player.angle -= self.angular_speed
        if key[pygame.K_d]:  # Move clockwise  
            player.angle += self.angular_speed
            
        # Keep angle in [0, 2π] range
        if player.angle < 0:
            player.angle += 2 * math.pi
        elif player.angle >= 2 * math.pi:
            player.angle -= 2 * math.pi
        
        # Update player position based on angle
        player.update_position(canvas)
        
        # Shooting
        can_shoot = current_time - self.last_shot_time > self.shot_cooldown
        if (key[pygame.K_w] or key[pygame.K_SPACE]) and can_shoot:
            self.last_shot_time = current_time
            return "shoot"  # Signal to create projectile
        
        return None


class GyrusPlayer(Character):
    """Player ship that moves around the screen perimeter"""
    
    def __init__(self, canvas):
        # Start at the bottom of the circle (angle = π/2)
        self.angle = math.pi / 2
        self.radius = min(canvas.screen_size[0], canvas.screen_size[1]) // 2 - 30
        self.center_x = canvas.screen_size[0] // 2
        self.center_y = canvas.screen_size[1] // 2
        
        # Calculate initial position (center of player)
        center_x = self.center_x + self.radius * math.cos(self.angle)
        center_y = self.center_y + self.radius * math.sin(self.angle)
        
        # Convert to top-left corner for spawn_coordinates
        top_left_x = int(center_x) - 10  # size=20, so size//2 = 10
        top_left_y = int(center_y) - 10
        
        super().__init__(spawn_coordinates=(top_left_x, top_left_y), size=20)
        
        # Player should be bright green
        self.image.fill((0, 255, 0))
        
        # Custom controller
        self.controller = GyrusController()
    
    def update_position(self, canvas):
        """Update position based on current angle"""
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        self.box_collider.x = int(x) - self.size // 2
        self.box_collider.y = int(y) - self.size // 2
    
    def handle_keys(self, canvas):
        """Handle player input and return action"""
        return self.controller.handle_keys(self, canvas)
    
    def get_shot_trajectory(self):
        """Calculate the direction vector for shooting toward center"""
        # Direction from player to center (normalized)
        dx = self.center_x - (self.box_collider.x + self.size // 2)
        dy = self.center_y - (self.box_collider.y + self.size // 2)
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance > 0:
            return (dx / distance, dy / distance)
        return (0, 0)


class Projectile(Character):
    """Projectile fired by the player toward the center"""
    
    def __init__(self, start_x, start_y, direction_x, direction_y, speed=8):
        super().__init__(spawn_coordinates=(start_x, start_y), size=6)
        
        # Projectile should be bright yellow
        self.image.fill((255, 255, 0))
        
        self.velocity_x = direction_x * speed
        self.velocity_y = direction_y * speed
        self.lifetime = 60  # Remove after 60 frames if no collision
    
    def update(self, canvas):
        """Update projectile position"""
        self.box_collider.x += self.velocity_x
        self.box_collider.y += self.velocity_y
        self.lifetime -= 1
        
        # Remove if out of bounds or lifetime expired
        if (self.lifetime <= 0 or 
            self.box_collider.x < 0 or self.box_collider.x > canvas.screen_size[0] or
            self.box_collider.y < 0 or self.box_collider.y > canvas.screen_size[1]):
            return False  # Signal for removal
        return True


class Enemy(Character):
    """Enemy that spirals outward from the center"""
    
    def __init__(self, canvas, spawn_angle=None):
        self.center_x = canvas.screen_size[0] // 2
        self.center_y = canvas.screen_size[1] // 2
        
        # Start from center with random or specified angle
        self.angle = spawn_angle if spawn_angle is not None else random.uniform(0, 2 * math.pi)
        self.radius = 10  # Start near center
        self.spiral_speed = 0.8  # How fast it moves outward
        self.angular_speed = 0.02  # How fast it rotates
        
        # Calculate initial position
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        
        super().__init__(spawn_coordinates=(int(x), int(y)), size=15)
        
        # Enemy should be red
        self.image.fill((255, 0, 0))
        
        self.max_radius = min(canvas.screen_size[0], canvas.screen_size[1]) // 2
    
    def update(self, canvas):
        """Update enemy position in spiral pattern"""
        # Move outward and rotate
        self.radius += self.spiral_speed
        self.angle += self.angular_speed
        
        # Calculate new position
        x = self.center_x + self.radius * math.cos(self.angle)
        y = self.center_y + self.radius * math.sin(self.angle)
        self.box_collider.x = int(x) - self.size // 2
        self.box_collider.y = int(y) - self.size // 2
        
        # Remove if reached edge
        if self.radius > self.max_radius:
            return False  # Signal for removal
        return True


def main():
    """Main Gyruss game function"""
    print("Starting Gyruss Demo...")
    print("Use A/D to move around the perimeter")
    print("Use W or SPACE to shoot")
    print("Destroy the red enemies spiraling from the center!")
    print("Press ESC or close window to exit")
    
    # Game setup
    canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 20))  # Dark blue space
    engine = Engine(fps=60, canvas=canvas, game_title="Gyruss Demo - EasyPygame")
    
    # Create player
    player = GyrusPlayer(canvas)
    
    # Game state
    projectiles = []
    enemies = []
    score = 0
    enemy_spawn_timer = 0
    enemy_spawn_interval = 90  # Spawn enemy every 90 frames (1.5 seconds at 60fps)
    
    # Game loop
    @engine.game_loop
    def game_loop():
        nonlocal score, enemy_spawn_timer
        
        # Handle player input
        action = player.handle_keys(canvas)
        if action == "shoot":
            # Create projectile
            direction = player.get_shot_trajectory()
            proj_x = player.box_collider.x + player.size // 2
            proj_y = player.box_collider.y + player.size // 2
            projectiles.append(Projectile(proj_x, proj_y, direction[0], direction[1]))
        
        # Update projectiles
        for projectile in projectiles[:]:  # Use slice copy for safe removal
            if not projectile.update(canvas):
                projectiles.remove(projectile)
        
        # Spawn enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= enemy_spawn_interval:
            enemy_spawn_timer = 0
            enemies.append(Enemy(canvas))
        
        # Update enemies
        for enemy in enemies[:]:  # Use slice copy for safe removal
            if not enemy.update(canvas):
                enemies.remove(enemy)
        
        # Check collisions between projectiles and enemies
        for projectile in projectiles[:]:
            for enemy in enemies[:]:
                if projectile.check_collision([enemy]):
                    # Hit! Remove both and increase score
                    projectiles.remove(projectile)
                    enemies.remove(enemy)
                    score += 10
                    print(f"Enemy destroyed! Score: {score}")
                    break
        
        # Draw all objects
        player.draw(engine.canvas.surface)
        
        for projectile in projectiles:
            projectile.draw(engine.canvas.surface)
            
        for enemy in enemies:
            enemy.draw(engine.canvas.surface)
        
        # Draw score (simple text rendering)
        # Note: For simplicity, score is printed to console rather than drawn on screen
        # In a full implementation, you'd use pygame.font to render text


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"Game error: {e}")
    finally:
        import pygame
        pygame.quit()
        print("Game ended")