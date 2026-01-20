"""
Orbit-Sandbox - N-body gravitational simulation with interactive visualization.

Usage:
    python main.py [--resolution RESOLUTION]

Options:
    --resolution    Window resolution: auto, 720p, 1080p, 1440p (default: auto)
"""

import argparse
from ui.visualize import run_visualization
from ui.menu import show_main_menu, show_system_menu
import pygame
from ui.game_state import GameState

RESOLUTION_MAP = {
    '720p': (1280, 720),
    '1080p': (1920, 1080),
    '1440p': (2560, 1440)
}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Orbit-Sandbox - Interactive N-body orbital mechanics simulator"
    )
    parser.add_argument(
        '--resolution',
        type=str,
        default='auto',
        choices=['auto', '720p', '1080p', '1440p'],
        help='Window resolution (default: auto - fullscreen borderless)'
    )
    
    args = parser.parse_args()
    
    pygame.init()

    # Set up display - uses dynamic resolution based on argument
    if args.resolution == 'auto':
        display_info = pygame.display.Info()
        window_width, window_height = display_info.current_w, display_info.current_h
        screen = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)
    else:
        window_width, window_height = RESOLUTION_MAP[args.resolution]
        screen = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("Orbit Sandbox")

    # Set initial application state
    current_state = GameState.MAIN_MENU

    while current_state != GameState.QUIT:
        if current_state == GameState.MAIN_MENU:
            print("Entering Main Menu...")
            # Call the menu and get back which state to go to next
            next_state = show_main_menu(screen)
            current_state = next_state

        elif current_state == GameState.LOAD_SYSTEM:
            print("Loading System and Starting Simulation...")
            # Show systen menu and get chosen system
            next_state, system_path = show_system_menu(screen)
            selected_system = system_path
            current_state = next_state

        elif current_state == GameState.SIMULATION:
            print("Starting Simulation...")
            #TODO: Run simulation with selected system
            # For now, just go back to the menu
            current_state = GameState.MAIN_MENU

    pygame.quit()
    print("Exiting application...")