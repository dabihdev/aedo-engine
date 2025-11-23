"""Handles user input parsing and execution of game commands and events."""
from typing import Dict, Any
from .player import Player

class Command:
    """Static class for processing user commands and events."""

    @staticmethod
    def execute_event(event_data: Dict[str, Any], player: Player, game_map: Dict[str, Any]):
        """
        Executes the logic based on the event_type.

        Args:
            event_data: The dictionary representation of the Event.
            player: The runtime Player object.
            game_map: The current state of the game map (for item modification).
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
            
            if required_key and not player.is_carrying(required_key):
                print(f"The chest is locked. It requires a {required_key}.")
                return

            print("The chest opens with a deep thud.")
            for item in data.get('items', []):
                # Add item to player's inventory
                player.take_item(item)
            
            # TODO: Remove chest from room after opening (requires updating Room structure)
            
        else:
            print(f"System Error: Unknown event type '{event_type}'.")


    @staticmethod
    def process(command_input: str, player: Player, game_map: Dict[str, Any], all_events: Dict[str, Any]) -> bool:
        """
        Processes the user input and modifies the game state.

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

        current_room_data = game_map[player.current_room_id]

        if verb in ["quit", "exit"]:
            return False

        elif verb == "go":
            if noun in current_room_data['exits']:
                player.current_room_id = current_room_data['exits'][noun]
                # Print room description upon moving
                print(f"You move {noun}...")
            else:
                print("You can't go that way.")

        elif verb == "look":
            print(f"\nLocation: {current_room_data['name']}")
            print(current_room_data['description'])
            
            # Show items
            if current_room_data['items']:
                print("You see items:", ", ".join([i['name'] for i in current_room_data['items']]))
            
            # Show interactive objects
            if current_room_data['interactive_objects']:
                print("You notice:", ", ".join(current_room_data['interactive_objects'].keys()))
            
            # Show people
            people = [e['name'] for e in current_room_data['enemies']] + [n['name'] for n in current_room_data['npcs']]
            if people:
                print("People present:", ", ".join(people))
        
        elif verb == "take":
            item_to_take = next((i for i in current_room_data['items'] if i['name'].lower() == noun), None)
            
            if item_to_take:
                if item_to_take.get('can_take', True):
                    # Remove from room and add to player
                    current_room_data['items'].remove(item_to_take)
                    player.take_item(item_to_take)
                else:
                    print(f"The {item_to_take['name']} is too heavy or fixed in place.")
            else:
                print(f"I don't see a '{noun}' here.")

        elif verb in ["inventory", "inv"]:
            player.show_inventory()

        # --- Interactive Commands ---
        elif verb == "talk":
            target_npc = next((n for n in current_room_data['npcs'] if n['name'].lower() == noun), None)
            
            if target_npc:
                dialogue_id = target_npc.get('dialogue_id')
                event_data = all_events.get(dialogue_id)
                if event_data:
                    Command.execute_event(event_data, player, game_map)
                else:
                    print(f"{target_npc['name']} just nods silently.")
            else:
                print("Talk to whom?")

        elif verb in ["read", "open"]:
            if noun in current_room_data['interactive_objects']:
                event_id = current_room_data['interactive_objects'][noun]
                event_data = all_events.get(event_id)
                
                # Check if the event type matches the command (e.g., cannot 'read' a 'chest')
                if event_data and event_data['event_type'] == verb:
                    Command.execute_event(event_data, player, game_map)
                else:
                    print(f"You can't '{verb}' the {noun}.")
            else:
                print(f"{verb.capitalize()} what?")

        # TODO: Implement 'fight' command logic for enemies

        else:
            print(f"I don't understand that command: '{command_input}'.")
        
        return True