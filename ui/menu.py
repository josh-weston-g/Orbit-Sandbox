"""
Menu system using pygame_menu
"""

import pygame
import pygame_menu
from ui.game_state import GameState
from orbit.loader import SystemLoader

# Create a custom theme based on the dark theme
CUSTOM_THEME = pygame_menu.themes.THEME_DARK.copy()

# Customize theme
CUSTOM_THEME.widget_margin = (0, 15)  # Add margin around widgets (horizontal, vertical)

# Disable selection effect
CUSTOM_THEME.widget_selection_effect = pygame_menu.widgets.NoneSelection()  # No selection effect

def show_main_menu(screen):
    """
    Display the main menu.

    param: screen: The pygame display surface.

    return: The next state to transition to.
    """

    next_state = {"value": None}

    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    menu_width = screen_width - 10
    menu_height = screen_height - 10

    menu = pygame_menu.Menu(
        title="Orbit Sandbox",
        width=menu_width,
        height=menu_height,
        theme=CUSTOM_THEME
    )
    
    # Button functions
    def new_system():
        next_state["value"] = GameState.NEW_SYSTEM
        menu.disable()

    def load_system():
        next_state["value"] = GameState.LOAD_SYSTEM
        menu.disable()
    
    def quit_game():
        next_state["value"] = GameState.QUIT
        menu.disable()

    # Create buttons
    menu.add.button("New System", new_system)
    menu.add.button("Load System", load_system)
    menu.add.button("Quit", quit_game)

    # Run the menu
    menu.mainloop(screen)

    return next_state["value"]

def show_system_menu(screen):
    """
    Display the system menu.

    param: screen: The pygame display surface.

    return: tuple: (next_state, selected_system_path)
                    next_state: The next state to transition to.
                    selected_system_path: Path to the selected system file.
    """

    result = {"next_state": None, "system_path": None}

    # Get available systems from the data/systems directory
    available_systems = SystemLoader.list_systems("data/systems")

    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    menu_width = screen_width - 10
    menu_height = screen_height - 10

    menu = pygame_menu.Menu(
        title="Select a System",
        width=menu_width,
        height=menu_height,
        theme=CUSTOM_THEME
    )

    # For each system, add a button
    for system_name, system_path in available_systems:
        def select_system(path=system_path):
            result["next_state"] = GameState.SIMULATION
            result["system_path"] = path
            menu.disable()
        
        menu.add.button(system_name.replace("_", " ").title(), select_system)

    # Add spacing before back button
    menu.add.vertical_margin(50)  # 50 pixels of vertical space

    # Add a back button
    def go_back():
        result["next_state"] = GameState.MAIN_MENU
        menu.disable()

    menu.add.button("Back", go_back)

    menu.mainloop(screen)

    return result["next_state"], result["system_path"]