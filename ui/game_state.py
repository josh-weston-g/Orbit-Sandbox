"""
Game state definitions for the application.
"""

from enum import Enum

class GameState(Enum):
    """Possible states the application can be in."""
    MAIN_MENU = 1
    LOAD_SYSTEM = 2
    SIMULATION = 3
    QUIT = 4