"""
Game state definitions for the application.
"""

from enum import Enum

class GameState(Enum):
    """Possible states the application can be in."""
    MAIN_MENU = 1
    NEW_SYSTEM = 2
    LOAD_SYSTEM = 3
    SIMULATION = 4
    QUIT = 5