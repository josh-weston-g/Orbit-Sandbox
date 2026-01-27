"""
UI Views for the application using pygame_gui.
Each view represents a screen/state in the application.
"""
import pygame
import pygame_gui

class MainMenuView:
    """Main menu screen with New System, Load System, and Quit options."""

    def __init__(self, screen_size):
        """
        Initialize the main menu view.

        param: screen_size: tuple (width, height) of the display surface.
        """
        self.manager = pygame_gui.UIManager(screen_size)
        self._next_view = None

        screen_w, screen_h = screen_size

        # Create centered panel
        panel_width, panel_height = 400, 350
        panel_x = (screen_w - panel_width) // 2
        panel_y = (screen_h - panel_height) // 2

        panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.manager
        )

        # Create buttons inside panel
        button_w = 300
        button_h = 60
        button_x = (panel_width - button_w) // 2
        button_y = 50
        gap = 20

        # New System Button
        self.btn_new = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), (button_w, button_h)),
            text="New System",
            manager=self.manager,
            container=panel
        )

        # Load System Button
        self.btn_load = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y + button_h + gap), (button_w, button_h)),
            text="Load System",
            manager=self.manager,
            container=panel
        )

        # Quit Button
        self.btn_quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y + 2 * (button_h + gap)), (button_w, button_h)),
            text="Quit",
            manager=self.manager,
            container=panel
        )

    def process_event(self, event):
        """Handle events for this view."""
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_new:
                self._next_view = 'new_system'
            elif event.ui_element == self.btn_load:
                self._next_view = 'load_system'
            elif event.ui_element == self.btn_quit:
                self._next_view = 'quit'

    def update(self, time_delta):
        """Update the UI manager."""
        self.manager.update(time_delta)

    def draw(self, screen):
        """Draw the UI elements to the surface."""
        screen.fill((20, 20, 30))  # Dark blue-gray background
        self.manager.draw_ui(screen)

    def get_next_view(self):
        """Return next view name if user requested a switch, then reset."""
        next_view = self._next_view
        self._next_view = None
        return next_view