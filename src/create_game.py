from game_builder import GameBuilder, GameData, Room, Item, NPC, Event
from settings import *

# --- 1. Define Events ---
dialogue_a = Event("old_man_chat", "dialogue", {
    "speaker": "Old Gatekeeper",
    "lines": [
        "Hello, traveler. The ruins are dangerous.", 
        "Only the bravest seek the Sunstone Key.",
        "It's said to be hidden in the eastern tower."
    ]
})

inscription_read = Event("ruin_inscription", "read", {
    "text": "The past is a lock, the present is the key. Seek what is hidden."
})

chest_event = Event("chest_vault", "chest", {
    "key_name": "Sunstone Key",
    "items": [
        Item("Ancient Sword", "A magnificent sword, still sharp.", can_take=True).to_dict(),
        Item("Gold Coin", "A single gold coin.", can_take=True).to_dict()
    ]
})

# --- 2. Define Entities ---
sunstone_key = Item("Sunstone Key", "A strange, warm key made of polished orange stone.", can_take=True)
gatekeeper = NPC("Gatekeeper", dialogue_id="old_man_chat")

# --- 3. Define Rooms ---
room_1 = Room("Western Gate", "You stand before a towering iron gate, guarded by an old man.", "room_1")
room_2 = Room("Central Courtyard", "A vast, crumbling courtyard. A worn inscription marks a statue base.", "room_2")
room_3 = Room("Eastern Tower Base", "The base of a collapsed tower. A locked chest sits in the corner.", "room_3")

# --- 4. Add Items/NPCs/Events to Rooms ---
room_1.add_npc(gatekeeper)
room_1.add_item(Item("Worn Sign", "A sign reads: 'Keep Out'.", can_take=False))

room_2.add_item(sunstone_key)
room_2.add_interactive_object("inscription", "ruin_inscription") # Read command uses "inscription"

room_3.add_interactive_object("chest", "chest_vault") # Open command uses "chest"

# --- 5. Define Exits ---
room_1.add_exit("east", "room_2")
room_2.add_exit("west", "room_1")
room_2.add_exit("east", "room_3")
room_3.add_exit("west", "room_2")

# --- 6. Create and Save Game Data ---
game_data = GameData(start_room_id="room_1")
game_data.add_room(room_1)
game_data.add_room(room_2)
game_data.add_room(room_3)

game_data.add_event(dialogue_a)
game_data.add_event(inscription_read)
game_data.add_event(chest_event)

GameBuilder.save_game(game_data, GAMES_FOLDER+"my_adventure.json")