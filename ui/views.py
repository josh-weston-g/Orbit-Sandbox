"""
UI Views for the application using pygame_gui.
Each view represents a screen/state in the application.
"""
import pygame
import pygame_gui
from orbit.loader import SystemLoader
from ui.visualize import SimulationRunner

def load_background(path, screen_size):
    """Helper function to load and scale background image."""
    try:
        background = pygame.image.load(path).convert()
        background = pygame.transform.scale(background, screen_size)
        return background
    except FileNotFoundError:
        print(f"Warning: Background image '{path}' not found.")
        return None

class MainMenuView:
    """Main menu screen with New System, Load System, and Quit options."""

    def __init__(self, screen_size):
        """
        Initialize the main menu view.

        param: screen_size: tuple (width, height) of the display surface.
        """
        self.manager = pygame_gui.UIManager(screen_size, 'assets/themes/main_menu_theme.json')
        self._next_view = None

        # Load background image
        self.background = load_background('assets/images/menu_bg.jpg', screen_size)

        screen_w, screen_h = screen_size

        # Define button properties first
        button_w = 300
        button_h = 60
        gap = 20
        padding = 40  # Padding around buttons inside panel
        
        # Define button labels - buttons must still be created using pygame_gui.elements.UIButton below
        button_labels = ["New System", "Load System", "Settings", "Quit"]
        num_buttons = len(button_labels)
        
        # Calculate panel dimensions based on button count
        panel_width = button_w + (padding * 2)
        total_content_height = (num_buttons * button_h) + ((num_buttons - 1) * gap)
        panel_height = total_content_height + (padding * 2)
        
        # Calculate dynamic title font size - scale with screen height
        title_font_size = max(36, min(96, int(screen_h * 0.065)))
        
        # Load title font
        try:
            title_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Bold.ttf", title_font_size)
        except FileNotFoundError:
            title_font = pygame.font.Font(None, title_font_size)
        
        # Render title
        self.title_surface = title_font.render("ORBIT SANDBOX", True, (220, 220, 230))
        title_rect = self.title_surface.get_rect()
        
        # Load and render description
        description_font_size = max(16, min(24, int(screen_h * 0.02)))
        try:
            description_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", description_font_size)
        except FileNotFoundError:
            description_font = pygame.font.Font(None, description_font_size)
        
        self.description_surface = description_font.render("Interactive Orbital Simulator", True, (180, 180, 190))
        description_rect = self.description_surface.get_rect()
        
        # Calculate spacing and positioning
        desc_gap = int(screen_h * 0.02)  # Gap between title and description
        title_spacing = int(screen_h * 0.12)  # Gap between description and panel
        
        # Calculate total height including both title and description
        title_group_height = title_rect.height + desc_gap + description_rect.height
        total_menu_height = title_group_height + title_spacing + panel_height
        menu_start_y = (screen_h - total_menu_height) // 2
        
        # Create semi-transparent background for title area
        bg_padding = 30
        title_bg_width = max(title_rect.width, description_rect.width) + (bg_padding * 2)
        title_bg_height = title_group_height + (bg_padding * 2)
        title_bg_x = (screen_w - title_bg_width) // 2
        title_bg_y = menu_start_y - bg_padding
        
        self.title_bg_surface = pygame.Surface((title_bg_width, title_bg_height))
        self.title_bg_surface.set_alpha(180)
        self.title_bg_surface.fill((15, 20, 30))
        self.title_bg_position = (title_bg_x, title_bg_y)
        
        # Store title and description positions (centered)
        self.title_position = ((screen_w - title_rect.width) // 2, menu_start_y)
        self.description_position = ((screen_w - description_rect.width) // 2, menu_start_y + title_rect.height + desc_gap)
        
        # Position panel below title group
        panel_x = (screen_w - panel_width) // 2
        panel_y = menu_start_y + title_group_height + title_spacing

        panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(panel_x, panel_y, panel_width, panel_height),
            manager=self.manager
        )

        # Center buttons inside panel
        button_x = (panel_width - button_w) // 2 - 4  # Offset for border/shadow
        button_y = padding - 4  # Offset for border/shadow

        # Create buttons
        self.btn_new = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), (button_w, button_h)),
            text=button_labels[0],
            manager=self.manager,
            container=panel
        )

        self.btn_load = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y + (button_h + gap)), (button_w, button_h)),
            text=button_labels[1],
            manager=self.manager,
            container=panel
        )

        self.btn_settings = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y + 2 * (button_h + gap)), (button_w, button_h)),
            text=button_labels[2],
            manager=self.manager,
            container=panel
        )

        self.btn_quit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y + 3 * (button_h + gap)), (button_w, button_h)),
            text=button_labels[3],
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
            elif event.ui_element == self.btn_settings:
                self._next_view = 'settings'
            elif event.ui_element == self.btn_quit:
                self._next_view = 'quit'

    def update(self, time_delta):
        """Update the UI manager."""
        self.manager.update(time_delta)

    def draw(self, screen):
        """Draw the UI elements to the surface."""
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((30, 30, 40))  # Fallback background color
        
        # Draw title background
        screen.blit(self.title_bg_surface, self.title_bg_position)
        
        # Draw title and description
        screen.blit(self.title_surface, self.title_position)
        screen.blit(self.description_surface, self.description_position)
        
        self.manager.draw_ui(screen)

    def get_next_view(self):
        """Return next view name if user requested a switch, then reset."""
        next_view = self._next_view
        self._next_view = None
        return next_view
    
class LoadSystemView:
    """View for loading orbital systems from files."""

    # Layout constants
    MIN_PANEL_HEIGHT = 100  # Minimum height for scrollable panels
    MIN_PANEL_WIDTH = 300   # Minimum width for panels
    MAX_PANEL_WIDTH = 500   # Maximum width for panels
    SCROLLBAR_WIDTH = 20    # Width of the scrollbar in scrollable containers

    def __init__(self, screen_size):
        """
        Initialize the load system view.
        
        param: screen_size: tuple (width, height) of the display surface.
        """
        self.manager = pygame_gui.UIManager(screen_size, 'assets/themes/load_system_theme.json')
        self._next_view = None
        self.selected_system = None

        # Hover tracking
        self.hovered_button = None
        self.hovered_system_path = None

        # Load background image (shared with main menu)
        self.background = load_background('assets/images/menu_bg.jpg', screen_size)

        # Load systems from both directories
        systems = SystemLoader.list_systems()
        self.default_systems = systems['default']
        self.custom_systems = systems['custom']

        screen_w, screen_h = screen_size

        # Calculate responsive dimensions based on screen size
        # Title section takes ~10% of height
        title_height = int(screen_h * 0.08)
        title_y = int(screen_h * 0.02)
        
        # Section labels height
        label_height = 25
        label_gap = 8
        
        # Back button at bottom - ensure it's always visible
        back_button_h = 50
        bottom_margin = int(screen_h * 0.03)  # 3% margin at bottom
        
        # Gap between panels
        panel_gap = int(screen_h * 0.04)
        
        # Calculate available height for panels
        # Available = screen_h - title area - 2x labels - gap between panels - back button area - margins
        title_area = title_y + title_height + int(screen_h * 0.02)
        back_area = back_button_h + bottom_margin
        available_height = screen_h - title_area - (2 * (label_height + label_gap)) - panel_gap - back_area
        
        # Each panel gets half the available height (ensure they're always equal)
        panel_h = max(int(available_height / 2), self.MIN_PANEL_HEIGHT)
        
        # Panel width - constrained between min and max
        panel_w = int(screen_w * 0.35)
        panel_w = max(panel_w, self.MIN_PANEL_WIDTH)
        panel_w = min(panel_w, self.MAX_PANEL_WIDTH)
        
        # Center horizontally
        panel_x = (screen_w - panel_w) // 2

        # Inset panel inside background panels for scrollable areas
        panel_inset = 8

        # Calculate vertical positions
        default_label_y = title_area
        default_panel_y = default_label_y + label_height + label_gap
        
        custom_label_y = default_panel_y + panel_h + panel_gap
        custom_panel_y = custom_label_y + label_height + label_gap
        
        back_button_y = custom_panel_y + panel_h + int(screen_h * 0.02)

        # Create title label at the top
        title_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((screen_w//2 - 200, title_y), (400, title_height)),
            text="Load Orbital System",
            manager=self.manager,
            object_id='#title_label'
        )

        # Create Default Systems label
        default_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, default_label_y), (panel_w, label_height)),
            text="Default Systems",
            manager=self.manager,
            object_id='#section_label'
        )

        # Create background panel for default systems
        default_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((panel_x, default_panel_y), (panel_w, panel_h)),
            manager=self.manager
        )

        # Create scrollable panel on top of background panel
        self.default_panel = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((panel_x, default_panel_y + panel_inset), (panel_w , panel_h - 2 * panel_inset)),
            manager=self.manager
        )

        # Calculate button dimensions - account for scrollbar width
        button_margin = 15
        # Button width fills container, centered regardless of scrollbar
        button_w = panel_w - (button_margin * 2) - self.SCROLLBAR_WIDTH
        button_h = 40
        button_spacing = 10
        button_y = button_margin
        
        self.default_buttons = []

        for system_name, system_path in self.default_systems:
            display_name = system_name.replace('_', ' ').title()

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_margin, button_y), (button_w, button_h)),
                text=display_name,
                manager=self.manager,
                container=self.default_panel,
                object_id='#system_button'
            )

            # Store button with its system path
            self.default_buttons.append((button, system_path))
            button_y += button_h + button_spacing

        # Set the scrollable area dimensions (total content height)
        content_height = button_y + button_margin
        self.default_panel.set_scrollable_area_dimensions((panel_w - self.SCROLLBAR_WIDTH, content_height))

        # Create Custom Systems label
        custom_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((panel_x, custom_label_y), (panel_w, label_height)),
            text="Custom Systems",
            manager=self.manager,
            object_id='#section_label'
        )

        # Create background panel for custom systems
        custom_bg = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((panel_x, custom_panel_y), (panel_w, panel_h)),
            manager=self.manager
        )

        # Create scrollable panel on top of background panel
        self.custom_panel = pygame_gui.elements.UIScrollingContainer(
            relative_rect=pygame.Rect((panel_x, custom_panel_y + panel_inset), (panel_w , panel_h - 2 * panel_inset)),
            manager=self.manager
        )

        # Add buttons for each custom system
        button_y = button_margin
        self.custom_buttons = []

        for system_name, system_path in self.custom_systems:
            display_name = system_name.replace('_', ' ').title()

            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_margin, button_y), (button_w, button_h)),
                text=display_name,
                manager=self.manager,
                container=self.custom_panel,
                object_id='#system_button'
            )

            # Store button with its system path
            self.custom_buttons.append((button, system_path))
            button_y += button_h + button_spacing

        # Set the scrollable area dimensions (total content height)
        content_height = button_y + button_margin
        self.custom_panel.set_scrollable_area_dimensions((panel_w - self.SCROLLBAR_WIDTH, content_height))

        # Add back button at the bottom - uses default button style (main button)
        self.btn_back = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((panel_x, back_button_y), (panel_w, back_button_h)),
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
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((20, 20, 30))  # Fallback background color
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