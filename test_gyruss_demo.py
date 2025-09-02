#!/usr/bin/env python3
"""
Quick test script to verify Gyruss demo functionality without opening window.
This test runs for a few iterations then exits automatically.
"""
import sys
import time
import math
import os

# Set dummy audio driver to suppress ALSA warnings
os.environ['SDL_AUDIODRIVER'] = 'dummy'

from gyruss_demo import GyrusPlayer, Enemy, Projectile, GyrusController
from EasyPygame import Canvas
import pygame

def test_gyruss_demo():
    """Test basic Gyruss demo functionality"""
    print("Testing Gyruss Demo mechanics...")
    
    pygame.init()
    
    # Initialize game objects
    canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 20))
    player = GyrusPlayer(canvas)
    
    projectiles = []
    enemies = []
    score = 0
    
    print(f"Player initial position: ({player.box_collider.x + player.size//2}, {player.box_collider.y + player.size//2})")
    print(f"Player initial angle: {player.angle:.3f} radians ({player.angle * 180 / math.pi:.1f} degrees)")
    
    # Test player movement
    original_angle = player.angle
    player.angle += 0.1  # Simulate movement
    player.update_position(canvas)
    print(f"After movement - angle: {player.angle:.3f}, position: ({player.box_collider.x + player.size//2}, {player.box_collider.y + player.size//2})")
    
    # Test projectile creation
    direction = player.get_shot_trajectory()
    proj_x = player.box_collider.x + player.size // 2
    proj_y = player.box_collider.y + player.size // 2
    projectile = Projectile(proj_x, proj_y, direction[0], direction[1])
    projectiles.append(projectile)
    print(f"Created projectile at ({projectile.box_collider.x}, {projectile.box_collider.y}) moving toward center")
    
    # Test enemy creation
    enemy = Enemy(canvas)
    enemies.append(enemy)
    print(f"Created enemy at center, radius: {enemy.radius}, angle: {enemy.angle:.3f}")
    
    # Simulate a few game iterations
    for i in range(5):
        print(f"\n--- Iteration {i+1} ---")
        
        # Update projectiles
        for proj in projectiles[:]:
            if not proj.update(canvas):
                projectiles.remove(proj)
                print("Projectile removed (lifetime or bounds)")
        
        # Update enemies  
        for enemy in enemies[:]:
            if not enemy.update(canvas):
                enemies.remove(enemy)
                print("Enemy removed (reached edge)")
            else:
                print(f"Enemy radius: {enemy.radius:.1f}, angle: {enemy.angle:.3f}")
        
        # Check collisions
        for projectile in projectiles[:]:
            for enemy in enemies[:]:
                if projectile.check_collision([enemy]):
                    projectiles.remove(projectile)
                    enemies.remove(enemy)
                    score += 10
                    print(f"HIT! Enemy destroyed, score: {score}")
                    break
        
        print(f"Active projectiles: {len(projectiles)}, enemies: {len(enemies)}")
    
    pygame.quit()
    print(f"\nTest completed successfully! Final score: {score}")
    return True

if __name__ == "__main__":
    try:
        test_gyruss_demo()
        print("✓ Gyruss demo test passed!")
    except Exception as e:
        print(f"✗ Gyruss demo test failed: {e}")
        sys.exit(1)