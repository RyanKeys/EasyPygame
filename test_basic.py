#!/usr/bin/env python3
"""
Simple test script to verify EasyPygame functionality without external sprites.
This test runs for 3 seconds then exits automatically.
"""
import sys
import time
import threading
from EasyPygame.actors import Player, Character
from EasyPygame.game_engine import Engine, Canvas

def test_easypygame():
    """Test basic EasyPygame functionality"""
    print("Testing EasyPygame...")
    
    # Initialization of all game related objects
    canvas = Canvas(screen_size=(400, 400), background_color=(0, 0, 0))
    engine = Engine(fps=60, canvas=canvas)
    
    # Create player and character without sprite (will use default colored square)
    player = Player(spawn_coordinates=(engine.canvas.screen_size[0]//2, engine.canvas.screen_size[1]-20), size=50)
    character = Character(spawn_coordinates=(engine.canvas.screen_size[0]//2, 0), size=50)  # No sprite = default colored square
    
    char_list = [player, character]
    
    # Set up auto-exit after 3 seconds
    def auto_exit():
        time.sleep(3)
        print("Test completed - auto-exiting")
        import pygame
        pygame.quit()
        sys.exit(0)
    
    # Start auto-exit timer
    timer = threading.Thread(target=auto_exit, daemon=True)
    timer.start()
    
    # Game loop
    @engine.game_loop
    def loop():
        for actor in char_list:
            actor.draw(engine.canvas.surface)
            if type(actor) == Player:
                actor.handle_keys(canvas=engine.canvas)
            if player.check_collision([character]) and character in char_list:
                char_list.remove(character)
                print("Collision detected and character removed!")

if __name__ == "__main__":
    try:
        test_easypygame()
    except KeyboardInterrupt:
        print("Test interrupted by user")
        import pygame
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"Test failed with error: {e}")
        import pygame
        pygame.quit()
        sys.exit(1)