#!/usr/bin/env python3
"""
Space Dodge - EasyPygame Demo
=============================

A survival game where you dodge falling asteroids.

NOTE: Run `pip install -e .` from the repo root before running this example.

Features:
    - WASD movement with smooth controls
    - Increasing difficulty over time
    - Survival timer with high score
    - Particle effects on collision
    - Clean space aesthetic

Controls:
    W/A/S/D     Move ship
    R           Restart game (when game over)
    ESC         Quit

This demo showcases:
    - Player class with keyboard controls
    - Character class for obstacles
    - Collision detection
    - Difficulty scaling
    - Particle systems
"""

import pygame
import random
import math
from EasyPygame import Player, Character, Engine, Canvas


# =============================================================================
# CONFIGURATION
# =============================================================================

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
FPS = 60

PLAYER_SIZE = 30
PLAYER_SPEED = 6

ASTEROID_SIZE_MIN = 20
ASTEROID_SIZE_MAX = 50
ASTEROID_SPEED_MIN = 3
ASTEROID_SPEED_MAX = 8

SPAWN_INTERVAL_INITIAL = 40
SPAWN_INTERVAL_MIN = 15
DIFFICULTY_INCREASE_RATE = 0.02

# Colors
BG_COLOR = (10, 12, 20)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
RED = (220, 80, 80)
ORANGE = (255, 160, 60)
CYAN = (80, 200, 220)
YELLOW = (255, 220, 80)


# =============================================================================
# GAME OBJECTS
# =============================================================================

class Ship(Player):
    """Player-controlled spaceship."""
    
    def __init__(self, x: int, y: int):
        super().__init__(spawn_coordinates=(x, y), size=PLAYER_SIZE)
        self._draw_ship()
        self.speed = PLAYER_SPEED
    
    def _draw_ship(self) -> None:
        """Draw a triangular ship."""
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE), pygame.SRCALPHA)
        
        # Triangle pointing up
        points = [
            (PLAYER_SIZE // 2, 0),           # Top
            (0, PLAYER_SIZE),                 # Bottom left
            (PLAYER_SIZE, PLAYER_SIZE)        # Bottom right
        ]
        pygame.draw.polygon(self.image, CYAN, points)
        
        # Engine glow
        engine_points = [
            (PLAYER_SIZE // 2 - 5, PLAYER_SIZE - 5),
            (PLAYER_SIZE // 2, PLAYER_SIZE + 3),
            (PLAYER_SIZE // 2 + 5, PLAYER_SIZE - 5)
        ]
        pygame.draw.polygon(self.image, ORANGE, engine_points)
    
    def update(self, keys_pressed: pygame.key.ScancodeWrapper) -> None:
        """Update ship position based on input."""
        if keys_pressed[pygame.K_w] and self.box_collider.top > 0:
            self.box_collider.y -= self.speed
        if keys_pressed[pygame.K_s] and self.box_collider.bottom < SCREEN_HEIGHT:
            self.box_collider.y += self.speed
        if keys_pressed[pygame.K_a] and self.box_collider.left > 0:
            self.box_collider.x -= self.speed
        if keys_pressed[pygame.K_d] and self.box_collider.right < SCREEN_WIDTH:
            self.box_collider.x += self.speed
    
    def reset(self) -> None:
        """Reset ship to starting position."""
        self.box_collider.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)


class Asteroid(Character):
    """A falling asteroid obstacle."""
    
    def __init__(self, x: int, size: int, speed: float):
        super().__init__(spawn_coordinates=(x, -size), size=size)
        self.speed = speed
        self.rotation = 0
        self.rotation_speed = random.uniform(-3, 3)
        self._draw_asteroid()
    
    def _draw_asteroid(self) -> None:
        """Draw an irregular asteroid shape."""
        self.base_image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Create irregular polygon
        center = self.size // 2
        points = []
        num_points = random.randint(6, 9)
        
        for i in range(num_points):
            angle = (2 * math.pi * i) / num_points
            radius = center * random.uniform(0.6, 1.0)
            px = center + radius * math.cos(angle)
            py = center + radius * math.sin(angle)
            points.append((px, py))
        
        # Main body
        color = random.choice([
            (120, 100, 80),
            (100, 90, 70),
            (90, 80, 60)
        ])
        pygame.draw.polygon(self.base_image, color, points)
        pygame.draw.polygon(self.base_image, (60, 50, 40), points, 2)
        
        self.image = self.base_image.copy()
    
    def update(self) -> bool:
        """
        Update asteroid position and rotation.
        
        Returns:
            False if asteroid is off screen.
        """
        self.box_collider.y += self.speed
        self.rotation += self.rotation_speed
        
        # Rotate image
        self.image = pygame.transform.rotate(self.base_image, self.rotation)
        
        # Update collider to match rotated image
        old_center = self.box_collider.center
        self.box_collider = self.image.get_rect(center=old_center)
        
        return self.box_collider.top < SCREEN_HEIGHT + 50


class Particle:
    """A simple particle for explosion effects."""
    
    def __init__(self, x: float, y: float, color: tuple):
        self.x = x
        self.y = y
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 8)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.size = random.randint(2, 5)
        self.lifetime = random.randint(20, 40)
    
    def update(self) -> bool:
        """Update particle. Returns False when expired."""
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.1  # Gravity
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the particle."""
        alpha = int(255 * (self.lifetime / 40))
        color = (*self.color[:3], alpha)
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.size)


class Star:
    """A background star for parallax effect."""
    
    def __init__(self):
        self.x = random.randint(0, SCREEN_WIDTH)
        self.y = random.randint(0, SCREEN_HEIGHT)
        self.speed = random.uniform(0.5, 2)
        self.brightness = random.randint(50, 150)
    
    def update(self) -> None:
        """Update star position."""
        self.y += self.speed
        if self.y > SCREEN_HEIGHT:
            self.y = 0
            self.x = random.randint(0, SCREEN_WIDTH)
    
    def draw(self, surface: pygame.Surface) -> None:
        """Draw the star."""
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), 1)


# =============================================================================
# GAME STATE
# =============================================================================

class GameState:
    """Manages game state."""
    
    def __init__(self):
        self.high_score = 0
        self.reset()
    
    def reset(self) -> None:
        """Reset game state."""
        self.survival_time = 0
        self.game_over = False
        self.spawn_interval = SPAWN_INTERVAL_INITIAL
        self.difficulty = 1.0
    
    def update(self, dt: float) -> None:
        """Update game state."""
        if not self.game_over:
            self.survival_time += dt
            self.difficulty = 1.0 + self.survival_time * DIFFICULTY_INCREASE_RATE
            self.spawn_interval = max(
                SPAWN_INTERVAL_MIN,
                SPAWN_INTERVAL_INITIAL / self.difficulty
            )
    
    def end_game(self) -> None:
        """End the game."""
        self.game_over = True
        self.high_score = max(self.high_score, self.survival_time)
    
    @property
    def time_display(self) -> str:
        """Format survival time for display."""
        total_seconds = int(self.survival_time)
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        tenths = int((self.survival_time % 1) * 10)
        return f"{minutes}:{seconds:02d}.{tenths}"


# =============================================================================
# RENDERING
# =============================================================================

def draw_ui(surface: pygame.Surface, state: GameState, fonts: dict) -> None:
    """Draw game UI."""
    # Survival time
    time_text = fonts['large'].render(state.time_display, True, WHITE)
    surface.blit(time_text, (SCREEN_WIDTH // 2 - time_text.get_width() // 2, 20))
    
    # High score (subtle)
    if state.high_score > 0:
        hs_time = state.high_score
        hs_str = f"Best: {int(hs_time // 60)}:{int(hs_time % 60):02d}"
        hs_text = fonts['small'].render(hs_str, True, GRAY)
        surface.blit(hs_text, (SCREEN_WIDTH // 2 - hs_text.get_width() // 2, 60))


def draw_game_over(surface: pygame.Surface, state: GameState, fonts: dict) -> None:
    """Draw game over screen."""
    # Overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    surface.blit(overlay, (0, 0))
    
    center_x = SCREEN_WIDTH // 2
    y = SCREEN_HEIGHT // 2 - 100
    
    # Title
    title = fonts['title'].render("GAME OVER", True, RED)
    surface.blit(title, (center_x - title.get_width() // 2, y))
    y += 80
    
    # Survival time
    time_label = fonts['medium'].render("You survived:", True, GRAY)
    surface.blit(time_label, (center_x - time_label.get_width() // 2, y))
    y += 40
    
    time_text = fonts['large'].render(state.time_display, True, YELLOW)
    surface.blit(time_text, (center_x - time_text.get_width() // 2, y))
    y += 60
    
    # High score
    if state.survival_time >= state.high_score:
        new_best = fonts['medium'].render("NEW BEST!", True, CYAN)
        surface.blit(new_best, (center_x - new_best.get_width() // 2, y))
        y += 40
    else:
        hs_time = state.high_score
        hs_str = f"Best: {int(hs_time // 60)}:{int(hs_time % 60):02d}"
        best = fonts['medium'].render(hs_str, True, GRAY)
        surface.blit(best, (center_x - best.get_width() // 2, y))
        y += 40
    
    y += 30
    
    # Restart prompt
    restart = fonts['medium'].render("Press R to try again", True, WHITE)
    surface.blit(restart, (center_x - restart.get_width() // 2, y))


def create_explosion(x: int, y: int) -> list[Particle]:
    """Create explosion particles."""
    particles = []
    colors = [RED, ORANGE, YELLOW, WHITE]
    
    for _ in range(30):
        color = random.choice(colors)
        particles.append(Particle(x, y, color))
    
    return particles


# =============================================================================
# MAIN GAME
# =============================================================================

def main():
    """Run the Space Dodge game."""
    # Initialize
    canvas = Canvas(screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT), background_color=BG_COLOR)
    engine = Engine(game_title="Space Dodge — EasyPygame Demo", fps=FPS, canvas=canvas)
    
    # Fonts
    fonts = {
        'title': pygame.font.Font(None, 64),
        'large': pygame.font.Font(None, 48),
        'medium': pygame.font.Font(None, 32),
        'small': pygame.font.Font(None, 24),
    }
    
    # Game objects
    ship = Ship(SCREEN_WIDTH // 2 - PLAYER_SIZE // 2, SCREEN_HEIGHT - 80)
    asteroids: list[Asteroid] = []
    particles: list[Particle] = []
    stars: list[Star] = [Star() for _ in range(50)]
    
    # Game state
    state = GameState()
    spawn_timer = 0
    
    @engine.game_loop
    def game_loop():
        nonlocal spawn_timer
        
        keys = pygame.key.get_pressed()
        
        # Handle restart
        if state.game_over:
            if keys[pygame.K_r]:
                state.reset()
                ship.reset()
                asteroids.clear()
                particles.clear()
                spawn_timer = 0
        else:
            # Update game state
            state.update(1 / FPS)
            
            # Update ship
            ship.update(keys)
            
            # Spawn asteroids
            spawn_timer += 1
            if spawn_timer >= state.spawn_interval:
                spawn_timer = 0
                
                size = random.randint(ASTEROID_SIZE_MIN, ASTEROID_SIZE_MAX)
                x = random.randint(size, SCREEN_WIDTH - size)
                speed = random.uniform(
                    ASTEROID_SPEED_MIN * state.difficulty,
                    ASTEROID_SPEED_MAX * state.difficulty
                )
                speed = min(speed, ASTEROID_SPEED_MAX * 2)  # Cap speed
                
                asteroids.append(Asteroid(x, size, speed))
            
            # Update asteroids
            for asteroid in asteroids[:]:
                if not asteroid.update():
                    asteroids.remove(asteroid)
            
            # Check collisions
            for asteroid in asteroids:
                if ship.check_collision([asteroid]):
                    # Create explosion at ship position
                    particles.extend(create_explosion(
                        ship.box_collider.centerx,
                        ship.box_collider.centery
                    ))
                    state.end_game()
                    break
        
        # Update particles (even when game over)
        for particle in particles[:]:
            if not particle.update():
                particles.remove(particle)
        
        # Update stars
        for star in stars:
            star.update()
        
        # Draw stars (background)
        for star in stars:
            star.draw(canvas.surface)
        
        # Draw asteroids
        for asteroid in asteroids:
            asteroid.draw(canvas.surface)
        
        # Draw ship (if alive)
        if not state.game_over:
            ship.draw(canvas.surface)
        
        # Draw particles
        for particle in particles:
            particle.draw(canvas.surface)
        
        # Draw UI
        draw_ui(canvas.surface, state, fonts)
        
        # Draw game over
        if state.game_over:
            draw_game_over(canvas.surface, state, fonts)


if __name__ == "__main__":
    main()
