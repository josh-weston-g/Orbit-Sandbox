"""
UI Views for the application using pygame_gui.
Each view represents a screen/state in the application.
"""
import pygame
import pygame_gui
from orbit.loader import SystemLoader

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
    
class LoadSystemView:
    """View for loading orbital systems from files."""

    def __init__(self, screen_size):
        """
        Initialize the load system view.
        
        param: screen_size: tuple (width, height) of the display surface.
        """
        self.manager = pygame_gui.UIManager(screen_size)
        self._next_view = None
        self.selected_system = None

        # Load systems from both directories
        systems = SystemLoader.list_systems()
        self.default_systems = systems['default']
        self.custom_systems = systems['custom']

        screen_w, screen_h = screen_size

        # Calculate dimensions for scrollable containers
        panel_w = int(screen_w * 0.3)
        panel_h = int(screen_h * 0.35)

        # Center horizontally
        panel_x = (screen_w - panel_w) // 2

        # Position vertically - leave space for title at top
        title_space = 100
        default_panel_y = title_space
        gap = 50 # Space between panels
        custom_panel_y = default_panel_y + panel_h + gap

        # Create title label at the top
        title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_w//2 - 150, 30), (300, 50)),
            text="Load Orbital System",
            manager=self.manager
        )

        # Create Default Systems label
        default_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, default_panel_y - 30), (panel_w, 25)),
            text="Default Systems",
            manager=self.manager
        )

        # Create background panel for default systems
        default_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((panel_x, default_panel_y), (panel_w, panel_h)),
            manager=self.manager
        )

        # Create scrollable panel for default systems ON TOP of background
        self.default_panel = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((panel_x, default_panel_y), (panel_w, panel_h)),
            manager=self.manager
        )

        # Add buttons for each default system
        button_w = panel_w - 40
        button_h = 40
        button_y = 10
        self.default_buttons = []

        for system_name, system_path in self.default_systems:
            display_name = system_name.replace('_', ' ').title()

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, button_y), (button_w, button_h)),
                text=display_name,
                manager=self.manager,
                container=self.default_panel
            )

            # Store button with its system path
            self.default_buttons.append((button, system_path))
            button_y += button_h + 10  # Move down for next button

        # Set the scrollable area dimensions (total content height)
        self.default_panel.set_scrollable_area_dimensions((panel_w - 20, button_y + 10))

        # Create Custom Systems label
        custom_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, custom_panel_y - 30), (panel_w, 25)),
            text="Custom Systems",
            manager=self.manager
        )

        # Create background panel for custom systems
        custom_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((panel_x, custom_panel_y), (panel_w, panel_h)),
            manager=self.manager
        )

        # Create scrollable panel for custom systems
        self.custom_panel = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((panel_x, custom_panel_y), (panel_w, panel_h)),
            manager=self.manager
        )

        # Add buttons for each custom system
        button_y = 10
        self.custom_buttons = []

        for system_name, system_path in self.custom_systems:
            display_name = system_name.replace('_', ' ').title()

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((10, button_y), (button_w, button_h)),
                text=display_name,
                manager=self.manager,
                container=self.custom_panel
            )

            # Store button with its system path
            self.custom_buttons.append((button, system_path))
            button_y += button_h + 10  # Move down for next button

        # Set the scrollable area dimensions (total content height)
        self.custom_panel.set_scrollable_area_dimensions((panel_w - 20, button_y + 10))

        # Add back button at the bottom
        back_button_y = custom_panel_y + panel_h + 30
        self.btn_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x, back_button_y), (panel_w, 50)),
            text="Back",
            manager=self.manager
        )

    def process_event(self, event):
        """Handle events for this view."""
        self.manager.process_events(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == self.btn_back:
                self._next_view = 'main_menu'
            else:
                # Check if a default system button was pressed
                for button, system_path in self.default_buttons:
                    if event.ui_element == button:
                        self.selected_system = system_path
                        self._next_view = 'simulation'
                        return
                    
                # Check if a custom system button was pressed
                for button, system_path in self.custom_buttons:
                    if event.ui_element == button:
                        self.selected_system = system_path
                        self._next_view = 'simulation'
                        return
                

    def update(self, time_delta):
        """Update the UI manager."""
        self.manager.update(time_delta)

    def draw(self, screen):
        """Draw the UI elements to the surface."""
        screen.fill((20, 20, 30))  # Darker blue-gray background
        self.manager.draw_ui(screen)

    def get_next_view(self):
        """Return next view name if user requested a switch, then reset."""
        next_view = self._next_view
        self._next_view = None
        return next_view