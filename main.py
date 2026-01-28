"""
Orbit-Sandbox - N-body gravitational simulation with interactive visualization.

Usage:
    python main.py [--resolution RESOLUTION]

Options:
    --resolution    Window resolution: auto, 720p, 1080p, 1440p (default: auto)
"""

import argparse
from ui.views import MainMenuView, LoadSystemView, SimulationView
import pygame

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
    clock = pygame.time.Clock()

    # Create views dictionary
    views = {
        "main_menu": MainMenuView((window_width, window_height)),
        "load_system": LoadSystemView((window_width, window_height))
    }

    current_view_name = "main_menu"
    selected_system_path = None

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0  # Limit to 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Pass event to current view
            views[current_view_name].process_event(event)

        # Update and draw current view
        views[current_view_name].update(time_delta)
        views[current_view_name].draw(screen)

        # Check if view wants to switch
        next_view_name = views[current_view_name].get_next_view()
        
        # Handle system selection from LoadSystemView
        if current_view_name == "load_system" and next_view_name == "simulation":
            selected_system_path = views["load_system"].selected_system
            if selected_system_path:
                # Create simulation view with selected system
                views["simulation"] = SimulationView(
                    (window_width, window_height),
                    selected_system_path
                )

        if next_view_name == "quit":
            running = False
        elif next_view_name:
            if next_view_name not in views:
                print(f"View '{next_view_name}' not yet implemented - staying in current view.")  #! Refactor for production
                # Stay on current view for now
            else:
                current_view_name = next_view_name
                print(f"Switched to: {current_view_name}") #! Remove debug print in production

        pygame.display.flip()

    pygame.quit()