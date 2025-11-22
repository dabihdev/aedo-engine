from engine.models import GameState, Location, Character
from typing import Optional, Dict
from .utils import clear_screen

class Engine:
    """
    The main class that initializes and runs the text-based adventure game.
    """

    def __init__(self, map_filename: str = "map_data", char_filename: str = "char_data"):
        """
        Initializes the game state and loads the map and character data.

        Args:
            map_filename: The base name of the map JSON file.
            char_filename: The base name of the character JSON file.
        """
        self.game_state = GameState()
        
        # Load Map
        self.game_state.map_from_json(map_filename)
        
        # Load Character
        self.game_state.character_from_json(char_filename)
        
        # Set starting location. Assumes a location with id "START" exists.
        if "START" in self.game_state.map:
            self.game_state.current_location_id = "START"
            print(f"Game initialized. Starting at: {self.game_state.map['START'].name}")
        else:
            print("Warning: No 'START' location found. Game may not function correctly.")
        
        self.running = True
        print("---")

    def _get_current_location(self) -> Optional[Location]:
        """Helper to get the current Location object."""
        return self.game_state.map.get(self.game_state.current_location_id)

    def show_location(self):
        """
        Displays the name, description, and available exits of the current location.
        """
        # First, clear the terminal screen to give the feeling of
        # changing scene, and avoid clusters of text which could make
        # everything incomprehensible.
        clear_screen()

        # Get current location
        current_loc = self._get_current_location()
        if not current_loc:
            print("\n!!! ERROR: Location not found. Game Over. !!!")
            self.running = False
            return

        # Display room
        print(f"\n{current_loc.name}")
        print("-" * (len(current_loc.name) + 18))
        print(current_loc.description)
        
        # Display Exits
        if current_loc.exits:
            exit_names = ", ".join(current_loc.exits.keys())
            print(f"\nAvailable Exits: {exit_names.capitalize()}")
        else:
            print("\nThere are no obvious exits.")


    def parse_input(self) -> Optional[Dict[str, str]]:
        """
        Receives user input and attempts to parse it into a command.

        Returns:
            A dictionary like {"command": "go", "target": "north"}, or None 
            if the command is "quit" or invalid.
        """
        user_input = input("> ").strip().lower()

        if user_input in {"quit", "exit"}:
            self.running = False
            return {"command": "quit"}

        parts = user_input.split()
        if not parts:
            return None

        # Basic movement command parsing (e.g., "go north", "north")
        if parts[0] in {"go", "move", "walk"} and len(parts) >= 2:
            return {"command": "move", "target": parts[-1]}
        elif parts[0] in self._get_current_location().exits.keys(): # Direct direction input
             return {"command": "move", "target": parts[0]}

        print("I don't understand that command. Try 'go [direction]' or 'quit'.")
        return None

    def update_gamestate(self, parsed_command: Optional[Dict[str, str]]):
        """
        Updates the game state based on the parsed user command.

        Args:
            parsed_command: The dictionary containing the command and its target.
        """
        if not parsed_command:
            return

        command = parsed_command.get("command")
        
        if command == "quit":
            print("\nThanks for playing! Goodbye.")
            # self.running is already set to False in parse_input
            return

        if command == "move":
            direction = parsed_command.get("target")
            current_loc = self._get_current_location()
            
            if not current_loc:
                return # Handled in show_location

            if direction in current_loc.exits:
                next_location_id = current_loc.exits[direction]
                if next_location_id in self.game_state.map:
                    self.game_state.current_location_id = next_location_id
                    # The new location will be shown in the next loop iteration
                else:
                    print(f"There's an exit {direction}, but the destination location ID '{next_location_id}' is missing from the map data!")
            else:
                print(f"You cannot go {direction} from here.")

    def run(self):
        """
        The main game loop.
        """
        while self.running:
            # 1. Render game
            self.show_location()
            if not self.running: # Check if show_location set running to False
                break
            
            # 2. Get input from player
            command = self.parse_input()

            # 3. Update game state
            if command:
               self.update_gamestate(command)