"""The runtime representation of the player state."""

class Player:
    """Manages the player's position, inventory, and combat stats."""
    def __init__(self, start_room_id: str):
        """
        Initializes the Player state.

        Args:
            start_room_id: The ID of the room where the player begins.
        """
        self.current_room_id = start_room_id
        self.inventory = [] # List of item dicts
        self.health = 100
        self.attack_power = 10
        self.is_in_combat = False

    def take_item(self, item_dict: dict):
        """
        Adds an item dictionary to the player's inventory.
        
        Args:
            item_dict: The dictionary representation of the item.
        """
        self.inventory.append(item_dict)
        print(f"You took the {item_dict['name']}.")

    def show_inventory(self):
        """Prints the contents of the player's inventory."""
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("Inventory:", ", ".join([item['name'] for item in self.inventory]))

    def is_carrying(self, item_name: str) -> bool:
        """Checks if the player has a specific item."""
        return any(item['name'].lower() == item_name.lower() for item in self.inventory)