from storyteller import GameEngine
from settings import *

if __name__=="__main__":
    # Initialize game engine
    engine = GameEngine()

    # Load the game and run it
    # FUTURE IMPLEMENTATION: add menu with following sections:
    # > Game title
    # > New Game
    # > Load Game
    # > Quit Game
    # > user input
    # Create a Menu class in the builder subpackage: the user should be able
    # to create custom menus
    
    if engine.load_game(GAMES_FOLDER+"my_adventure.json"):
        engine.run()