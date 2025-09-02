#!/usr/bin/env python3
"""
Quick visual test of the Gyruss demo - runs for 5 seconds then exits
"""
import sys
import time
import threading
import os

# Set environment for headless operation if needed
# os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Uncomment if no display available

from gyruss_demo import *

def main():
    """Run Gyruss demo for a short time"""
    print("Starting 5-second Gyruss Demo test...")
    print("Green square = player, Red circles = enemies, Yellow dots = projectiles")
    
    # Game setup
    canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 20))
    engine = Engine(fps=60, canvas=canvas, game_title="Gyruss Demo Test - EasyPygame")
    
    # Create player
    player = GyrusPlayer(canvas)
    
    # Game state
    projectiles = []
    enemies = []
    score = 0
    enemy_spawn_timer = 0
    enemy_spawn_interval = 60  # Spawn faster for demo
    frame_count = 0
    max_frames = 300  # 5 seconds at 60fps
    
    # Auto-exit timer
    def auto_exit():
        time.sleep(5)
        print("\n5-second test completed - auto-exiting")
        import pygame
        pygame.quit()
        sys.exit(0)
    
    timer = threading.Thread(target=auto_exit, daemon=True)
    timer.start()
    
    # Game loop
    @engine.game_loop
    def game_loop():
        nonlocal score, enemy_spawn_timer, frame_count
        
        frame_count += 1
        if frame_count > max_frames:
            print("\nMax frames reached - exiting")
            import pygame
            pygame.quit()
            sys.exit(0)
        
        # Simulate player movement and shooting
        if frame_count % 60 == 0:  # Move every second
            player.angle += 0.3
            player.update_position(canvas)
        
        if frame_count % 30 == 0:  # Shoot twice per second
            direction = player.get_shot_trajectory()
            proj_x = player.box_collider.x + player.size // 2
            proj_y = player.box_collider.y + player.size // 2
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
        
        # Check collisions
        for projectile in projectiles[:]:
            for enemy in enemies[:]:
                if projectile.check_collision([enemy]):
                    projectiles.remove(projectile)
                    enemies.remove(enemy)
                    score += 10
                    print(f"Hit! Score: {score}")
                    break
        
        # Draw all objects
        player.draw(engine.canvas.surface)
        
        for projectile in projectiles:
            projectile.draw(engine.canvas.surface)
            
        for enemy in enemies:
            enemy.draw(engine.canvas.surface)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nDemo interrupted")
    except Exception as e:
        print(f"Demo error: {e}")
    finally:
        import pygame
        pygame.quit()
        print("Demo ended")