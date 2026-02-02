# EasyPygame

A package designed to simplify your Pygame development!

## Installation

```bash
pip install EasyPygame

# Or from source:
git clone https://github.com/RyanKeys/EasyPygame.git
cd EasyPygame
pip install -e .
```

## Quick Start

```python
from EasyPygame import Player, Character, Engine, Canvas

canvas = Canvas(screen_size=(800, 600), background_color=(0, 0, 0))
engine = Engine(fps=60, canvas=canvas)

player = Player(spawn_coordinates=(400, 500), size=40)

@engine.game_loop
def game_loop():
    player.handle_keys(canvas=canvas)
    player.draw(canvas.surface)
```

## Features

- **Player** — Keyboard-controlled character (WASD)
- **Character** — Base class for game objects with sprites
- **Engine** — Game loop, FPS, window management
- **Canvas** — Window and drawing surface
- **KeyboardController** — Customizable keyboard input
- **MouseController** — Mouse position, clicks, hover detection
- **Collision Detection** — Built-in `check_collision()` method
- **Type Hints** — Full type annotations on public API

## Mouse Input

```python
from EasyPygame import MouseController, Character

mouse = MouseController()

# In game loop:
pos = mouse.get_position()           # (x, y) tuple
clicking = mouse.is_left_pressed()   # bool
hovering = mouse.is_over(character)  # bool
```

## Examples

See the `examples/` folder for complete games:

| Example | Description | Controls |
|---------|-------------|----------|
| `pong.py` | Classic Pong vs AI | W/S, R to restart |
| `target_practice.py` | Click targets to score | Mouse, R to restart |
| `space_dodge.py` | Dodge falling asteroids | WASD, R to restart |

Run examples:
```bash
cd EasyPygame
pip install -e .
python examples/pong.py
```

## API Reference

### Canvas
```python
canvas = Canvas(screen_size=(800, 600), background_color=(255, 255, 255))
canvas.reset(screen_size=(1024, 768))  # Resize
```

### Engine
```python
engine = Engine(fps=60, canvas=canvas, game_title="My Game")

@engine.game_loop
def loop():
    # Your game logic here
    pass
```

### Player / Character
```python
player = Player(spawn_coordinates=(100, 100), size=32)
player.handle_keys(canvas=canvas)  # WASD movement
player.draw(surface)
player.check_collision([other_characters])  # Returns bool

character = Character(spawn_coordinates=(200, 200), size=32, sprite="sprite.png")
```

### MouseController
```python
mouse = MouseController()
mouse.get_position()        # (x, y)
mouse.is_pressed(button=0)  # 0=left, 1=middle, 2=right
mouse.is_left_pressed()     # Shorthand
mouse.is_over(character)    # Hover detection
mouse.is_clicking(character)  # Hover + click
```

## Requirements

- Python 3.9+
- pygame

## License

MIT
