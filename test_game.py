import sys
# Internal modules
from EasyPygame.actors import Player, Character
from EasyPygame.game_engine import Engine, Canvas

# Initialization of all game related objects. Think 'void Setup()' for all my Unity devs c:
canvas = Canvas(screen_size = (400,400), background_color = (0,0,0))
engine = Engine(fps=60, canvas=canvas)

player = Player(spawn_coordinates=(engine.canvas.screen_size[0]//2, engine.canvas.screen_size[1]-20), size=50)
character = Character(spawn_coordinates=(engine.canvas.screen_size[0]//2, 0), size=50, sprite="Fantasy RPG NPCs - Individual Frames\Alchemist\Alchemist_Idle_1.png")

char_list = [player,character]
# Repeats following code until told otherwise. AKA 'void Loop()'
@engine.game_loop #All in game logic must come after this decorator.
def loop():
    for actor in char_list:
        actor.draw(engine.canvas.surface)
        if type(actor) == Player:
            actor.handle_keys(canvas=engine.canvas)
        if player.check_collision([character]) and character in char_list:
            char_list.remove(character)