"""Handles saving and loading the GameData structure using JSON."""
import json
from .game_data import GameData

class GameBuilder:
    """Static methods for serializing the game world data."""

    @staticmethod
    def save_game(game_data: GameData, filename: str):
        """
        Saves the GameData object to a JSON file.

        Args:
            game_data: The fully constructed GameData object.
            filename: The path to the output JSON file.
        """
        try:
            with open(filename, 'w') as f:
                # Use to_dict() method of the root object for recursive serialization
                json.dump(game_data.to_dict(), f, indent=4)
            print(f"Game saved successfully to {filename}")
        except Exception as e:
            print(f"Error saving game: {e}")