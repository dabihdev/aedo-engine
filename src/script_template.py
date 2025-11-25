from storywriter import GameBuilder, GameData, Room, Item, NPC, Event
from settings import *

# INITIALIZE GAME
game_data = GameData("LOC1")

# LOCATION NAME:
# ========================================================================

# Create enemies and npcs
# ...

# Create items
# ...

# Create events
# ...

# Create location
# ...
# add exits
# add enemies/npcs to location
# add items to location
# add events to location

# Add location to game data
# ...

# ========================================================================

# When you finished building your level, save it
GameBuilder.save_game(game_data, GAMES_FOLDER+"my_adventure.json")