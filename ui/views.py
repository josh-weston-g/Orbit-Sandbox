"""
UI Views for the application using pygame_gui.
Each view represents a screen/state in the application.
"""
import pygame
import pygame_gui
from orbit.loader import SystemLoader
from ui.visualize import SimulationRunner

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

        # Hover tracking
        self.hovered_button = None
        self.hovered_system_path = None

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

    def get_system_description(self, system_path):
        """Load and return the description from a system's JSON file."""
        import json
        try:
            with open(system_path, 'r') as f:
                data = json.load(f)
                return data.get('description', 'No description available.')
        except Exception as e:
            return f"Error loading description: {e}"

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

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        currently_hovered = None
        hovered_path = None

        # Check default system buttons for hover
        for button, system_path in self.default_buttons:
            if button.rect.collidepoint(mouse_pos):
                currently_hovered = button
                hovered_path = system_path
                break

        # Check custom system buttons for hover if no default button is hovered
        if currently_hovered is None:
            for button, system_path in self.custom_buttons:
                if button.rect.collidepoint(mouse_pos):
                    currently_hovered = button
                    hovered_path = system_path
                    break

        # Update hover state
        if currently_hovered != self.hovered_button:
            # Mouse moved to a different button (or none)
            self.hovered_button = currently_hovered
            self.hovered_system_path = hovered_path
        
        # If not hovering over anything, reset
        if currently_hovered is None:
            self.hovered_button = None
            self.hovered_system_path = None

    def draw(self, screen):
        """Draw the UI elements to the surface."""
        screen.fill((20, 20, 30))  # Darker blue-gray background
        self.manager.draw_ui(screen)

        # Draw tooltip if hovering over a system button
        if self.hovered_button and self.hovered_system_path:
            # Load description for hovered system
            description = self.get_system_description(self.hovered_system_path)

            # Create tooltip
            try:
                tooltip_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 20)
            except FileNotFoundError:
                tooltip_font = pygame.font.Font(None, 20)

            # Word wrap the description to fit in tooltip
            max_tooltip_width = 300
            words = description.split(' ')
            lines = []
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surface = tooltip_font.render(test_line, True, (255, 255, 255))

                if test_surface.get_width() <= max_tooltip_width - 20:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:
                lines.append(' '.join(current_line))

            # Calculate tooltip dimensions
            line_height = 25
            tooltip_height = len(lines) * line_height + 20
            tooltip_width = max_tooltip_width

            # Position tooltip to the right of the button
            button_rect = self.hovered_button.rect
            tooltip_x = button_rect.right + 20
            tooltip_y = button_rect.top

            # Make sure tooltip stays on screen
            screen_w, screen_h = screen.get_size()
            # If goes off right edge, keep it on right but align to screen edge
            if tooltip_x + tooltip_width > screen_w:
                tooltip_x = screen_w - tooltip_width - 20

            # If goes off bottom edge, shift it up
            if tooltip_y + tooltip_height > screen_h:
                tooltip_y = screen_h - tooltip_height - 10

            # If goes off top edge, shift it down
            if tooltip_y < 0:
                tooltip_y = 10

            # Draw semi-transparent background
            tooltip_surface = pygame.Surface((tooltip_width, tooltip_height))
            tooltip_surface.set_alpha(150)
            tooltip_surface.fill((50, 50, 50))  # Dark background
            screen.blit(tooltip_surface, (tooltip_x, tooltip_y))

            # Draw border
            pygame.draw.rect(screen, (100, 100, 100),
                            (tooltip_x, tooltip_y, tooltip_width, tooltip_height), 2)

            # Draw text lines
            text_y = tooltip_y + 10
            for line in lines:
                text_surface = tooltip_font.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (tooltip_x + 10, text_y))
                text_y += line_height

    def get_next_view(self):
        """Return next view name if user requested a switch, then reset."""
        next_view = self._next_view
        self._next_view = None
        return next_view

class SimulationView:
    """Thin wrapper around SimulationRunner to fit in the view system."""

    def __init__(self, screen_size, system_path, clock):
        """Initialize simulation view with the selected system"""
        self.runner = SimulationRunner(screen_size, system_path, clock)
        self._next_view = None

    def process_event(self, event):
        """Pass event to simulation runner."""
        self.runner.handle_event(event)

    def update(self, time_delta):
        """Update simulation physics"""
        self.runner.update_physics(time_delta)

        # Check if runner wants to exit
        requested = self.runner.get_requested_next_view()
        if requested:
            self._next_view = requested

    def draw(self, screen):
        """Draw simulation."""
        self.runner.draw(screen)

    def get_next_view(self):
        """Return next view if simulation wants to exit."""
        next_view = self._next_view
        self._next_view = None
        return next_view