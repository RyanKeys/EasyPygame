#!/usr/bin/env python3
"""
Pong - EasyPygame Demo
======================

A polished Pong implementation showcasing EasyPygame's capabilities.

NOTE: Run `pip install -e .` from the repo root before running this example.

Features:
    - Player vs AI gameplay
    - On-screen score display
    - Ball physics with paddle angle deflection
    - Game over screen with restart option
    - Clean visual design

Controls:
    W / S       Move paddle up/down
    R           Restart game (when game over)
    ESC         Quit

This demo showcases:
    - Character class extension
    - Collision detection
    - Custom keyboard handling
    - Game state management
"""

import pygame
import random
from EasyPygame import Character, Engine, Canvas


# =============================================================================
# CONFIGURATION
# =============================================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
FPS = 60

PADDLE_WIDTH = 12
PADDLE_HEIGHT = 80
PADDLE_SPEED = 7
PADDLE_MARGIN = 40

BALL_SIZE = 14
BALL_SPEED_INITIAL = 5
BALL_SPEED_MAX = 10
BALL_SPEED_INCREMENT = 0.2

WINNING_SCORE = 7

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)


# =============================================================================
# GAME OBJECTS
# =============================================================================

class Paddle(Character):
    """A rectangular paddle that can move vertically."""
    
    def __init__(self, x: int, y: int):
        super().__init__(spawn_coordinates=(x, y), size=PADDLE_HEIGHT)
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill(WHITE)
        self.box_collider = self.image.get_rect(topleft=(x, y))
        self.speed = PADDLE_SPEED
    
    def move_up(self) -> None:
        """Move paddle up, respecting screen bounds."""
        self.box_collider.y = max(0, self.box_collider.y - self.speed)
    
    def move_down(self, screen_height: int) -> None:
        """Move paddle down, respecting screen bounds."""
        max_y = screen_height - PADDLE_HEIGHT
        self.box_collider.y = min(max_y, self.box_collider.y + self.speed)


class Ball(Character):
    """A ball that bounces around the playing field."""
    
    def __init__(self, x: int, y: int):
        super().__init__(spawn_coordinates=(x, y), size=BALL_SIZE)
        self.image.fill(WHITE)
        self.reset()
    
    def reset(self) -> None:
        """Reset ball to center with random direction."""
        self.box_collider.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        
        # Random angle, biased toward horizontal
        angle = random.uniform(-0.5, 0.5)
        direction = random.choice([-1, 1])
        
        self.vx = direction * BALL_SPEED_INITIAL
        self.vy = angle * BALL_SPEED_INITIAL
    
    def update(self) -> str | None:
        """
        Update ball position and handle wall bounces.
        
        Returns:
            'left' or 'right' if ball exits screen, None otherwise.
        """
        self.box_collider.x += self.vx
        self.box_collider.y += self.vy
        
        # Bounce off top/bottom
        if self.box_collider.top <= 0:
            self.box_collider.top = 0
            self.vy = abs(self.vy)
        elif self.box_collider.bottom >= SCREEN_HEIGHT:
            self.box_collider.bottom = SCREEN_HEIGHT
            self.vy = -abs(self.vy)
        
        # Check for scoring
        if self.box_collider.right < 0:
            return 'left'
        elif self.box_collider.left > SCREEN_WIDTH:
            return 'right'
        
        return None
    
    def bounce_off_paddle(self, paddle: Paddle) -> None:
        """Bounce off paddle with angle based on hit position."""
        # Calculate hit position (-1 to 1, where 0 is center)
        paddle_center = paddle.box_collider.centery
        ball_center = self.box_collider.centery
        hit_pos = (ball_center - paddle_center) / (PADDLE_HEIGHT / 2)
        hit_pos = max(-1, min(1, hit_pos))  # Clamp to [-1, 1]
        
        # Reverse horizontal direction
        self.vx = -self.vx
        
        # Adjust vertical velocity based on hit position
        self.vy = hit_pos * abs(self.vx) * 0.8
        
        # Speed up slightly
        speed = (self.vx ** 2 + self.vy ** 2) ** 0.5
        if speed < BALL_SPEED_MAX:
            factor = 1 + BALL_SPEED_INCREMENT / speed
            self.vx *= factor
            self.vy *= factor
        
        # Push ball out of paddle to prevent multiple collisions
        if self.vx > 0:
            self.box_collider.left = paddle.box_collider.right + 1
        else:
            self.box_collider.right = paddle.box_collider.left - 1


class AIController:
    """Simple AI that follows the ball with some reaction delay."""
    
    def __init__(self, paddle: Paddle, difficulty: float = 0.7):
        self.paddle = paddle
        self.difficulty = difficulty
        self.reaction_zone = SCREEN_WIDTH * 0.6  # Only react when ball is close
    
    def update(self, ball: Ball) -> None:
        """Move paddle toward ball position."""
        # Only react when ball is coming toward AI
        if ball.vx <= 0:
            return
        
        # Only react when ball is in reaction zone
        if ball.box_collider.x < self.reaction_zone:
            return
        
        # Random chance to skip (imperfect AI)
        if random.random() > self.difficulty:
            return
        
        # Move toward ball
        paddle_center = self.paddle.box_collider.centery
        ball_center = ball.box_collider.centery
        
        if paddle_center < ball_center - 10:
            self.paddle.move_down(SCREEN_HEIGHT)
        elif paddle_center > ball_center + 10:
            self.paddle.move_up()


# =============================================================================
# RENDERING
# =============================================================================

def draw_center_line(surface: pygame.Surface) -> None:
    """Draw dashed center line."""
    for y in range(0, SCREEN_HEIGHT, 30):
        pygame.draw.rect(surface, DARK_GRAY, (SCREEN_WIDTH // 2 - 2, y, 4, 15))


def draw_scores(surface: pygame.Surface, player_score: int, ai_score: int, font: pygame.font.Font) -> None:
    """Draw score display."""
    # Player score (left)
    player_text = font.render(str(player_score), True, GRAY)
    surface.blit(player_text, (SCREEN_WIDTH // 4 - player_text.get_width() // 2, 30))
    
    # AI score (right)
    ai_text = font.render(str(ai_score), True, GRAY)
    surface.blit(ai_text, (3 * SCREEN_WIDTH // 4 - ai_text.get_width() // 2, 30))


def draw_game_over(surface: pygame.Surface, winner: str, font_large: pygame.font.Font, font_small: pygame.font.Font) -> None:
    """Draw game over screen."""
    # Overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.fill(BLACK)
    overlay.set_alpha(180)
    surface.blit(overlay, (0, 0))
    
    # Winner text
    text = f"{'YOU WIN!' if winner == 'player' else 'AI WINS!'}"
    winner_text = font_large.render(text, True, WHITE)
    x = SCREEN_WIDTH // 2 - winner_text.get_width() // 2
    y = SCREEN_HEIGHT // 2 - 50
    surface.blit(winner_text, (x, y))
    
    # Restart prompt
    restart_text = font_small.render("Press R to restart or ESC to quit", True, GRAY)
    x = SCREEN_WIDTH // 2 - restart_text.get_width() // 2
    y = SCREEN_HEIGHT // 2 + 20
    surface.blit(restart_text, (x, y))


# =============================================================================
# MAIN GAME
# =============================================================================

def main():
    """Run the Pong game."""
    # Initialize
    canvas = Canvas(screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT), background_color=BLACK)
    engine = Engine(game_title="Pong — EasyPygame Demo", fps=FPS, canvas=canvas)
    
    # Fonts
    font_large = pygame.font.Font(None, 72)
    font_score = pygame.font.Font(None, 64)
    font_small = pygame.font.Font(None, 32)
    
    # Game objects
    player = Paddle(PADDLE_MARGIN, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ai_paddle = Paddle(SCREEN_WIDTH - PADDLE_MARGIN - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
    ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ai = AIController(ai_paddle, difficulty=0.75)
    
    # Game state
    player_score = 0
    ai_score = 0
    game_over = False
    winner = None
    
    @engine.game_loop
    def game_loop():
        nonlocal player_score, ai_score, game_over, winner
        
        keys = pygame.key.get_pressed()
        
        # Handle restart
        if game_over:
            if keys[pygame.K_r]:
                player_score = 0
                ai_score = 0
                game_over = False
                winner = None
                ball.reset()
                player.box_collider.centery = SCREEN_HEIGHT // 2
                ai_paddle.box_collider.centery = SCREEN_HEIGHT // 2
        else:
            # Player input
            if keys[pygame.K_w]:
                player.move_up()
            if keys[pygame.K_s]:
                player.move_down(SCREEN_HEIGHT)
            
            # AI
            ai.update(ball)
            
            # Ball physics
            result = ball.update()
            
            # Scoring
            if result == 'left':
                ai_score += 1
                if ai_score >= WINNING_SCORE:
                    game_over = True
                    winner = 'ai'
                else:
                    ball.reset()
            elif result == 'right':
                player_score += 1
                if player_score >= WINNING_SCORE:
                    game_over = True
                    winner = 'player'
                else:
                    ball.reset()
            
            # Paddle collisions
            if ball.check_collision([player]):
                ball.bounce_off_paddle(player)
            elif ball.check_collision([ai_paddle]):
                ball.bounce_off_paddle(ai_paddle)
        
        # Draw
        draw_center_line(canvas.surface)
        draw_scores(canvas.surface, player_score, ai_score, font_score)
        player.draw(canvas.surface)
        ai_paddle.draw(canvas.surface)
        ball.draw(canvas.surface)
        
        if game_over:
            draw_game_over(canvas.surface, winner, font_large, font_small)


if __name__ == "__main__":
    main()
