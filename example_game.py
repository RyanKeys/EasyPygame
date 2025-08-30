#!/usr/bin/env python3
"""
EasyPygame Example: Simple Game Demo
=====================================

This example demonstrates how to create a simple game using EasyPygame.
The game features:
- A player (green square) controlled with WASD keys
- An enemy character (purple square) 
- Collision detection between player and enemy
- When they collide, the enemy disappears

Controls:
- W: Move up
- A: Move left  
- S: Move down
- D: Move right
- ESC or close window: Exit game

Note: This example will run in an actual window when executed.
"""

from EasyPygame import Player, Character, Engine, Canvas

def main():
    """Main game function"""
    print("Starting EasyPygame Demo...")
    print("Use WASD to move the green player square")
    print("Collide with the purple enemy to make it disappear")
    print("Press ESC or close window to exit")
    
    # Game setup
    canvas = Canvas(screen_size=(800, 600), background_color=(50, 50, 50))
    engine = Engine(fps=60, canvas=canvas, game_title="EasyPygame Demo")
    
    # Create game objects
    player = Player(spawn_coordinates=(100, 300), size=40)
    enemy = Character(spawn_coordinates=(700, 300), size=40)
    
    # Give player a green color
    player.image.fill((0, 255, 0))  # Green
    # Enemy already has purple color by default
    
    game_objects = [player, enemy]
    
    # Game loop
    @engine.game_loop
    def game_loop():
        # Draw all objects
        for obj in game_objects[:]:  # Use slice copy to safely modify during iteration
            obj.draw(engine.canvas.surface)
            
            # Handle player input
            if isinstance(obj, Player):
                obj.handle_keys(canvas=engine.canvas)
        
        # Check collisions
        if enemy in game_objects and player.check_collision([enemy]):
            game_objects.remove(enemy)
            print("Enemy defeated! Collision detected.")

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