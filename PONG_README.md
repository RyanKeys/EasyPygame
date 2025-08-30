# Pong Demo for EasyPygame

This is a classic Pong game implementation built using the EasyPygame framework, demonstrating the framework's capabilities for creating arcade-style games.

## Game Features

- **Player vs AI**: Left paddle controlled by player, right paddle controlled by AI
- **Realistic Physics**: Ball bounces off paddles and walls with realistic physics
- **Adaptive Difficulty**: Ball speed increases slightly after each paddle hit
- **Score Tracking**: First to 5 points wins (scores displayed in console)
- **Smart AI**: AI paddle that intelligently follows the ball
- **Smooth Controls**: Responsive W/S key controls for player paddle

## How to Play

1. Run the game:
   ```bash
   python3 pong_demo.py
   ```

2. Controls:
   - **W**: Move player paddle up
   - **S**: Move player paddle down
   - **ESC** or close window: Exit game

3. Objective: 
   - Prevent the ball from reaching your side of the screen
   - Try to get the ball past the AI paddle to score
   - First to 5 points wins!

## Technical Implementation

The Pong demo showcases several EasyPygame framework features:

### Classes Used

- **Ball**: Extends `Character` class with velocity-based movement and collision physics
- **Paddle**: Custom rectangular character optimized for Pong gameplay
- **PongPlayer**: Player-controlled paddle with W/S key controls
- **PongKeyboardController**: Specialized input controller for Pong
- **AIController**: Simple AI that tracks ball movement

### EasyPygame Framework Features Demonstrated

1. **Character System**: Base character class with collision detection and drawing
2. **Input Handling**: Custom keyboard controllers for game-specific controls
3. **Game Engine**: 60 FPS game loop with event handling
4. **Canvas Management**: 800x600 window with black background
5. **Collision Detection**: Ball-paddle and ball-wall collision handling

### Game Physics

- Ball bounces off top and bottom walls
- Ball bounce angle depends on where it hits the paddle
- Ball speed gradually increases to make game more challenging
- Paddle movement constrained to screen boundaries
- AI difficulty can be adjusted (currently set to 80% accuracy)

## Code Structure

The demo is entirely self-contained in `pong_demo.py` and uses only the existing EasyPygame framework without modifications, demonstrating how easy it is to create complete games with the framework.

## Running Tests

Run the Pong-specific unit tests:
```bash
python3 test_pong_units.py
```

This tests all the game mechanics including ball physics, collision detection, paddle behavior, and AI controller functionality.