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

    # Get categorized systems
    systems = SystemLoader.list_systems()
    default_systems = systems['default']
    custom_systems = systems['custom']

    # Get screen dimensions
    screen_width, screen_height = screen.get_size()
    menu_width = screen_width - 10
    menu_height = screen_height - 10

    # Calculate frame sizes (relative to screen size)
    # Each frame gets 35% of screen height, leaving room for title, labels, back button
    frame_height = int(screen_height * 0.35)
    frame_width = int(screen_width * 0.25)

    menu = pygame_menu.Menu(
        title="Load System",
        width=menu_width,
        height=menu_height,
        theme=CUSTOM_THEME
    )

    # Add "Default Systems" header label
    menu.add.label("Default Systems", font_size=30)  #! Make it look like a header
    menu.add.vertical_margin(10)

    # Create a scrollable frame for default systems
    default_frame = menu.add.frame_v(
        width=frame_width,
        height=frame_height,
        background_color=(30, 30, 30),  # Slightly different shade to show the frame
        padding=10
    )

    # Add buttons for default systems
    for system_name, system_path in default_systems:
        def select_system(path=system_path):
            result["next_state"] = GameState.SIMULATION
            result["system_path"] = path
            menu.disable()

        display_name = system_name.replace('_', ' ').title()
        button = menu.add.button(display_name, select_system, margin=(0, 0))
        default_frame.pack(button, align=pygame_menu.locals.ALIGN_CENTER)

    # Add spacing between categories
    menu.add.vertical_margin(30)

    # Add "Custom Systems" header label
    menu.add.label("Custom Systems", font_size=30)  #! Make it look like a header
    menu.add.vertical_margin(10)

    # Create a scrollable frame for custom systems
    custom_frame = menu.add.frame_v(
        width=frame_width,
        height=frame_height,
        background_color=(30, 30, 30),
        padding=10
    )

    # Add buttons for custom systems
    for system_name, system_path in custom_systems:
        def select_system(path=system_path):
            result["next_state"] = GameState.SIMULATION
            result["system_path"] = path
            menu.disable()

        display_name = system_name.replace('_', ' ').title()
        button = menu.add.button(display_name, select_system, margin=(0, 0))
        custom_frame.pack(button, align=pygame_menu.locals.ALIGN_CENTER)

    # Add spacing before back button
    menu.add.vertical_margin(50)

    # Add a back button
    def go_back():
        result["next_state"] = GameState.MAIN_MENU
        menu.disable()

    menu.add.button("Back", go_back)

    menu.mainloop(screen)

    return result["next_state"], result["system_path"]