"""
UI Views for Orbit-Sandbox menu system.

Provides themed, responsive views for the main menu and system selection interfaces.
"""

import pygame
import json
import os
from orbit.loader import SystemLoader


class Theme:
    """Load and manage theme configuration from JSON files."""
    
    def __init__(self, theme_path):
        """Load theme from JSON file."""
        with open(theme_path, 'r') as f:
            self.data = json.load(f)
        self.name = self.data.get('name', 'Unnamed Theme')
    
    def get_color(self, *keys):
        """Get a color value by nested keys, returns as tuple."""
        value = self.data.get('colors', {})
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, [255, 255, 255])
            else:
                return (255, 255, 255)
        return tuple(value) if isinstance(value, list) else value
    
    def get_font_config(self, key):
        """Get font configuration by key."""
        return self.data.get('fonts', {}).get(key, {
            'family': None,
            'size': 24
        })
    
    def get_button_config(self, key='button'):
        """Get button configuration."""
        return self.data.get(key, {
            'width': 200,
            'height': 40,
            'border_radius': 5,
            'border_width': 2,
            'spacing': 10
        })
    
    def get_container_config(self):
        """Get container configuration."""
        return self.data.get('container', {
            'border_radius': 8,
            'border_width': 2,
            'header_height': 35,
            'padding': 10,
            'spacing': 20
        })
    
    def get_scrollbar_config(self):
        """Get scrollbar configuration."""
        return self.data.get('scrollbar', {
            'width': 8,
            'border_radius': 4,
            'padding': 3
        })
    
    def get_background_image(self):
        """Get background image path."""
        return self.data.get('background_image', None)


class Button:
    """Themed button with hover and click states."""
    
    def __init__(self, rect, text, theme, button_type='button'):
        self.rect = rect
        self.text = text
        self.theme = theme
        self.button_type = button_type
        self.hovered = False
        self.pressed = False
        
        # Get button styling from theme
        color_key = 'system_button' if button_type == 'system_button' else 'button'
        self.colors = {
            'normal': theme.get_color(color_key, 'normal'),
            'hover': theme.get_color(color_key, 'hover'),
            'pressed': theme.get_color(color_key, 'pressed'),
            'text': theme.get_color(color_key, 'text'),
            'border': theme.get_color(color_key, 'border')
        }
        
        # Get button config
        config = theme.get_button_config(button_type)
        self.border_radius = config.get('border_radius', 5)
        self.border_width = config.get('border_width', 2)
        
        # Load font
        font_key = 'system_button' if button_type == 'system_button' else 'button'
        font_config = theme.get_font_config(font_key)
        self.font = self._load_font(font_config)
    
    def _load_font(self, font_config):
        """Load font from config."""
        try:
            font_path = os.path.join('assets/fonts', font_config.get('family', ''))
            return pygame.font.Font(font_path, font_config.get('size', 24))
        except (FileNotFoundError, TypeError):
            return pygame.font.Font(None, font_config.get('size', 24))
    
    def update(self, mouse_pos, mouse_pressed):
        """Update button state based on mouse position and clicks."""
        self.hovered = self.rect.collidepoint(mouse_pos)
        self.pressed = self.hovered and mouse_pressed
    
    def draw(self, surface):
        """Draw the button on the given surface."""
        # Determine current color based on state
        if self.pressed:
            bg_color = self.colors['pressed']
        elif self.hovered:
            bg_color = self.colors['hover']
        else:
            bg_color = self.colors['normal']
        
        # Draw button background with rounded corners
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.border_radius)
        
        # Draw border
        pygame.draw.rect(surface, self.colors['border'], self.rect, 
                        width=self.border_width, border_radius=self.border_radius)
        
        # Draw text centered
        text_surface = self.font.render(self.text, True, self.colors['text'])
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def is_clicked(self, event):
        """Check if button was clicked."""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class ScrollableContainer:
    """A themed scrollable container for displaying a list of items."""
    
    def __init__(self, rect, title, theme):
        self.rect = rect
        self.title = title
        self.theme = theme
        self.items = []
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scrollbar_hovered = False
        self.scrollbar_dragging = False
        self.drag_start_y = 0
        self.drag_start_offset = 0
        
        # Get config
        self.container_config = theme.get_container_config()
        self.scrollbar_config = theme.get_scrollbar_config()
        
        # Calculate dimensions
        self.header_height = self.container_config.get('header_height', 40)
        self.padding = self.container_config.get('padding', 15)
        self.border_radius = self.container_config.get('border_radius', 10)
        self.border_width = self.container_config.get('border_width', 2)
        self.scrollbar_width = self.scrollbar_config.get('width', 10)
        self.scrollbar_padding = self.scrollbar_config.get('padding', 5)
        
        # Content area (excludes header, includes scrollbar space)
        self.content_rect = pygame.Rect(
            self.rect.x + self.padding,
            self.rect.y + self.header_height + self.padding,
            self.rect.width - (self.padding * 2) - self.scrollbar_width - self.scrollbar_padding,
            self.rect.height - self.header_height - (self.padding * 2)
        )
        
        # Scrollbar track area
        self.scrollbar_track = pygame.Rect(
            self.rect.x + self.rect.width - self.scrollbar_width - self.scrollbar_padding,
            self.rect.y + self.header_height + self.scrollbar_padding,
            self.scrollbar_width,
            self.rect.height - self.header_height - (self.scrollbar_padding * 2)
        )
        
        # Load header font
        font_config = theme.get_font_config('container_header')
        self.header_font = self._load_font(font_config)
    
    def _load_font(self, font_config):
        """Load font from config."""
        try:
            font_path = os.path.join('assets/fonts', font_config.get('family', ''))
            return pygame.font.Font(font_path, font_config.get('size', 22))
        except (FileNotFoundError, TypeError):
            return pygame.font.Font(None, font_config.get('size', 22))
    
    def set_items(self, items):
        """Set the list of items (Button objects)."""
        self.items = items
        self._recalculate_layout()
    
    def _recalculate_layout(self):
        """Recalculate item positions and scroll bounds."""
        if not self.items:
            self.max_scroll = 0
            return
        
        button_config = self.theme.get_button_config('system_button')
        button_height = button_config.get('height', 40)
        button_spacing = button_config.get('spacing', 8)
        
        total_height = len(self.items) * (button_height + button_spacing) - button_spacing
        self.max_scroll = max(0, total_height - self.content_rect.height)
        
        # Reposition items based on current scroll - center horizontally
        button_width = button_config.get('width', 240)
        center_x = self.content_rect.x + (self.content_rect.width - button_width) // 2
        
        for i, item in enumerate(self.items):
            y = self.content_rect.y + i * (button_height + button_spacing) - self.scroll_offset
            item.rect = pygame.Rect(center_x, y, button_width, button_height)
    
    def handle_event(self, event):
        """Handle mouse events for scrolling."""
        if event.type == pygame.MOUSEWHEEL:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.scroll_offset = max(0, min(self.max_scroll, 
                    self.scroll_offset - event.y * 30))
                self._recalculate_layout()
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.scrollbar_track.collidepoint(event.pos) and self.max_scroll > 0:
                thumb_rect = self._get_thumb_rect()
                if thumb_rect.collidepoint(event.pos):
                    self.scrollbar_dragging = True
                    self.drag_start_y = event.pos[1]
                    self.drag_start_offset = self.scroll_offset
                else:
                    # Click on track - jump to position
                    track_click_ratio = (event.pos[1] - self.scrollbar_track.y) / self.scrollbar_track.height
                    self.scroll_offset = int(track_click_ratio * self.max_scroll)
                    self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
                    self._recalculate_layout()
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.scrollbar_dragging = False
        
        elif event.type == pygame.MOUSEMOTION:
            if self.scrollbar_dragging:
                delta_y = event.pos[1] - self.drag_start_y
                scroll_ratio = delta_y / (self.scrollbar_track.height - self._get_thumb_height())
                self.scroll_offset = int(self.drag_start_offset + scroll_ratio * self.max_scroll)
                self.scroll_offset = max(0, min(self.max_scroll, self.scroll_offset))
                self._recalculate_layout()
    
    def _get_thumb_height(self):
        """Calculate scrollbar thumb height."""
        if self.max_scroll == 0:
            return self.scrollbar_track.height
        
        content_ratio = self.content_rect.height / (self.content_rect.height + self.max_scroll)
        thumb_height = max(30, int(self.scrollbar_track.height * content_ratio))
        return min(thumb_height, self.scrollbar_track.height)
    
    def _get_thumb_rect(self):
        """Get the current scrollbar thumb rectangle."""
        thumb_height = self._get_thumb_height()
        
        if self.max_scroll == 0:
            thumb_y = self.scrollbar_track.y
        else:
            scroll_ratio = self.scroll_offset / self.max_scroll
            available_space = self.scrollbar_track.height - thumb_height
            thumb_y = self.scrollbar_track.y + int(scroll_ratio * available_space)
        
        return pygame.Rect(
            self.scrollbar_track.x,
            thumb_y,
            self.scrollbar_width,
            thumb_height
        )
    
    def update(self, mouse_pos, mouse_pressed):
        """Update container and items state."""
        self.scrollbar_hovered = self.scrollbar_track.collidepoint(mouse_pos)
        
        # Update visible items
        for item in self.items:
            if self._is_item_visible(item):
                item.update(mouse_pos, mouse_pressed)
    
    def _is_item_visible(self, item):
        """Check if an item is visible within the content area."""
        return (item.rect.bottom > self.content_rect.y and 
                item.rect.top < self.content_rect.bottom)
    
    def draw(self, surface):
        """Draw the container and its contents."""
        # Draw container background
        bg_color = self.theme.get_color('container', 'background')
        pygame.draw.rect(surface, bg_color, self.rect, border_radius=self.border_radius)
        
        # Draw container border
        border_color = self.theme.get_color('container', 'border')
        pygame.draw.rect(surface, border_color, self.rect, 
                        width=self.border_width, border_radius=self.border_radius)
        
        # Draw header
        header_rect = pygame.Rect(self.rect.x, self.rect.y, 
                                  self.rect.width, self.header_height)
        header_color = self.theme.get_color('container', 'header')
        pygame.draw.rect(surface, header_color, header_rect, 
                        border_top_left_radius=self.border_radius,
                        border_top_right_radius=self.border_radius)
        
        # Draw header text
        header_text_color = self.theme.get_color('container', 'header_text')
        text_surface = self.header_font.render(self.title, True, header_text_color)
        text_rect = text_surface.get_rect(center=(header_rect.centerx, header_rect.centery))
        surface.blit(text_surface, text_rect)
        
        # Create clipping region for content
        clip_rect = self.content_rect.copy()
        clip_rect.width += self.scrollbar_width + self.scrollbar_padding  # Include scrollbar
        original_clip = surface.get_clip()
        surface.set_clip(clip_rect)
        
        # Draw items
        for item in self.items:
            if self._is_item_visible(item):
                item.draw(surface)
        
        # Reset clipping
        surface.set_clip(original_clip)
        
        # Draw scrollbar if needed
        if self.max_scroll > 0:
            self._draw_scrollbar(surface)
    
    def _draw_scrollbar(self, surface):
        """Draw the scrollbar."""
        # Draw track
        track_color = self.theme.get_color('scrollbar', 'track')
        scrollbar_radius = self.scrollbar_config.get('border_radius', 5)
        pygame.draw.rect(surface, track_color, self.scrollbar_track, 
                        border_radius=scrollbar_radius)
        
        # Draw thumb
        thumb_rect = self._get_thumb_rect()
        if self.scrollbar_dragging or self.scrollbar_hovered:
            thumb_color = self.theme.get_color('scrollbar', 'thumb_hover')
        else:
            thumb_color = self.theme.get_color('scrollbar', 'thumb')
        pygame.draw.rect(surface, thumb_color, thumb_rect, 
                        border_radius=scrollbar_radius)
    
    def get_clicked_item(self, event):
        """Get the item that was clicked, if any."""
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.content_rect.collidepoint(event.pos):
                for item in self.items:
                    if self._is_item_visible(item) and item.rect.collidepoint(event.pos):
                        return item
        return None


class BaseView:
    """Base class for all views."""
    
    def __init__(self, screen, theme_path):
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        self.theme = Theme(theme_path)
        self.background = None
        self.clock = pygame.time.Clock()
        self._load_background()
    
    def _load_background(self):
        """Load and scale background image."""
        bg_path = self.theme.get_background_image()
        if bg_path and os.path.exists(bg_path):
            try:
                bg_image = pygame.image.load(bg_path)
                self.background = pygame.transform.scale(bg_image, (self.width, self.height))
            except pygame.error:
                self.background = None
    
    def _load_font(self, font_key):
        """Load a font by theme key."""
        font_config = self.theme.get_font_config(font_key)
        try:
            font_path = os.path.join('assets/fonts', font_config.get('family', ''))
            return pygame.font.Font(font_path, font_config.get('size', 24))
        except (FileNotFoundError, TypeError):
            return pygame.font.Font(None, font_config.get('size', 24))
    
    def draw_background(self):
        """Draw the background (image or solid color)."""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            bg_color = self.theme.get_color('background')
            self.screen.fill(bg_color)
    
    def run(self):
        """Main loop for the view. Override in subclasses."""
        raise NotImplementedError


class MainMenuView(BaseView):
    """Main menu view with themed buttons."""
    
    def __init__(self, screen):
        super().__init__(screen, 'assets/themes/main_menu_theme.json')
        self.title_font = self._load_font('title')
        self.subtitle_font = self._load_font('subtitle')
        self._create_buttons()
    
    def _create_buttons(self):
        """Create menu buttons."""
        button_config = self.theme.get_button_config()
        button_width = button_config.get('width', 300)
        button_height = button_config.get('height', 50)
        button_spacing = button_config.get('spacing', 15)
        
        # Calculate button positions - centered horizontally, in lower third of screen
        center_x = self.width // 2
        start_y = int(self.height * 0.45)
        
        button_data = [
            ('load_system', 'Load System'),
            ('settings', 'Settings'),
            ('exit', 'Exit')
        ]
        
        self.buttons = {}
        for i, (key, text) in enumerate(button_data):
            y = start_y + i * (button_height + button_spacing)
            rect = pygame.Rect(center_x - button_width // 2, y, button_width, button_height)
            self.buttons[key] = Button(rect, text, self.theme)
    
    def draw_title(self):
        """Draw the title and subtitle."""
        # Title
        title_color = self.theme.get_color('title')
        title_shadow_color = self.theme.get_color('title_shadow')
        
        title_text = self.title_font.render("Orbit Sandbox", True, title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, int(self.height * 0.2)))
        
        # Draw shadow
        shadow_text = self.title_font.render("Orbit Sandbox", True, title_shadow_color)
        shadow_rect = shadow_text.get_rect(center=(title_rect.centerx + 3, title_rect.centery + 3))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_color = self.theme.get_color('subtitle')
        subtitle_text = self.subtitle_font.render("N-Body Gravitational Simulation", True, subtitle_color)
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, int(self.height * 0.28)))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def run(self):
        """Run the main menu. Returns the selected action."""
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'exit'
                
                for key, button in self.buttons.items():
                    if button.is_clicked(event):
                        return key
            
            # Update buttons
            for button in self.buttons.values():
                button.update(mouse_pos, mouse_pressed)
            
            # Draw
            self.draw_background()
            self.draw_title()
            for button in self.buttons.values():
                button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return 'exit'


class LoadSystemView(BaseView):
    """View for loading orbital systems, with two scrollable containers."""
    
    def __init__(self, screen):
        super().__init__(screen, 'assets/themes/load_system_theme.json')
        self.title_font = self._load_font('title')
        self.selected_system = None
        
        # Calculate responsive layout
        self._calculate_layout()
        self._create_containers()
        self._create_back_button()
        self._populate_containers()
    
    def _calculate_layout(self):
        """Calculate responsive layout dimensions based on window size."""
        # Reference resolution for scaling (1080p)
        ref_height = 1080
        scale_factor = self.height / ref_height
        
        # Minimum margins and sizes
        self.title_height = int(80 * scale_factor)
        self.title_y = int(50 * scale_factor)
        
        # Container dimensions - responsive to window size
        container_config = self.theme.get_container_config()
        container_spacing = int(container_config.get('spacing', 30) * scale_factor)
        
        # Calculate available space for containers
        top_margin = self.title_y + self.title_height + int(20 * scale_factor)
        bottom_margin = int(80 * scale_factor)  # Space for back button
        
        available_height = self.height - top_margin - bottom_margin
        
        # Each container gets equal height
        container_height = (available_height - container_spacing) // 2
        container_height = max(container_height, 150)  # Minimum height
        
        # Container width - centered with margins
        container_width = min(int(500 * scale_factor), self.width - int(100 * scale_factor))
        container_x = (self.width - container_width) // 2
        
        # Position containers
        self.container1_rect = pygame.Rect(
            container_x, 
            top_margin, 
            container_width, 
            container_height
        )
        
        self.container2_rect = pygame.Rect(
            container_x,
            top_margin + container_height + container_spacing,
            container_width,
            container_height
        )
        
        # Back button position - below containers with margin
        button_config = self.theme.get_button_config()
        button_width = button_config.get('width', 260)
        button_height = button_config.get('height', 45)
        
        button_y = self.container2_rect.bottom + int(15 * scale_factor)
        # Ensure button is always visible on screen
        button_y = min(button_y, self.height - button_height - int(10 * scale_factor))
        
        self.back_button_rect = pygame.Rect(
            (self.width - button_width) // 2,
            button_y,
            button_width,
            button_height
        )
    
    def _create_containers(self):
        """Create the scrollable containers."""
        self.builtin_container = ScrollableContainer(
            self.container1_rect, 
            "Built-in Systems", 
            self.theme
        )
        
        self.custom_container = ScrollableContainer(
            self.container2_rect,
            "Custom Systems",
            self.theme
        )
    
    def _create_back_button(self):
        """Create the back button with main button styling."""
        self.back_button = Button(
            self.back_button_rect,
            "Back",
            self.theme,
            button_type='button'  # Main button style
        )
    
    def _populate_containers(self):
        """Load and populate containers with system files."""
        # Get all available systems
        all_systems = SystemLoader.list_systems("data/systems")
        
        # For this demo, we'll split them - first half builtin, second half custom
        # In a real implementation, you'd have separate directories
        mid = len(all_systems) // 2
        builtin_systems = all_systems[:max(mid, len(all_systems))]
        custom_systems = all_systems[mid:] if mid > 0 else []
        
        # Actually, let's put all in builtin for now since that's where they are
        builtin_systems = all_systems
        custom_systems = []  # Empty for now - user can add custom systems later
        
        # Create buttons for builtin systems
        builtin_buttons = []
        button_config = self.theme.get_button_config('system_button')
        button_width = button_config.get('width', 240)
        button_height = button_config.get('height', 40)
        
        for name, path in builtin_systems:
            display_name = name.replace('_', ' ').title()
            rect = pygame.Rect(0, 0, button_width, button_height)  # Position set by container
            button = Button(rect, display_name, self.theme, button_type='system_button')
            button.system_path = path  # Store the path for later use
            builtin_buttons.append(button)
        
        self.builtin_container.set_items(builtin_buttons)
        
        # Create buttons for custom systems (empty for now)
        custom_buttons = []
        for name, path in custom_systems:
            display_name = name.replace('_', ' ').title()
            rect = pygame.Rect(0, 0, button_width, button_height)
            button = Button(rect, display_name, self.theme, button_type='system_button')
            button.system_path = path
            custom_buttons.append(button)
        
        self.custom_container.set_items(custom_buttons)
    
    def draw_title(self):
        """Draw the view title."""
        title_color = self.theme.get_color('title')
        title_shadow_color = self.theme.get_color('title_shadow')
        
        title_text = self.title_font.render("Load System", True, title_color)
        title_rect = title_text.get_rect(center=(self.width // 2, self.title_y + self.title_height // 2))
        
        # Draw shadow
        shadow_text = self.title_font.render("Load System", True, title_shadow_color)
        shadow_rect = shadow_text.get_rect(center=(title_rect.centerx + 2, title_rect.centery + 2))
        self.screen.blit(shadow_text, shadow_rect)
        self.screen.blit(title_text, title_rect)
    
    def run(self):
        """Run the load system view. Returns selected system path or None."""
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()[0]
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return 'back'
                
                # Handle container events
                self.builtin_container.handle_event(event)
                self.custom_container.handle_event(event)
                
                # Check for back button click
                if self.back_button.is_clicked(event):
                    return 'back'
                
                # Check for system selection
                clicked_item = self.builtin_container.get_clicked_item(event)
                if clicked_item:
                    return clicked_item.system_path
                
                clicked_item = self.custom_container.get_clicked_item(event)
                if clicked_item:
                    return clicked_item.system_path
            
            # Update
            self.builtin_container.update(mouse_pos, mouse_pressed)
            self.custom_container.update(mouse_pos, mouse_pressed)
            self.back_button.update(mouse_pos, mouse_pressed)
            
            # Draw
            self.draw_background()
            self.draw_title()
            self.builtin_container.draw(self.screen)
            self.custom_container.draw(self.screen)
            self.back_button.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        return None
