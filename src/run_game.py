from storyteller import GameEngine
from settings import *

if __name__=="__main__":
    # Initialize game engine
    engine = GameEngine()
    
    # Load game and run it
    if engine.load_game(GAMES_FOLDER+"my_adventure.json"):
        engine.run()