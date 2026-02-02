#!/usr/bin/env python3
"""
Unit tests for EasyPygame package
=================================

This module contains unit tests for the core EasyPygame functionality.
Run with: python -m pytest tests.py -v
Or simply: python tests.py
"""

import unittest
import pygame
from EasyPygame import Player, Character, Engine, Canvas, KeyboardController, MouseController


class TestEasyPygame(unittest.TestCase):
    """Test cases for EasyPygame classes"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        
    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()
        
    def test_canvas_creation(self):
        """Test Canvas class creation and properties"""
        canvas = Canvas(screen_size=(400, 300), background_color=(255, 0, 0))
        self.assertEqual(canvas.screen_size, (400, 300))
        self.assertEqual(canvas.background_color, (255, 0, 0))
        self.assertIsNotNone(canvas.surface)
        
    def test_canvas_reset(self):
        """Test Canvas reset functionality"""
        canvas = Canvas()
        original_size = canvas.screen_size
        canvas.reset(screen_size=(800, 600), background_color=(0, 255, 0))
        self.assertEqual(canvas.screen_size, (800, 600))
        self.assertEqual(canvas.background_color, (0, 255, 0))
        self.assertNotEqual(canvas.screen_size, original_size)
        
    def test_character_creation(self):
        """Test Character class creation"""
        char = Character(spawn_coordinates=(100, 200), size=50)
        self.assertEqual(char.spawn_coordinates, (100, 200))
        self.assertEqual(char.size, 50)
        self.assertEqual(char.box_collider.x, 100)
        self.assertEqual(char.box_collider.y, 200)
        self.assertIsNotNone(char.image)
        
    def test_character_default_sprite(self):
        """Test Character with default sprite (no sprite provided)"""
        char = Character(size=30)
        self.assertIsNotNone(char.image)
        # Should create a colored surface when no sprite is provided
        self.assertEqual(char.image.get_size(), (30, 30))
        
    def test_player_creation(self):
        """Test Player class creation and inheritance"""
        player = Player(spawn_coordinates=(50, 75), size=25)
        self.assertEqual(player.spawn_coordinates, (50, 75))
        self.assertEqual(player.size, 25)
        self.assertIsInstance(player.controller, KeyboardController)
        # Player should inherit from Character
        self.assertIsInstance(player, Character)
        
    def test_keyboard_controller(self):
        """Test KeyboardController creation"""
        controller = KeyboardController(movement_speed=15)
        self.assertEqual(controller.movement_speed, 15)
        
    def test_collision_detection_no_collision(self):
        """Test collision detection when objects don't collide"""
        char1 = Character(spawn_coordinates=(0, 0), size=20)
        char2 = Character(spawn_coordinates=(100, 100), size=20)
        
        # Objects are far apart, should not collide
        self.assertFalse(char1.check_collision([char2]))
        self.assertFalse(char2.check_collision([char1]))
        
    def test_collision_detection_with_collision(self):
        """Test collision detection when objects do collide"""
        char1 = Character(spawn_coordinates=(100, 100), size=50)
        char2 = Character(spawn_coordinates=(120, 120), size=50)
        
        # Objects overlap, should collide
        self.assertTrue(char1.check_collision([char2]))
        self.assertTrue(char2.check_collision([char1]))
        
    def test_collision_detection_multiple_objects(self):
        """Test collision detection with multiple objects"""
        player = Player(spawn_coordinates=(100, 100), size=30)
        char1 = Character(spawn_coordinates=(200, 200), size=30)  # Far away
        char2 = Character(spawn_coordinates=(110, 110), size=30)  # Close/colliding
        
        # Should detect collision with char2 but not char1
        result = player.check_collision([char1, char2])
        self.assertTrue(result)
        
        # Test with only non-colliding object
        result = player.check_collision([char1])
        self.assertFalse(result)
        
    def test_engine_creation(self):
        """Test Engine class creation"""
        canvas = Canvas()
        engine = Engine(fps=30, canvas=canvas, game_title="Test Game")
        
        self.assertEqual(engine.fps, 30)
        self.assertEqual(engine.game_title, "Test Game")
        self.assertEqual(engine.canvas, canvas)
        self.assertIsNotNone(engine.clock)
        
    def test_engine_default_canvas(self):
        """Test Engine creation with default canvas"""
        engine = Engine(fps=60)
        self.assertEqual(engine.fps, 60)
        self.assertIsNotNone(engine.canvas)
        self.assertIsInstance(engine.canvas, Canvas)

    def test_mouse_controller_creation(self):
        """Test MouseController class creation and methods"""
        mouse = MouseController()
        
        # Test that methods exist and are callable
        self.assertTrue(callable(mouse.get_position))
        self.assertTrue(callable(mouse.is_pressed))
        self.assertTrue(callable(mouse.is_left_pressed))
        self.assertTrue(callable(mouse.is_right_pressed))
        self.assertTrue(callable(mouse.is_over))
        self.assertTrue(callable(mouse.is_clicking))
        
        # Test get_position returns a tuple
        pos = mouse.get_position()
        self.assertIsInstance(pos, tuple)
        self.assertEqual(len(pos), 2)

    def test_mouse_is_over(self):
        """Test MouseController.is_over method"""
        mouse = MouseController()
        char = Character(spawn_coordinates=(0, 0), size=100)
        
        # is_over should return a boolean
        result = mouse.is_over(char)
        self.assertIsInstance(result, bool)


def run_tests():
    """Run all tests"""
    print("Running EasyPygame unit tests...")
    unittest.main(verbosity=2, exit=False)


if __name__ == "__main__":
    run_tests()