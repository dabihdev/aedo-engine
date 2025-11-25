from storywriter import GameBuilder, GameData, Room, Item, NPC, Event
from settings import *

# INITIALIZE GAME
game_data = GameData("LOC1")

# RADURA
# ==============================================================================
radura = Room(
    "Radura dell'altare",
    "una radura con un antico altare in mezzo, ricoperto d'edera e licheni.",
    "LOC1")

# add exits
radura.add_exit("nord", "LOC2")
radura.add_exit("est", "LOC3")
radura.add_exit("sud", "LOC4")
radura.add_exit("ovest", "LOC5")

# Add location to game data
game_data.add_room(radura)

# ==============================================================================

# BOSCO FITTO
# ==============================================================================
bosco_fitto = Room(
    "Bosco fitto",
    "un bosco intricato, dove si fa fatica a passare.",
    "LOC2")

# add exits
bosco_fitto.add_exit("sud", "LOC1")

# add items
bosco_fitto.add_item(Item("bastone", "un bastone nodoso"))
bosco_fitto.add_item(Item("fungo", "un fungo di colore viola"))

# Add location to game data
game_data.add_room(bosco_fitto)

# ==============================================================================

# FIUME
# ==============================================================================
fiume = Room(
    "Fiume sassoso",
    "Un fiume con molti sassi, acqua cristallina e qualche pesciolino",
    "LOC3")

# add exits
fiume.add_exit("ovest", "LOC1")

# add items
fiume.add_item(Item("sasso", "un sasso levigato"))
fiume.add_item(Item("pesce", "un pesciolino"))

# Add location to game data
game_data.add_room(fiume)

# ==============================================================================

GameBuilder.save_game(game_data, GAMES_FOLDER+"my_adventure.json")