# Gyruss Demo for EasyPygame

## Overview

This is a classic Gyruss-style arcade game implementation using the EasyPygame framework. Gyruss is a shoot-em-up game where the player controls a ship that moves around the perimeter of a circular playing field, shooting at enemies that spiral outward from the center.

## Features

- **Circular Player Movement**: Player ship moves around the screen perimeter in a circular path
- **Enemy Spiral Patterns**: Enemies spawn from the center and spiral outward in classic Gyruss style
- **Projectile System**: Shoot projectiles from the player position toward the center
- **Collision Detection**: Projectiles destroy enemies on contact
- **Score Tracking**: Points awarded for destroying enemies
- **Real-time Gameplay**: 60 FPS smooth gameplay using EasyPygame framework

## Controls

- **A**: Move counterclockwise around the perimeter
- **D**: Move clockwise around the perimeter  
- **W** or **SPACE**: Fire projectile toward center
- **ESC** or close window: Exit game

## Visual Elements

- **Green Square**: Player ship
- **Red Circles**: Enemy ships
- **Yellow Dots**: Projectiles
- **Dark Blue Background**: Space environment

## Game Mechanics

1. **Player Movement**: The player ship is constrained to move in a circle around the screen perimeter. Movement is controlled by changing the angular position around the circle.

2. **Enemy Spawning**: Enemies spawn from the center at regular intervals with random angles.

3. **Enemy Movement**: Enemies move in spiral patterns, gradually increasing their distance from the center while rotating.

4. **Shooting**: Projectiles are fired radially inward from the player's current position toward the center.

5. **Collision**: When a projectile hits an enemy, both are destroyed and the score increases.

6. **Cleanup**: Projectiles and enemies are automatically removed when they go off-screen or exceed their lifetime.

## Technical Implementation

### Classes

- **GyrusPlayer**: Extends Character class, handles circular movement around screen perimeter
- **GyrusController**: Custom input controller for circular movement and shooting
- **Projectile**: Bullet objects that move from player toward center
- **Enemy**: Spiral-moving enemies that emerge from the center

### Key Algorithms

- **Circular Movement**: Uses trigonometric functions (sin/cos) to calculate positions on the circle
- **Trajectory Calculation**: Computes direction vectors from player position to screen center
- **Spiral Movement**: Combines radial expansion with angular rotation for enemy movement

## Running the Demo

```bash
python gyruss_demo.py
```

## Testing

Unit tests are available to verify the game mechanics:

```bash
python test_gyruss_units.py
```

This tests:
- Player positioning and movement
- Projectile creation and physics
- Enemy spawning and spiral movement
- Collision detection
- Game object lifecycle management

## Files

- `gyruss_demo.py`: Main game implementation
- `test_gyruss_units.py`: Unit tests for game classes
- `test_gyruss_demo.py`: Integration test for game mechanics
- `visual_test_gyruss.py`: Quick visual test (runs for 5 seconds)
- `GYRUSS_README.md`: This documentation

## Framework Integration

This demo showcases the EasyPygame framework's capabilities:

- **Character System**: All game objects inherit from the Character base class
- **Input Handling**: Custom controller extends KeyboardController
- **Game Engine**: Uses Engine class for main game loop and timing
- **Canvas Management**: Leverages Canvas for screen management
- **Collision Detection**: Built-in collision detection between game objects

The implementation follows EasyPygame patterns established in other demos like `pong_demo.py` and `example_game.py`.