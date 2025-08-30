#!/usr/bin/env python3
"""
EasyPygame Pong Demo
====================

A classic Pong game implementation using EasyPygame framework.

Features:
- Player paddle controlled with W/S keys
- AI paddle that follows the ball
- Ball that bounces off paddles and walls
- Score tracking (displayed in console)
- Realistic Pong physics

Controls:
- W: Move player paddle up
- S: Move player paddle down  
- ESC or close window: Exit game

This demo showcases the EasyPygame framework's capabilities for creating
classic arcade-style games with minimal code.
"""

import pygame
import math
import random
from EasyPygame import Player, Character, Engine, Canvas
from EasyPygame.input_controller import KeyboardController


class Ball(Character):
    """A ball that moves and bounces around the screen"""
    
    def __init__(self, spawn_coordinates=(400, 300), size=15):
        super().__init__(spawn_coordinates, size)
        # Ball should be white
        self.image.fill((255, 255, 255))
        
        # Ball physics
        self.velocity_x = random.choice([-5, 5])  # Random starting direction
        self.velocity_y = random.choice([-3, 3])
        self.max_speed = 8
        
    def update(self, canvas):
        """Update ball position and handle wall bouncing"""
        # Move ball
        self.box_collider.x += self.velocity_x
        self.box_collider.y += self.velocity_y
        
        # Bounce off top and bottom walls
        if self.box_collider.y <= 0 or self.box_collider.y >= canvas.screen_size[1] - self.size:
            self.velocity_y = -self.velocity_y
            
        # Keep ball in bounds
        if self.box_collider.y < 0:
            self.box_collider.y = 0
        elif self.box_collider.y > canvas.screen_size[1] - self.size:
            self.box_collider.y = canvas.screen_size[1] - self.size
    
    def bounce_off_paddle(self, paddle):
        """Handle ball bouncing off a paddle"""
        # Calculate relative position where ball hit paddle (0.0 to 1.0)
        paddle_center = paddle.box_collider.y + paddle.size // 2
        ball_center = self.box_collider.y + self.size // 2
        relative_intersect = (ball_center - paddle_center) / (paddle.size // 2)
        
        # Reverse X direction
        self.velocity_x = -self.velocity_x
        
        # Adjust Y velocity based on where ball hit paddle
        self.velocity_y = relative_intersect * 5
        
        # Increase speed slightly on each hit (up to max)
        if abs(self.velocity_x) < self.max_speed:
            self.velocity_x = self.velocity_x * 1.05
    
    def reset(self, canvas):
        """Reset ball to center with random direction"""
        self.box_collider.x = canvas.screen_size[0] // 2 - self.size // 2
        self.box_collider.y = canvas.screen_size[1] // 2 - self.size // 2
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])


class Paddle(Character):
    """A paddle for Pong game"""
    
    def __init__(self, spawn_coordinates=(0, 250), width=15, height=80):
        super().__init__(spawn_coordinates, height)  # Use height as size for square
        self.width = width
        self.height = height
        
        # Create rectangular paddle surface
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))  # White paddle
        self.box_collider = self.image.get_rect()
        self.box_collider.x, self.box_collider.y = spawn_coordinates[0], spawn_coordinates[1]
        
        self.speed = 6
    
    def update(self, canvas):
        """Keep paddle within screen bounds"""
        if self.box_collider.y < 0:
            self.box_collider.y = 0
        elif self.box_collider.y > canvas.screen_size[1] - self.height:
            self.box_collider.y = canvas.screen_size[1] - self.height


class PongKeyboardController(KeyboardController):
    """Custom keyboard controller for Pong paddles (W/S keys only)"""
    
    def handle_keys(self, paddle, canvas):
        """Handle W/S keys for paddle movement"""
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and paddle.box_collider.y > 0:
            paddle.box_collider.y -= paddle.speed
        if key[pygame.K_s] and paddle.box_collider.y < canvas.screen_size[1] - paddle.height:
            paddle.box_collider.y += paddle.speed


class PongPlayer(Paddle):
    """Player-controlled paddle"""
    
    def __init__(self, spawn_coordinates=(0, 250)):
        super().__init__(spawn_coordinates)
        self.controller = PongKeyboardController()
    
    def handle_keys(self, canvas):
        """Handle player input"""
        self.controller.handle_keys(self, canvas)


class AIController:
    """Simple AI controller for computer paddle"""
    
    def __init__(self, difficulty=0.7):
        self.difficulty = difficulty  # 0.0 = easy, 1.0 = impossible
    
    def update(self, paddle, ball, canvas):
        """Move AI paddle toward ball with some imperfection"""
        ball_center = ball.box_collider.y + ball.size // 2
        paddle_center = paddle.box_collider.y + paddle.height // 2
        
        # Only react if ball is moving toward AI paddle
        if ball.velocity_x > 0:  # Ball moving right (toward AI)
            target_y = ball_center - paddle.height // 2
            
            # Add some AI difficulty (imperfection)
            if random.random() < self.difficulty:
                if paddle_center < ball_center:
                    paddle.box_collider.y += paddle.speed
                elif paddle_center > ball_center:
                    paddle.box_collider.y -= paddle.speed


def main():
    """Main Pong game function"""
    print("Starting EasyPygame Pong Demo...")
    print("Player 1 (Left): Use W/S keys to move")
    print("Player 2 (Right): AI controlled")
    print("First to 5 points wins!")
    print("Press ESC or close window to exit")
    
    # Game setup
    canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 0))
    engine = Engine(fps=60, canvas=canvas, game_title="EasyPygame Pong Demo")
    
    # Create game objects
    player_paddle = PongPlayer(spawn_coordinates=(50, 250))
    ai_paddle = Paddle(spawn_coordinates=(735, 250))
    ball = Ball(spawn_coordinates=(400, 300))
    
    # AI controller
    ai = AIController(difficulty=0.8)
    
    # Game state
    player_score = 0
    ai_score = 0
    max_score = 5
    game_over = False
    
    # Store original game loop method for ESC handling
    original_await_closure = engine.await_closure
    
    def custom_await_closure():
        """Custom event handler that includes ESC key"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                import sys
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    import sys
                    sys.exit()
    
    # Replace the engine's await_closure method
    engine.await_closure = custom_await_closure
    
    # Game loop
    @engine.game_loop
    def game_loop():
        nonlocal player_score, ai_score, game_over
        
        if not game_over:
            # Update game objects
            player_paddle.handle_keys(canvas)
            player_paddle.update(canvas)
            
            ai.update(ai_paddle, ball, canvas)
            ai_paddle.update(canvas)
            
            ball.update(canvas)
            
            # Check paddle collisions
            if ball.check_collision([player_paddle]):
                ball.bounce_off_paddle(player_paddle)
            elif ball.check_collision([ai_paddle]):
                ball.bounce_off_paddle(ai_paddle)
            
            # Check scoring
            if ball.box_collider.x < 0:  # AI scores
                ai_score += 1
                print(f"AI scores! Score: Player {player_score} - AI {ai_score}")
                ball.reset(canvas)
                if ai_score >= max_score:
                    game_over = True
                    print("AI wins! Game over.")
                    
            elif ball.box_collider.x > canvas.screen_size[0]:  # Player scores
                player_score += 1
                print(f"Player scores! Score: Player {player_score} - AI {ai_score}")
                ball.reset(canvas)
                if player_score >= max_score:
                    game_over = True
                    print("Player wins! Game over.")
        
        # Draw everything
        player_paddle.draw(canvas.surface)
        ai_paddle.draw(canvas.surface)
        ball.draw(canvas.surface)
        
        # Draw center line
        for y in range(0, canvas.screen_size[1], 20):
            pygame.draw.rect(canvas.surface, (100, 100, 100), 
                           (canvas.screen_size[0] // 2 - 2, y, 4, 10))


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