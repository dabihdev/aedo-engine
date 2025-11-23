from game_engine import GameEngine
from settings import *

engine = GameEngine()

if engine.load_game(GAMES_FOLDER+"my_adventure.json"):
    engine.run()