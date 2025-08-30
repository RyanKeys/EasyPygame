#!/usr/bin/env python3
"""
Unit tests for Pong demo classes
"""
import unittest
import pygame
from pong_demo import Ball, Paddle, PongPlayer, AIController
from EasyPygame.game_engine import Canvas


class TestPongDemo(unittest.TestCase):
    """Test cases for Pong demo classes"""
    
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 0))
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
    
    def test_ball_creation(self):
        """Test Ball class creation"""
        ball = Ball(spawn_coordinates=(400, 300), size=20)
        self.assertEqual(ball.box_collider.x, 400)
        self.assertEqual(ball.box_collider.y, 300)
        self.assertIsInstance(ball.velocity_x, (int, float))
        self.assertIsInstance(ball.velocity_y, (int, float))
        
    def test_ball_movement(self):
        """Test ball movement"""
        ball = Ball(spawn_coordinates=(400, 300))
        original_x = ball.box_collider.x
        ball.velocity_x = 5
        ball.update(self.canvas)
        self.assertEqual(ball.box_collider.x, original_x + 5)
    
    def test_ball_wall_bounce(self):
        """Test ball bouncing off walls"""
        ball = Ball(spawn_coordinates=(400, 0))  # At top wall
        ball.velocity_y = -5  # Moving up
        ball.update(self.canvas)
        self.assertGreater(ball.velocity_y, 0)  # Should bounce down
    
    def test_paddle_creation(self):
        """Test Paddle class creation"""
        paddle = Paddle(spawn_coordinates=(50, 250))
        self.assertEqual(paddle.box_collider.x, 50)
        self.assertEqual(paddle.box_collider.y, 250)
        self.assertEqual(paddle.width, 15)
        self.assertEqual(paddle.height, 80)
    
    def test_paddle_bounds(self):
        """Test paddle staying within bounds"""
        paddle = Paddle(spawn_coordinates=(50, -10))  # Above screen
        paddle.update(self.canvas)
        self.assertEqual(paddle.box_collider.y, 0)  # Should be clamped to top
        
        paddle.box_collider.y = self.canvas.screen_size[1] + 10  # Below screen
        paddle.update(self.canvas)
        self.assertEqual(paddle.box_collider.y, self.canvas.screen_size[1] - paddle.height)
    
    def test_pong_player_creation(self):
        """Test PongPlayer class creation"""
        player = PongPlayer(spawn_coordinates=(50, 250))
        self.assertIsNotNone(player.controller)
        self.assertEqual(player.box_collider.x, 50)
        self.assertEqual(player.box_collider.y, 250)
    
    def test_ai_controller(self):
        """Test AI controller creation"""
        ai = AIController(difficulty=0.8)
        self.assertEqual(ai.difficulty, 0.8)
    
    def test_ball_paddle_collision(self):
        """Test ball and paddle collision detection"""
        ball = Ball(spawn_coordinates=(50, 250))
        paddle = Paddle(spawn_coordinates=(50, 250))
        
        # They should collide since they're at the same position
        self.assertTrue(ball.check_collision([paddle]))
    
    def test_ball_bounce_off_paddle(self):
        """Test ball bouncing off paddle"""
        ball = Ball(spawn_coordinates=(50, 250))
        paddle = Paddle(spawn_coordinates=(50, 250))
        
        original_velocity_x = ball.velocity_x
        ball.bounce_off_paddle(paddle)
        
        # X velocity should be reversed (and may be slightly increased)
        self.assertLess(ball.velocity_x * original_velocity_x, 0)  # Opposite signs


def run_pong_tests():
    """Run all Pong tests"""
    print("Running Pong demo unit tests...")
    unittest.main(verbosity=2, exit=False)


if __name__ == "__main__":
    try:
        run_pong_tests()
    except Exception as e:
        print(f"Test error: {e}")
    finally:
        import pygame
        pygame.quit()