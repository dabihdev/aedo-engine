import json
from pathlib import Path
from typing import Any, Dict, List

# Define the path for the games data folder
GAME_DATA_FOLDER = Path(__file__).parent.parent / "games"

class Location:
    """
    Represents a single location or room in the game map.
    """
    def __init__(self, id: str, name: str, description: str, exits: Dict[str, str] = None):
        """
        Initializes a Location.

        Args:
            id: A unique string identifier for the location.
            name: The display name of the location.
            description: A detailed description of the location.
            exits: A dictionary where keys are directions (e.g., "north") 
                   and values are the IDs of the linked location.
        """
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits if exits is not None else {}

    def add_exits(self, new_exits: Dict[str, str]):
        """
        Adds one or more exits to the location's exits dictionary.

        Args:
            new_exits: A dictionary of new exits to add (e.g., {"north": "loc_002"}).
        """
        self.exits.update(new_exits)

    def to_dict(self) -> Dict[str, Any]:
        """Converts the Location object into a dictionary for JSON serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "exits": self.exits,
        }

class Character:
    """
    Represents the player character in the game.
    """
    def __init__(self, stats: Dict[str, Any] = None):
        """
        Initializes the Character with a set of statistics.

        Args:
            stats: A dictionary defining the character's properties 
                   (e.g., {"name": "Hero", "HP": 100, "inventory": []}).
        """
        self.stats = stats if stats is not None else {}

    def add_stats(self, new_stats: Dict[str, Any]):
        """
        Adds one or more stats to the character's stats dictionary.

        Args:
            new_stats: A dictionary of new stats to add or existing stats to update.
        """
        self.stats.update(new_stats)

class GameState:
    """
    Manages the overall state of the game during creation.
    """
    def __init__(self, name: str, current_location: str = "START"):
        """
        Initializes the GameState.

        Args:
            name: The name of the game/map/level.
            current_location: The starting location ID (default "START").
        """
        self.name = name
        self.current_location = current_location
        self.map: List[Location] = []

    def add_location(self, loc: Location):
        """
        Adds a Location object to the game map list.

        Args:
            loc: The Location object to add.
        """
        self.map.append(loc)

    def map_to_json(self, output_filename: str = "map_data"):
        """
        Serializes the game map (list of Location objects) to a JSON file.

        The JSON file is saved in the 'src/games/' folder.

        Args:
            output_filename: The base name for the output file (e.g., "map_data" becomes 
                             "map_data.json").
        """
        GAME_DATA_FOLDER.mkdir(exist_ok=True)
        
        map_list_of_dicts = [loc.to_dict() for loc in self.map]
        
        output_file_path = GAME_DATA_FOLDER / f"{output_filename}.json"
        with output_file_path.open("w", encoding="utf-8") as f:
            json.dump(map_list_of_dicts, f, indent=4)
        print(f"Map successfully saved to {output_file_path}")

    def character_to_json(self, character: Character, output_filename: str = "char_data"):
        """
        Stores the Character's stats dictionary to a JSON file.

        The JSON file is saved in the 'src/games/' folder.

        Args:
            character: The Character object whose stats are to be saved.
            output_filename: The base name for the output file.
        """
        GAME_DATA_FOLDER.mkdir(exist_ok=True)
        
        output_file_path = GAME_DATA_FOLDER / f"{output_filename}.json"
        with output_file_path.open("w", encoding="utf-8") as f:
            json.dump(character.stats, f, indent=4)
        print(f"Character stats successfully saved to {output_file_path}")