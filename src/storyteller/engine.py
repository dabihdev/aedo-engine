"""The main game engine, managing the load, loop, and display."""
import json
from typing import Dict, Any
from .player import Player
from .command import Command

class GameEngine:
    """
    The main controller for the text adventure game.
    
    Handles loading the game map and running the interactive loop.
    """
    def __init__(self):
        """Initializes the engine state."""
        self.game_map: Dict[str, Any] = {}
        self.all_events: Dict[str, Any] = {}
        self.player: Player = None
        self.is_running = False

    def load_game(self, filename: str) -> bool:
        """
        Loads the game data from a JSON file and initializes the Player.

        Args:
            filename: The path to the game data file.

        Returns:
            True if the game loaded successfully, False otherwise.
        """
        try:
            with open(filename, 'r') as f:
                game_data = json.load(f)
            
            self.game_map = game_data.get('rooms', {})
            self.all_events = game_data.get('events', {})
            start_room_id = game_data.get('start_room_id')
            
            if not start_room_id or start_room_id not in self.game_map:
                print("Error: Start room is invalid or missing.")
                return False

            self.player = Player(start_room_id)
            self.is_running = True
            print(f"Game loaded successfully from {filename}.")
            return True
        except FileNotFoundError:
            print(f"Error: Game file '{filename}' not found.")
            return False
        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON data from '{filename}'. Check file integrity.")
            return False

    def display_current_room(self):
        """Displays the name and description of the player's current room."""
        current_room_data = self.game_map[self.player.current_room_id]
        print(f"\n=====================================")
        print(f"LOCATION: {current_room_data['name'].upper()}")
        print(f"HEALTH: {self.player.health}")
        print(f"=====================================")
        
        print(current_room_data['description'])
        
        # Summarize contents
        items = [i['name'] for i in current_room_data['items']]
        objects = list(current_room_data['interactive_objects'].keys())
        enemies = [e['name'] for e in current_room_data['enemies']]
        npcs = [n['name'] for n in current_room_data['npcs']]
        exits = list(current_room_data['exits'].keys())

        if items: print(f"Items: {', '.join(items)}")
        if objects: print(f"Objects: {', '.join(objects)}")
        if enemies: print(f"DANGER! Enemies present: {', '.join(enemies)}")
        if npcs: print(f"People: {', '.join(npcs)}")
        if exits: print(f"Exits: {', '.join(exits)}")
        print("-------------------------------------")


    def run(self):
        """Runs the main game loop."""
        if not self.is_running:
            print("Engine not ready. Please call load_game() first.")
            return

        self.display_current_room()

        while self.is_running:
            try:
                user_input = input("What do you do? (Type 'look' or 'quit') > ").strip()
                if not user_input:
                    continue

                # Process the command, which may update self.is_running
                continue_game = Command.process(user_input, self.player, self.game_map, self.all_events)
                
                if not continue_game:
                    self.is_running = False
                    break

                # After processing movement, display the new room description
                if user_input.lower().startswith("go"):
                    self.display_current_room()
                    
            except Exception as e:
                print(f"\n[SYSTEM ERROR]: An unhandled error occurred: {e}")
                print("The game state may be unstable. Try a different command.")

        print("\n*** Game Over. Thanks for playing! ***")