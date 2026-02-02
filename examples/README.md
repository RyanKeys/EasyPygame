# EasyPygame Examples

Polished game demos showcasing EasyPygame's features.

## Installation

```bash
pip install EasyPygame

# Or install from source:
cd EasyPygame
pip install -e .
```

## Running the Examples

```bash
python examples/pong.py
python examples/target_practice.py
python examples/space_dodge.py
```

---

## 🏓 Pong

A classic Pong game with Player vs AI.

**Showcases:**
- `Character` class extension for custom game objects
- Collision detection with `check_collision()`
- Keyboard input handling
- AI opponent logic
- Game state management (playing → game over → restart)

**Controls:**
| Key | Action |
|-----|--------|
| W | Move paddle up |
| S | Move paddle down |
| R | Restart (when game over) |
| ESC | Quit |

---

## 🎯 Target Practice

A timed shooting gallery with shrinking targets and combo scoring.

**Showcases:**
- `MouseController` for click and position tracking
- Dynamic object resizing
- Combo/scoring systems
- Visual effects (hit feedback, crosshair)
- UI rendering with fonts

**Controls:**
| Input | Action |
|-------|--------|
| Left Click | Shoot |
| R | Restart (when game over) |
| ESC | Quit |

---

## 🚀 Space Dodge

A survival game where you dodge falling asteroids.

**Showcases:**
- `Player` class with WASD movement
- Procedural asteroid generation
- Difficulty scaling over time
- Particle effects (explosions)
- Parallax star background

**Controls:**
| Key | Action |
|-----|--------|
| W | Move up |
| A | Move left |
| S | Move down |
| D | Move right |
| R | Restart (when game over) |
| ESC | Quit |

---

## What Each Demo Teaches

| Feature | Pong | Target Practice | Space Dodge |
|---------|:----:|:---------------:|:-----------:|
| Character class | ✅ | ✅ | ✅ |
| Player class | | | ✅ |
| Keyboard input | ✅ | | ✅ |
| Mouse input | | ✅ | |
| Collision detection | ✅ | ✅ | ✅ |
| Game states | ✅ | ✅ | ✅ |
| UI/Fonts | ✅ | ✅ | ✅ |
| Particle effects | | | ✅ |

---

## Code Structure

Each example follows the same pattern:

```python
# 1. Configuration constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# 2. Custom game object classes
class Ball(Character):
    ...

# 3. Helper functions for rendering
def draw_ui(surface, state, fonts):
    ...

# 4. Main game function with @engine.game_loop
def main():
    canvas = Canvas(...)
    engine = Engine(...)
    
    @engine.game_loop
    def game_loop():
        # Game logic here
        ...

if __name__ == "__main__":
    main()
```

Feel free to use these as templates for your own games!
