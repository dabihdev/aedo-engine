"""
Defines the core object-oriented models for the game world.

These classes are designed to be easily serialized to a JSON format.
"""

class Item:
    """Represents a passive object in the game world."""
    def __init__(self, name: str, description: str, can_take: bool = True):
        """
        Initializes an Item object.

        Args:
            name: The display name of the item (e.g., "Rusty Key").
            description: The text shown when the player examines the item.
            can_take: Whether the player can pick up the item.
        """
        self.name = name
        self.description = description
        self.can_take = can_take

    def to_dict(self) -> dict:
        """Converts the object to a dictionary for serialization."""
        return self.__dict__

class Character:
    """Base class for all sentient entities (Player, Enemy, NPC)."""
    def __init__(self, name: str, health: int):
        """
        Initializes a Character object.

        Args:
            name: The display name of the character.
            health: The current health points of the character.
        """
        self.name = name
        self.health = health
    
    def to_dict(self) -> dict:
        """Converts the object to a dictionary for serialization."""
        return self.__dict__

class Enemy(Character):
    """Represents a hostile character in the game."""
    def __init__(self, name: str, health: int, attack_power: int, reward_item_name: str = None):
        """
        Initializes an Enemy object.

        Args:
            name: The display name of the enemy.
            health: The starting health points.
            attack_power: Damage the enemy deals.
            reward_item_name: Name of the item dropped upon defeat.
        """
        super().__init__(name, health)
        self.attack_power = attack_power
        self.reward_item_name = reward_item_name 

    def to_dict(self) -> dict:
        """Converts the object to a dictionary for serialization."""
        return self.__dict__

class NPC(Character):
    """Represents a non-player character, typically for interaction."""
    def __init__(self, name: str, dialogue_id: str, trigger_event_id: str = None):
        """
        Initializes an NPC object.

        Args:
            name: The display name of the NPC.
            dialogue_id: Key referencing a Dialogue Event in GameData.events.
            trigger_event_id: Event triggered after the dialogue completes (optional).
        """
        # NPCs are usually not fightable in simple games, setting health to 1
        super().__init__(name, 1) 
        self.dialogue_id = dialogue_id
        self.trigger_event_id = trigger_event_id

    def to_dict(self) -> dict:
        """Converts the object to a dictionary for serialization."""
        return {"name": self.name, "dialogue_id": self.dialogue_id, 
                "trigger_event_id": self.trigger_event_id}


class Event:
    """
    Represents an interactive event (dialogue, reading, opening).
    
    The 'data' dictionary holds specific content based on 'event_type'.
    """
    def __init__(self, event_id: str, event_type: str, data: dict):
        """
        Initializes an Event object.

        Args:
            event_id: Unique identifier for the event.
            event_type: The type of event ('dialogue', 'read', 'chest').
            data: The content or requirements for the event (e.g., lines of text, key name).
        """
        self.event_id = event_id
        self.event_type = event_type
        self.data = data
    
    def to_dict(self) -> dict:
        """Converts the object to a dictionary for serialization."""
        return self.__dict__


class Room:
    """Represents a location in the game world."""
    def __init__(self, name: str, description: str, room_id: str):
        """
        Initializes a Room object.

        Args:
            name: The display name of the room.
            description: The text shown when the player enters.
            room_id: Unique identifier for the room (used for exits).
        """
        self.room_id = room_id
        self.name = name
        self.description = description
        self.exits = {}         # {"direction": "target_room_id"}
        self.items = []         # List of Item objects
        self.enemies = []       # List of Enemy objects
        self.npcs = []          # List of NPC objects
        self.interactive_objects = {} # Map names to event IDs: {"chest": "chest_1", "inscription": "text_1"}
    
    def add_exit(self, direction: str, target_room_id: str):
        """Adds a directional exit to another room ID."""
        self.exits[direction] = target_room_id

    def add_item(self, item: Item):
        """Adds an Item object to the room."""
        self.items.append(item)

    def add_enemy(self, enemy: Enemy):
        """Adds an Enemy object to the room."""
        self.enemies.append(enemy)

    def add_npc(self, npc: NPC):
        """Adds an NPC object to the room."""
        self.npcs.append(npc)
        
    def add_interactive_object(self, name: str, event_id: str):
        """Adds an object that triggers an Event (e.g., chest, book, sign)."""
        self.interactive_objects[name] = event_id

    def to_dict(self) -> dict:
        """Converts the Room and its contents to a dictionary for serialization."""
        return {
            "room_id": self.room_id,
            "name": self.name,
            "description": self.description,
            "exits": self.exits,
            "items": [item.to_dict() for item in self.items],
            "enemies": [e.to_dict() for e in self.enemies],
            "npcs": [n.to_dict() for n in self.npcs],
            "interactive_objects": self.interactive_objects
        }


class GameData:
    """The root container class holding all game data."""
    def __init__(self, start_room_id: str):
        """
        Initializes the main GameData object.

        Args:
            start_room_id: The ID of the room where the game starts.
        """
        self.rooms = {}
        self.events = {}
        self.start_room_id = start_room_id

    def add_room(self, room: Room):
        """Adds a Room object to the game map."""
        self.rooms[room.room_id] = room

    def add_event(self, event: Event):
        """Adds an Event object to the central event store."""
        self.events[event.event_id] = event

    def to_dict(self) -> dict:
        """Converts the entire game structure to a dictionary."""
        return {
            "start_room_id": self.start_room_id,
            "rooms": {id: room.to_dict() for id, room in self.rooms.items()},
            "events": {id: event.to_dict() for id, event in self.events.items()}
        }