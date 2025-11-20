# 1) Import necessary modules and classes
from models import Location, Character, GameState

# --- GAME CREATION START ---

# 2) GameState instantiation
game = GameState(name="My First Text Adventure", current_location="START")
print(f"Creating game: {game.name}")
print("---")

# 3) Location instantiation and exit definition (TEMPLATE SECTION)

# Location 1: START
start_loc = Location(
    id="START", 
    name="The Dusty Attic", 
    description="You wake up in a small, dusty attic. Cobwebs cling to the rafters. "
                "A single door leads downstairs."
)
start_loc.add_exits({"down": "hallway"})
game.add_location(start_loc)

# Location 2: Hallway
hallway = Location(
    id="hallway",
    name="Ground Floor Hallway",
    description="A long, empty hallway with faded wallpaper. To the east is a kitchen "
                "and a staircase leads back up."
)
hallway.add_exits({
    "up": "START", 
    "east": "kitchen"
})
game.add_location(hallway)

# Location 3: Kitchen
kitchen = Location(
    id="kitchen",
    name="The Kitchen",
    description="A surprisingly clean kitchen with a large wooden table. A window looks "
                "out onto a dark garden. The hallway is to the west."
)
kitchen.add_exits({"west": "hallway"})
game.add_location(kitchen)

# 4) Character instantiation and stat definition (TEMPLATE SECTION)
player_char = Character()
player_char.add_stats({
    "name": "Player One",
    "HP": 100,
    "MP": 50,
    "current_inventory": [] # Not used in V1, but ready for V2
})

print("Map Locations:")
for loc in game.map:
    print(f"- {loc.id}: {loc.name}")
print("---")
print(f"Character Name: {player_char.stats.get('name')}")
print("---")


# 5) Save the GameState to JSON files
# Note: The output_filename arguments are optional, using defaults here.
game.map_to_json(output_filename="map_data")
game.character_to_json(player_char, output_filename="char_data")

# --- GAME CREATION END ---