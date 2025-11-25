"""
Implements the Command Pattern for processing user input.

This file defines the base command class and the router that dispatches commands.
"""
from typing import Dict, Any, List
from .player import Player

# --- BASE COMMAND CLASS ---

class BaseCommand:
    """The abstract base class for all commands."""
    
    VERB: List[str] = [] # The keywords that trigger this command (e.g., ['go', 'move'])
    
    def __init__(self, player: Player, game_map: Dict[str, Any], all_events: Dict[str, Any]):
        """Initializes the command with access to game state."""
        self.player = player
        self.game_map = game_map
        self.all_events = all_events
        self.current_room_data = game_map[player.current_room_id]

    def execute(self, noun: str) -> bool:
        """
        Executes the specific logic of the command.
        
        Args:
            noun: The direct object of the command (e.g., 'north' for 'go north').
            
        Returns:
            True to continue the game loop, False to quit.
        """
        raise NotImplementedError("Subclasses must implement the execute method.")
    
    def _execute_event(self, event_data: Dict[str, Any]):
        """
        Helper method (copied logic) to execute events centrally.
        
        Args:
            event_data: The dictionary representation of the Event.
        """
        event_type = event_data['event_type']
        data = event_data['data']

        if event_type == "dialogue":
            print(f"\n--- Dialogue with {data.get('speaker', 'Stranger')} ---")
            for line in data.get('lines', []):
                print(f"  > {line}")
            print("---------------------------------")

        elif event_type == "read":
            print("\nYou read:")
            print(f"  *** {data.get('text', 'The text is too faded to read.')} ***")

        elif event_type == "chest":
            required_key = data.get('key_name')
            
            if required_key and not self.player.is_carrying(required_key):
                print(f"The chest is locked. It requires a {required_key}.")
                return

            print("The chest opens with a deep thud.")
            for item in data.get('items', []):
                self.player.take_item(item)
            # TODO: Add logic to remove the chest from the room after opening.
            
        else:
            print(f"System Error: Unknown event type '{event_type}'.")


# --- SPECIFIC COMMAND IMPLEMENTATIONS ---

class GoCommand(BaseCommand):
    """Handles movement between rooms."""
    VERB = ['go', 'move']
    
    def execute(self, noun: str) -> bool:
        if noun in self.current_room_data['exits']:
            self.player.current_room_id = self.current_room_data['exits'][noun]
            # Print room description upon moving is now handled by the Engine loop
            print(f"You move {noun}...")
        else:
            print("You can't go that way.")
        return True # Continue game


class TakeCommand(BaseCommand):
    """Handles picking up items."""
    VERB = ['take', 'get', 'pick up']
    
    def execute(self, noun: str) -> bool:
        item_to_take = next((i for i in self.current_room_data['items'] if i['name'].lower() == noun), None)
        
        if item_to_take:
            if item_to_take.get('can_take', True):
                # Remove from room and add to player
                self.current_room_data['items'].remove(item_to_take)
                self.player.take_item(item_to_take)
            else:
                print(f"The {item_to_take['name']} is too heavy or fixed in place.")
        else:
            print(f"I don't see a '{noun}' here.")
        return True

class TalkCommand(BaseCommand):
    """Handles talking to NPCs."""
    VERB = ['talk']

    def execute(self, noun: str) -> bool:
        target_npc = next((n for n in self.current_room_data['npcs'] if n['name'].lower() == noun), None)
        
        if target_npc:
            dialogue_id = target_npc.get('dialogue_id')
            event_data = self.all_events.get(dialogue_id)
            if event_data:
                self._execute_event(event_data)
            else:
                print(f"{target_npc['name']} just nods silently.")
        else:
            print("Talk to whom?")
        return True
    
class OpenCommand(BaseCommand):
    """Handles opening interactive objects like chests."""
    VERB = ['open']

    def execute(self, noun: str) -> bool:
        if noun in self.current_room_data['interactive_objects']:
            event_id = self.current_room_data['interactive_objects'][noun]
            event_data = self.all_events.get(event_id)
            
            if event_data and event_data['event_type'] == 'chest':
                self._execute_event(event_data)
            else:
                print(f"You can't 'open' the {noun}.")
        else:
            print("Open what?")
        return True

class ReadCommand(BaseCommand):
    """Handles reading interactive objects like signs or inscriptions."""
    VERB = ['read']

    def execute(self, noun: str) -> bool:
        if noun in self.current_room_data['interactive_objects']:
            event_id = self.current_room_data['interactive_objects'][noun]
            event_data = self.all_events.get(event_id)
            
            if event_data and event_data['event_type'] == 'read':
                self._execute_event(event_data)
            else:
                print(f"You can't 'read' the {noun}.")
        else:
            print("Read what?")
        return True

class LookCommand(BaseCommand):
    """Handles looking around (re-displaying room details)."""
    VERB = ['look']

    def execute(self, noun: str) -> bool:
        # Note: The Engine will call display_current_room() after any movement.
        # This command is for explicit 'look' command.
        print(f"\nLocation: {self.current_room_data['name']}")
        print(self.current_room_data['description'])
        
        items = [i['name'] for i in self.current_room_data['items']]
        objects = list(self.current_room_data['interactive_objects'].keys())
        enemies = [e['name'] for e in self.current_room_data['enemies']]
        npcs = [n['name'] for n in self.current_room_data['npcs']]
        
        if items: print("You see items:", ", ".join(items))
        if objects: print("You notice:", ", ".join(objects))
        if enemies: print(f"DANGER! Enemies present: {', '.join(enemies)}")
        if npcs: print("People present:", ", ".join(npcs))

        return True

class InventoryCommand(BaseCommand):
    """Handles checking the player's inventory."""
    VERB = ['inventory', 'inv']
    
    def execute(self, noun: str) -> bool:
        self.player.show_inventory()
        return True

class QuitCommand(BaseCommand):
    """Handles quitting the game."""
    VERB = ['quit', 'exit']
    
    def execute(self, noun: str) -> bool:
        return False # Signal to stop the game loop

# --- COMMAND DISPATCHER / FACTORY ---

class CommandProcessor:
    """Routes the raw user input to the correct command class."""

    # Register all concrete command classes here
    _COMMANDS = [
        GoCommand, TakeCommand, TalkCommand, OpenCommand, ReadCommand, 
        LookCommand, InventoryCommand, QuitCommand
    ]
    
    # Create a mapping of verb string to Command Class for fast lookup
    _VERB_MAP = {}
    for cmd_class in _COMMANDS:
        for verb in cmd_class.VERB:
            _VERB_MAP[verb] = cmd_class

    @staticmethod
    def process(command_input: str, player: Player, game_map: Dict[str, Any], all_events: Dict[str, Any]) -> bool:
        """
        Parses input and executes the relevant command class.

        Args:
            command_input: The raw string input from the user.
            player: The runtime Player object.
            game_map: The current game map data.
            all_events: A dictionary of all global events.

        Returns:
            True if the game should continue, False if the game should quit.
        """
        parts = command_input.lower().split()
        if not parts:
            return True

        verb = parts[0]
        noun = " ".join(parts[1:])

        command_class = CommandProcessor._VERB_MAP.get(verb)
        
        if command_class:
            # Instantiate the command object and execute it
            command_instance = command_class(player, game_map, all_events)
            return command_instance.execute(noun)
        else:
            print(f"I don't understand that command: '{command_input}'.")
            return True # Continue game

# Rename the old Command class to CommandProcessor for clarity.
Command = CommandProcessor