# EasyPygame

### A package designed to simplify your Pygame development!

EasyPygame provides a simplified API for creating games with Pygame, featuring easy-to-use classes for players, characters, game engines, and input handling.

## Installation

Install the package using pip:

```bash
pip install EasyPygame
```

## Quick Start

Here's a simple example to get you started:

```python
from EasyPygame import Player, Character, Engine, Canvas

# Create a canvas and game engine
canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 0))
engine = Engine(fps=60, canvas=canvas)

# Create a player and character
player = Player(spawn_coordinates=(400, 550), size=50)
character = Character(spawn_coordinates=(400, 50), size=50)

actors = [player, character]

# Define the game loop
@engine.game_loop
def game_loop():
    for actor in actors:
        actor.draw(engine.canvas.surface)
        if isinstance(actor, Player):
            actor.handle_keys(canvas=engine.canvas)
```

## Features

- **Simple Player class**: Easy player creation with built-in keyboard controls (WASD)
- **Character class**: Create NPCs with optional sprite support
- **Game Engine**: Handles the main game loop, FPS, and window management
- **Canvas**: Manages the game window and drawing surface
- **Collision Detection**: Built-in collision detection between game objects
- **Built-in Exit Controls**: Automatic handling of window close button and ESC key for game exit

## API Reference

### Canvas
Creates and manages the game window.

```python
canvas = Canvas(screen_size=(800, 600), background_color=(255, 255, 255))
```

### Engine
Manages the game loop and timing. Automatically handles window close events and ESC key for game exit.

```python
engine = Engine(fps=60, canvas=canvas, game_title="My Game")
```

### Player
A character controlled by keyboard input (WASD keys).

```python
player = Player(spawn_coordinates=(100, 100), size=32)
```

### Character
A basic game character that can optionally use sprites.

```python
# Character with default colored square
character = Character(spawn_coordinates=(200, 200), size=32)

# Character with custom sprite
character = Character(spawn_coordinates=(200, 200), size=32, sprite="path/to/sprite.png")
```

## Requirements

- Python 3.6+
- pygame

## License

MIT License
