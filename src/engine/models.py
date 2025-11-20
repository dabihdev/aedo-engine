from typing import Any, Dict, List, Optional
import json
from pathlib import Path

# Define the path for the games data folder
GAME_DATA_FOLDER = Path(__file__).parent.parent / "games"

class Location:
    """
    Represents a single location or room in the game map during runtime.
    """
    def __init__(self, id: str, name: str, description: str, exits: Dict[str, str] = None):
        """
        Initializes a Location.

        Args:
            id: A unique string identifier for the location.
            name: The display name of the location.
            description: A detailed description of the location.
            exits: A dictionary where keys are directions and values are the IDs 
                   of the linked location.
        """
        self.id = id
        self.name = name
        self.description = description
        self.exits = exits if exits is not None else {}

    def add_exit(self, direction: str, location_id: str):
        """
        Adds a single exit to the location.

        Args:
            direction: The direction of the exit (e.g., "north").
            location_id: The ID of the location the exit leads to.
        """
        self.exits[direction] = location_id

    def remove_exit(self, direction: str):
        """
        Removes an exit from the location. Useful for locking/closing doors.

        Args:
            direction: The direction of the exit to remove.
        """
        if direction in self.exits:
            del self.exits[direction]

class Character:
    """
    Represents the player character in the game during runtime.
    """
    def __init__(self, stats: Dict[str, Any] = None):
        """
        Initializes the Character with a set of statistics.

        Args:
            stats: A dictionary defining the character's properties.
        """
        self.stats = stats if stats is not None else {}

    def update_stats(self, new_stats: Dict[str, Any]):
        """
        Updates one or more stats in the character's stats dictionary.

        Args:
            new_stats: A dictionary of stats to update.
        """
        self.stats.update(new_stats)

class GameState:
    """
    Manages the overall state of the game during runtime.
    """
    def __init__(self, map_name: str = ""):
        """
        Initializes the GameState with default empty values.

        Args:
            map_name: The name of the game/map/level.
        """
        self.map_name = map_name
        self.character: Optional[Character] = None
        self.current_location_id: str = ""
        # Map: keys are location IDs, values are Location objects
        self.map: Dict[str, Location] = {} 

    def map_from_json(self, filename: str = "map_data") -> Dict[str, Location]:
        """
        Reads the map data from a JSON file and populates the self.map dictionary.

        Args:
            filename: The base name of the map JSON file (e.g., "map_data").

        Returns:
            The populated dictionary of Location objects, with IDs as keys.
        """
        file_path = GAME_DATA_FOLDER / f"{filename}.json"
        
        try:
            with file_path.open("r", encoding="utf-8") as f:
                map_data_list: List[Dict[str, Any]] = json.load(f)
        except FileNotFoundError:
            print(f"Error: Map file not found at {file_path}")
            return {}

        for loc_data in map_data_list:
            loc = Location(
                id=loc_data["id"],
                name=loc_data["name"],
                description=loc_data["description"],
                exits=loc_data["exits"]
            )
            self.map[loc.id] = loc
        
        print("Map data loaded successfully.")
        return self.map

    def character_from_json(self, filename: str = "char_data") -> Optional[Character]:
        """
        Reads the character stats from a JSON file and creates a Character object.

        Args:
            filename: The base name of the character JSON file (e.g., "char_data").
        
        Returns:
            The created Character object, or None if the file is not found.
        """
        file_path = GAME_DATA_FOLDER / f"{filename}.json"

        try:
            with file_path.open("r", encoding="utf-8") as f:
                char_stats: Dict[str, Any] = json.load(f)
        except FileNotFoundError:
            print(f"Error: Character file not found at {file_path}")
            return None
        
        self.character = Character(stats=char_stats)
        print("Character data loaded successfully.")
        return self.character