#!/usr/bin/env python3
"""
Unit tests for Gyruss demo classes
==================================

This module contains unit tests for the Gyruss demo functionality.
Tests game mechanics without requiring actual pygame display.
"""

import unittest
import math
import pygame
from gyruss_demo import GyrusPlayer, Enemy, Projectile, GyrusController
from EasyPygame import Canvas


class TestGyrussDemo(unittest.TestCase):
    """Test cases for Gyruss demo classes"""
    
    def setUp(self):
        """Set up test fixtures"""
        pygame.init()
        self.canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 20))
    
    def tearDown(self):
        """Clean up after tests"""
        pygame.quit()
    
    def test_gyrus_player_creation(self):
        """Test GyrusPlayer class creation"""
        player = GyrusPlayer(self.canvas)
        self.assertIsNotNone(player.angle)
        self.assertIsNotNone(player.radius)
        self.assertEqual(player.center_x, 400)  # 800/2
        self.assertEqual(player.center_y, 300)  # 600/2
        self.assertIsInstance(player.controller, GyrusController)
    
    def test_gyrus_player_positioning(self):
        """Test player positioning around circle"""
        player = GyrusPlayer(self.canvas)
        
        # Test initial position (bottom of circle, angle = π/2)
        # cos(π/2) ≈ 0, sin(π/2) ≈ 1
        expected_center_x = 400 + player.radius * math.cos(math.pi / 2)
        expected_center_y = 300 + player.radius * math.sin(math.pi / 2)
        
        # Get actual center position
        actual_center_x = player.box_collider.x + player.size // 2
        actual_center_y = player.box_collider.y + player.size // 2
        
        # Position should be close to expected (accounting for floating point precision)
        self.assertAlmostEqual(actual_center_x, expected_center_x, delta=2)
        self.assertAlmostEqual(actual_center_y, expected_center_y, delta=2)
    
    def test_gyrus_controller_creation(self):
        """Test GyrusController creation"""
        controller = GyrusController(movement_speed=0.1)
        self.assertEqual(controller.angular_speed, 0.1)
        self.assertEqual(controller.shot_cooldown, 0.2)
    
    def test_projectile_creation(self):
        """Test Projectile class creation"""
        projectile = Projectile(100, 200, 1.0, 0.0, speed=10)
        self.assertEqual(projectile.box_collider.x, 100)
        self.assertEqual(projectile.box_collider.y, 200)
        self.assertEqual(projectile.velocity_x, 10.0)
        self.assertEqual(projectile.velocity_y, 0.0)
        self.assertEqual(projectile.lifetime, 60)
    
    def test_projectile_movement(self):
        """Test projectile movement"""
        projectile = Projectile(100, 200, 1.0, 0.0, speed=5)
        original_x = projectile.box_collider.x
        
        # Update projectile
        result = projectile.update(self.canvas)
        
        # Should move and still be active
        self.assertTrue(result)
        self.assertEqual(projectile.box_collider.x, original_x + 5)
        self.assertEqual(projectile.lifetime, 59)
    
    def test_projectile_lifetime_expiry(self):
        """Test projectile removal after lifetime expires"""
        projectile = Projectile(100, 200, 0.0, 0.0)
        projectile.lifetime = 1
        
        # Should be active for one more frame
        result = projectile.update(self.canvas)
        self.assertFalse(result)  # Should signal removal
    
    def test_enemy_creation(self):
        """Test Enemy class creation"""
        enemy = Enemy(self.canvas, spawn_angle=0.0)
        self.assertEqual(enemy.center_x, 400)
        self.assertEqual(enemy.center_y, 300)
        self.assertEqual(enemy.angle, 0.0)
        self.assertEqual(enemy.radius, 10)
    
    def test_enemy_spiral_movement(self):
        """Test enemy spiral movement"""
        enemy = Enemy(self.canvas, spawn_angle=0.0)
        original_radius = enemy.radius
        original_angle = enemy.angle
        
        # Update enemy
        result = enemy.update(self.canvas)
        
        # Should move outward and rotate
        self.assertTrue(result)
        self.assertGreater(enemy.radius, original_radius)
        self.assertGreater(enemy.angle, original_angle)
    
    def test_enemy_max_radius_removal(self):
        """Test enemy removal when reaching max radius"""
        enemy = Enemy(self.canvas)
        enemy.radius = enemy.max_radius + 1  # Beyond max
        
        result = enemy.update(self.canvas)
        self.assertFalse(result)  # Should signal removal
    
    def test_player_shot_trajectory(self):
        """Test player shooting trajectory calculation"""
        player = GyrusPlayer(self.canvas)
        direction = player.get_shot_trajectory()
        
        # Direction should be normalized (length ≈ 1)
        length = math.sqrt(direction[0]**2 + direction[1]**2)
        self.assertAlmostEqual(length, 1.0, places=5)
        
        # Direction should point toward center from player position
        player_center_x = player.box_collider.x + player.size // 2
        player_center_y = player.box_collider.y + player.size // 2
        
        expected_dx = player.center_x - player_center_x
        expected_dy = player.center_y - player_center_y
        expected_length = math.sqrt(expected_dx**2 + expected_dy**2)
        
        if expected_length > 0:
            expected_direction = (expected_dx / expected_length, expected_dy / expected_length)
            self.assertAlmostEqual(direction[0], expected_direction[0], places=5)
            self.assertAlmostEqual(direction[1], expected_direction[1], places=5)
    
    def test_collision_detection(self):
        """Test collision between projectile and enemy"""
        projectile = Projectile(100, 100, 0, 0)
        enemy = Enemy(self.canvas)
        enemy.box_collider.x = 100
        enemy.box_collider.y = 100
        
        # They should collide since they're at the same position
        self.assertTrue(projectile.check_collision([enemy]))


def run_gyruss_tests():
    """Run all Gyruss tests"""
    print("Running Gyruss demo unit tests...")
    unittest.main(verbosity=2, exit=False)


if __name__ == "__main__":
    run_gyruss_tests()