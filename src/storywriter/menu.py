class Menu:
    """
    Base class for all menus in the text-based adventure game.

    Provides basic structure for displaying options and handling input.
    """
    def __init__(self, title, options):
        """
        Initializes the Menu object.

        Args:
            title (str): The title of the menu (e.g., "Settings").
            options (list[str]): A list of strings representing the menu choices.
        """
        self.title = title
        self.options = options
        
    def display_menu(self):
        """
        Prints the menu title and the numbered options to the console.
        """
        print(f"\n--- {self.title.upper()} ---")
        for i, option in enumerate(self.options, 1):
            print(f"[{i}] {option}")
        print("-" * (len(self.title) + 12)) # Simple separator line

    def get_user_choice(self) -> int:
        """
        Prompts the user for input and validates the choice.

        The validation ensures the input is an integer within the valid range
        of the available menu options.
        
        Returns:
            int: The validated integer index (1-based) of the user's choice.
        """
        num_options = len(self.options)
        while True:
            # Display the prompt for user input
            choice_str = input(">>> Enter your choice: ")
            
            try:
                choice = int(choice_str)
                # Check if the number is within the valid range of options
                if 1 <= choice <= num_options:
                    return choice
                else:
                    print(f"Invalid choice. Please enter a number between 1 and {num_options}.")
            except ValueError:
                print("Invalid input. Please enter a number.")

    def run(self):
        """
        Displays the menu, handles user input, and returns the validated choice.

        Returns:
            int: The validated integer index (1-based) of the user's selected option.
        """
        self.display_menu()
        return self.get_user_choice()
    

class MainMenu(Menu):
    """
    The main menu for the game, inheriting from the base Menu class.
    
    Contains standard options like New Game, Load Game, and Quit Game.
    """
    def __init__(self, game_title="A Text Adventure Game"):
        """
        Initializes the Main Menu with the game title and fixed options.

        Args:
            game_title (str, optional): The title of the game to display. 
                Defaults to "A Text Adventure Game".
        """
        # The options for the Main Menu
        main_menu_options = [
            "New Game",
            "Load Game",
            "Quit Game"
        ]
        
        # Call the parent class's constructor
        super().__init__(game_title, main_menu_options)

    def handle_choice(self, choice):
        """
        Executes an action based on the user's choice.

        This method is a template for the user to modify to integrate
        with the main game loop and functionality.
        
        Args:
            choice (int): The integer choice (1-based) returned by run().

        Returns:
            str or None: A string indicating the action taken (e.g., "Starting..."),
                         or ``None`` if the action was 'Quit Game'.
        """
        if choice == 1:
            return "Starting a New Game..."
        elif choice == 2:
            return "Loading a Saved Game..."
        elif choice == 3:
            print("Thanks for playing! Exiting.")
            return None # Signal to stop the loop
        else:
            # This should generally not be reached
            return "Error: Unknown choice."

    def run(self):
        """
        Overrides the base run method to repeatedly display the menu 
        and handle choices until a terminal action (like Quit) is selected.
        
        This method manages the primary interaction loop for the Main Menu.

        Returns:
            int or None: The final choice made by the user if the menu exits
                         (e.g., the Quit option's index), or ``None`` if the
                         menu successfully led to a state change (like New Game).
        """
        while True:
            choice = super().run()
            action_result = self.handle_choice(choice)
            
            if action_result is None:
                # Quit Game was chosen
                return choice
            elif action_result:
                print(action_result)
                
                # Assume selecting 'New Game' or 'Load Game' successfully exits the menu loop
                # and transfers control back to the main game logic.
                if choice in [1, 2]: 
                    return choice