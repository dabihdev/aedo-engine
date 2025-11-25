from storyteller import GameEngine
from settings import *

if __name__=="__main__":
    # Initialize game engine
    engine = GameEngine()
    
    if engine.load_game(GAMES_FOLDER+"my_adventure.json"):
        engine.run()