#!/usr/bin/env python3
"""
Target Practice - EasyPygame Demo
=================================

A mouse-based target shooting game showcasing EasyPygame's mouse input.

NOTE: Run `pip install -e .` from the repo root before running this example.

Features:
    - Click on targets to score points
    - Targets shrink over time (harder to hit)
    - Combo system for consecutive hits
    - 60-second timed rounds
    - High score tracking (per session)
    - Visual feedback on hits/misses

Controls:
    Left Click      Shoot at targets
    R               Restart game (when game over)
    ESC             Quit

This demo showcases:
    - MouseController for click/hover detection
    - Character class for targets
    - Game state management
    - UI rendering
"""

import pygame
import random
import math
from EasyPygame import Character, Engine, Canvas, MouseController


# =============================================================================
# CONFIGURATION
# =============================================================================

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

TARGET_SIZE_MAX = 60
TARGET_SIZE_MIN = 20
TARGET_SHRINK_RATE = 0.3
TARGET_SPAWN_INTERVAL = 45  # frames
MAX_TARGETS = 6

GAME_DURATION = 60  # seconds

# Colors
BG_COLOR = (20, 25, 35)
WHITE = (255, 255, 255)
GRAY = (120, 120, 120)
RED = (220, 60, 60)
GREEN = (60, 220, 100)
YELLOW = (255, 220, 50)
ORANGE = (255, 150, 50)
DARK_OVERLAY = (0, 0, 0, 200)


# =============================================================================
# GAME OBJECTS
# =============================================================================

class Target(Character):
    """A shrinking target that can be clicked."""
    
    def __init__(self, x: int, y: int):
        super().__init__(spawn_coordinates=(x, y), size=TARGET_SIZE_MAX)
        self.max_size = TARGET_SIZE_MAX
        self.current_size = float(TARGET_SIZE_MAX)
        self.points = 10  # Base points
        self._update_image()
    
    def _update_image(self) -> None:
        """Recreate image at current size."""
        size = int(self.current_size)
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # Draw target rings
        center = size // 2
        
        # Outer ring (red)
        pygame.draw.circle(self.image, RED, (center, center), center)
        
        # Middle ring (white)
        if center > 10:
            pygame.draw.circle(self.image, WHITE, (center, center), int(center * 0.65))
        
        # Inner ring (red)
        if center > 15:
            pygame.draw.circle(self.image, RED, (center, center), int(center * 0.35))
        
        # Bullseye (white)
        if center > 20:
            pygame.draw.circle(self.image, WHITE, (center, center), int(center * 0.15))
        
        self.box_collider = self.image.get_rect(center=(
            self.box_collider.centerx if hasattr(self, 'box_collider') else self.spawn_coordinates[0],
            self.box_collider.centery if hasattr(self, 'box_collider') else self.spawn_coordinates[1]
        ))
    
    def update(self) -> bool:
        """
        Shrink target over time.
        
        Returns:
            False if target should be removed (too small).
        """
        self.current_size -= TARGET_SHRINK_RATE
        
        if self.current_size < TARGET_SIZE_MIN:
            return False
        
        # Update points (smaller = more points)
        size_ratio = 1 - (self.current_size - TARGET_SIZE_MIN) / (TARGET_SIZE_MAX - TARGET_SIZE_MIN)
        self.points = 10 + int(size_ratio * 40)  # 10-50 points
        
        center = self.box_collider.center
        self._update_image()
        self.box_collider.center = center
        
        return True
    
    def contains_point(self, pos: tuple[int, int]) -> bool:
        """Check if a point is within the target circle."""
        cx, cy = self.box_collider.center
        px, py = pos
        radius = self.current_size / 2
        distance = math.sqrt((px - cx) ** 2 + (py - cy) ** 2)
        return distance <= radius


class HitEffect:
    """Visual effect for hits/misses."""
    
    def __init__(self, x: int, y: int, text: str, color: tuple):
        self.x = x
        self.y = y
        self.text = text
        self.color = color
        self.lifetime = 30
        self.alpha = 255
    
    def update(self) -> bool:
        """Update effect. Returns False when expired."""
        self.lifetime -= 1
        self.y -= 2
        self.alpha = int(255 * (self.lifetime / 30))
        return self.lifetime > 0
    
    def draw(self, surface: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the effect."""
        text_surf = font.render(self.text, True, self.color)
        text_surf.set_alpha(self.alpha)
        surface.blit(text_surf, (self.x - text_surf.get_width() // 2, self.y))


# =============================================================================
# GAME STATE
# =============================================================================

class GameState:
    """Manages game state and scoring."""
    
    def __init__(self):
        self.reset()
    
    def reset(self) -> None:
        """Reset game state."""
        self.score = 0
        self.combo = 0
        self.max_combo = 0
        self.hits = 0
        self.misses = 0
        self.time_remaining = GAME_DURATION
        self.game_over = False
        self.high_score = getattr(self, 'high_score', 0)
    
    def register_hit(self, points: int) -> int:
        """Register a hit and return total points earned."""
        self.hits += 1
        self.combo += 1
        self.max_combo = max(self.max_combo, self.combo)
        
        # Combo bonus
        combo_multiplier = min(1 + self.combo * 0.1, 3.0)
        total_points = int(points * combo_multiplier)
        self.score += total_points
        
        return total_points
    
    def register_miss(self) -> None:
        """Register a miss."""
        self.misses += 1
        self.combo = 0
    
    def update_time(self, dt: float) -> None:
        """Update remaining time."""
        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.time_remaining = 0
            self.game_over = True
            self.high_score = max(self.high_score, self.score)
    
    @property
    def accuracy(self) -> float:
        """Calculate accuracy percentage."""
        total = self.hits + self.misses
        return (self.hits / total * 100) if total > 0 else 0


# =============================================================================
# RENDERING
# =============================================================================

def draw_ui(surface: pygame.Surface, state: GameState, fonts: dict) -> None:
    """Draw game UI elements."""
    # Score
    score_text = fonts['large'].render(f"{state.score:,}", True, WHITE)
    surface.blit(score_text, (20, 15))
    
    score_label = fonts['small'].render("SCORE", True, GRAY)
    surface.blit(score_label, (20, 55))
    
    # Combo
    if state.combo > 1:
        combo_color = YELLOW if state.combo < 5 else ORANGE if state.combo < 10 else GREEN
        combo_text = fonts['medium'].render(f"{state.combo}x COMBO", True, combo_color)
        surface.blit(combo_text, (20, 90))
    
    # Timer
    minutes = int(state.time_remaining) // 60
    seconds = int(state.time_remaining) % 60
    timer_color = RED if state.time_remaining < 10 else WHITE
    timer_text = fonts['large'].render(f"{minutes}:{seconds:02d}", True, timer_color)
    surface.blit(timer_text, (SCREEN_WIDTH - timer_text.get_width() - 20, 15))
    
    time_label = fonts['small'].render("TIME", True, GRAY)
    surface.blit(time_label, (SCREEN_WIDTH - time_label.get_width() - 20, 55))


def draw_crosshair(surface: pygame.Surface, pos: tuple[int, int]) -> None:
    """Draw crosshair at mouse position."""
    x, y = pos
    color = (200, 200, 200)
    
    # Outer circle
    pygame.draw.circle(surface, color, (x, y), 15, 2)
    
    # Cross lines
    pygame.draw.line(surface, color, (x - 20, y), (x - 8, y), 2)
    pygame.draw.line(surface, color, (x + 8, y), (x + 20, y), 2)
    pygame.draw.line(surface, color, (x, y - 20), (x, y - 8), 2)
    pygame.draw.line(surface, color, (x, y + 8), (x, y + 20), 2)
    
    # Center dot
    pygame.draw.circle(surface, color, (x, y), 2)


def draw_game_over(surface: pygame.Surface, state: GameState, fonts: dict) -> None:
    """Draw game over screen."""
    # Overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 200))
    surface.blit(overlay, (0, 0))
    
    center_x = SCREEN_WIDTH // 2
    y = 120
    
    # Title
    title = fonts['title'].render("TIME'S UP!", True, WHITE)
    surface.blit(title, (center_x - title.get_width() // 2, y))
    y += 80
    
    # Final score
    score_text = fonts['large'].render(f"Score: {state.score:,}", True, YELLOW)
    surface.blit(score_text, (center_x - score_text.get_width() // 2, y))
    y += 60
    
    # Stats
    stats = [
        f"Hits: {state.hits}  |  Misses: {state.misses}",
        f"Accuracy: {state.accuracy:.1f}%",
        f"Max Combo: {state.max_combo}x",
        f"High Score: {state.high_score:,}"
    ]
    
    for stat in stats:
        stat_text = fonts['medium'].render(stat, True, GRAY)
        surface.blit(stat_text, (center_x - stat_text.get_width() // 2, y))
        y += 35
    
    # Restart prompt
    y += 30
    restart = fonts['medium'].render("Press R to play again", True, WHITE)
    surface.blit(restart, (center_x - restart.get_width() // 2, y))


# =============================================================================
# MAIN GAME
# =============================================================================

def spawn_target(targets: list[Target]) -> Target | None:
    """Spawn a new target at a random position, avoiding overlap."""
    margin = TARGET_SIZE_MAX
    
    for _ in range(20):  # Max attempts
        x = random.randint(margin, SCREEN_WIDTH - margin)
        y = random.randint(margin + 80, SCREEN_HEIGHT - margin)  # Avoid UI
        
        # Check overlap with existing targets
        overlaps = False
        for t in targets:
            dx = x - t.box_collider.centerx
            dy = y - t.box_collider.centery
            dist = math.sqrt(dx*dx + dy*dy)
            if dist < TARGET_SIZE_MAX * 1.5:
                overlaps = True
                break
        
        if not overlaps:
            target = Target(x, y)
            target.box_collider.center = (x, y)
            return target
    
    return None


def main():
    """Run the Target Practice game."""
    # Initialize
    canvas = Canvas(screen_size=(SCREEN_WIDTH, SCREEN_HEIGHT), background_color=BG_COLOR)
    engine = Engine(game_title="Target Practice — EasyPygame Demo", fps=FPS, canvas=canvas)
    mouse = MouseController()
    
    # Fonts
    fonts = {
        'title': pygame.font.Font(None, 72),
        'large': pygame.font.Font(None, 48),
        'medium': pygame.font.Font(None, 32),
        'small': pygame.font.Font(None, 24),
    }
    
    # Game state
    state = GameState()
    targets: list[Target] = []
    effects: list[HitEffect] = []
    spawn_timer = 0
    click_processed = False
    
    # Hide system cursor
    pygame.mouse.set_visible(False)
    
    @engine.game_loop
    def game_loop():
        nonlocal spawn_timer, click_processed
        
        mouse_pos = mouse.get_position()
        mouse_clicked = mouse.is_left_pressed()
        
        # Handle restart
        if state.game_over:
            if pygame.key.get_pressed()[pygame.K_r]:
                state.reset()
                targets.clear()
                effects.clear()
                spawn_timer = 0
        else:
            # Update time
            state.update_time(1 / FPS)
            
            # Spawn targets
            spawn_timer += 1
            if spawn_timer >= TARGET_SPAWN_INTERVAL and len(targets) < MAX_TARGETS:
                spawn_timer = 0
                new_target = spawn_target(targets)
                if new_target:
                    targets.append(new_target)
            
            # Update targets
            for target in targets[:]:
                if not target.update():
                    targets.remove(target)
            
            # Handle clicks
            if mouse_clicked and not click_processed:
                click_processed = True
                hit = False
                
                for target in targets[:]:
                    if target.contains_point(mouse_pos):
                        points = state.register_hit(target.points)
                        effects.append(HitEffect(
                            target.box_collider.centerx,
                            target.box_collider.centery,
                            f"+{points}",
                            GREEN
                        ))
                        targets.remove(target)
                        hit = True
                        break
                
                if not hit:
                    state.register_miss()
                    effects.append(HitEffect(mouse_pos[0], mouse_pos[1], "MISS", RED))
            
            if not mouse_clicked:
                click_processed = False
        
        # Update effects
        for effect in effects[:]:
            if not effect.update():
                effects.remove(effect)
        
        # Draw targets
        for target in targets:
            target.draw(canvas.surface)
        
        # Draw effects
        for effect in effects:
            effect.draw(canvas.surface, fonts['medium'])
        
        # Draw UI
        draw_ui(canvas.surface, state, fonts)
        
        # Draw crosshair (always on top)
        draw_crosshair(canvas.surface, mouse_pos)
        
        # Draw game over
        if state.game_over:
            draw_game_over(canvas.surface, state, fonts)


if __name__ == "__main__":
    try:
        main()
    finally:
        pygame.mouse.set_visible(True)
