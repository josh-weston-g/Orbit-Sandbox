import pygame
import numpy as np
import random
from math import ceil
from orbit.simulation import Simulation
from orbit.loader import SystemLoader
from orbit.units import velocity_to_km_per_s

# Body colors for visualization
BODY_COLORS = [
    (255, 215, 0),   # Gold (Sun)
    (169, 169, 169), # Gray (Mercury)
    (255, 198, 73),  # Pale yellow (Venus)
    (100, 149, 237), # Cornflower blue (Earth)
    (205, 92, 92),   # Indian red (Mars)
    (210, 180, 140), # Tan (Jupiter)
    (238, 232, 170), # Pale goldenrod (Saturn)
    (175, 238, 238), # Pale turquoise (Uranus)
    (65, 105, 225),  # Royal blue (Neptune)
]

class SimulationRunner:
    """
    Handles simulation logic, physics updates, and rendering.
    Frame-based (no internal loop) - called by SimulationView.
    """
    
    def __init__(self, screen_size, system_path, clock):
        """Initialize the simulation with the given system"""
        # Load system
        self.bodies, self.G, self.metadata = SystemLoader.load_from_file(system_path)
        self.system_path = system_path # Store for potential reloads
        self.clock = clock

        # Screen dimensions
        self.window_width, self.window_height = screen_size

        # Load fonts
        try:
            self.icon_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 48)
            self.bold_hud_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Bold.ttf", 24)
            self.primary_hud_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 24)
            self.secondary_hud_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 20)
            self.primary_panel_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 20)
            self.secondary_panel_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 16)
        except FileNotFoundError:
            print("⚠ JetBrains Mono Nerd Font not found, using system font")
            self.icon_font = pygame.font.Font(None, 48)
            self.bold_hud_font = pygame.font.Font(None, 24)
            self.primary_hud_font = pygame.font.Font(None, 24)
            self.secondary_hud_font = pygame.font.Font(None, 20)
            self.primary_panel_font = pygame.font.Font(None, 20)
            self.secondary_panel_font = pygame.font.Font(None, 16)

        # Nerd font icon codes
        self.PAUSE_ICON = "\uf04c"
        self.REWIND_ICON = "\uf04a"

        # Timing and scale
        self.elapsed_sim_time = 0.0
        self.elapsed_real_time = 0.0
        self.scale = 200  # pixels per AU

        # Create simulation
        self.sim = Simulation(self.bodies, G=self.G, dt=0.001)

        # Physics timing
        self.physics_dt = self.sim.dt
        self.physics_accumulator = 0.0
        self.speed_multiplier = 0.1

        # Speed change settings
        self.speed_change_cooldown = 0.0
        self.SPEED_CHANGE_DELAY = 0.1

        # Trail settings - one trail per body
        self.max_trail_length = 200
        self.trails = [[] for _ in self.sim.bodies]

        # Camera settings
        self.camera_x, self.camera_y = 0.0, 0.0
        self.camera_speed = 1.0
        self.dragging = False
        self.last_mouse_pos = (0, 0)

        # Body selection
        self.selected_body_index = None # Which body is selected (None = no selection)
        self.close_button_rect = None  # Is set when drawing info panel

        # Toggle states
        self.paused = False
        self.rewinding = False
        self.show_grid = False
        self.show_trail = True
        self.show_energy = False

        # Create starfield
        self.starfield = []
        for _ in range(160):
            x = random.randint(0, self.window_width)
            y = random.randint(0, self.window_height)
            brightness = random.randint(100, 255)
            self.starfield.append((x, y, brightness))

        # Track if user wants to exit
        self._next_view = None

        print("Controls: \033[96mW,A,S,D\033[0m pan, \033[96mSPACE\033[0m pause, \033[96mLEFT\033[0m rewind, \033[96mUP/DOWN\033[0m speed, \033[96m+/-\033[0m zoom, \033[96mR\033[0m reset, \033[96mG\033[0m grid, \033[96mT\033[0m trail, \033[96mE\033[0m energy, \033[96mESC\033[0m menu")

    def handle_event(self, event):
        """Handle a sinlge pygame event."""
        if event.type == pygame.QUIT:
            self._next_view = 'quit'

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._next_view = 'main_menu'  # Return to main menu
            elif event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.key == pygame.K_r:
                # Reset simulation
                self.bodies, self.G, self.metadata = SystemLoader.load_from_file(self.system_path)
                self.sim = Simulation(self.bodies, G=self.G, dt=0.001)
                self.trails = [[] for _ in self.sim.bodies]
                self.elapsed_sim_time = 0.0
                self.elapsed_real_time = 0.0
                self.camera_x, self.camera_y = 0.0, 0.0
            elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                self.scale = min(2000, self.scale + 20)
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                self.scale = max(40, self.scale - 20)
            elif event.key == pygame.K_g:
                self.show_grid = not self.show_grid
            elif event.key == pygame.K_t:
                self.show_trail = not self.show_trail
            elif event.key == pygame.K_e:
                self.show_energy = not self.show_energy
            elif event.key == pygame.K_LEFT:
                self.paused = True # Ensure sim is paused when starting rewind
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.rewinding = False

        # Mouse click - check for body selection and then mouse drag
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            center_x, center_y = self.window_width // 2, self.window_height // 2
            clicked_body = False

            # Check if we clicked the close button
            if self.selected_body_index is not None and hasattr(self, 'close_button_rect'):
                if self.close_button_rect.collidepoint(mouse_x, mouse_y):
                    self.selected_body_index = None
                    clicked_body = True # Prevent drag from starting
            
            # Check if we clicked on any body (only if didn't click the close button)
            if not clicked_body:
                for i, body in enumerate(self.sim.bodies):
                    body_screen_x = center_x + ((body.pos[0] - self.camera_x) * self.scale)
                    body_screen_y = center_y - ((body.pos[1] - self.camera_y) * self.scale)

                    # Calculate distance from click to body center
                    distance = ((mouse_x - body_screen_x) ** 2 + (mouse_y - body_screen_y) ** 2) ** 0.5

                    if distance <= 8: #! Assuming body radius is 8 pixels - needs to be changed when variable body sizes are added back
                        self.selected_body_index = i
                        clicked_body = True
                        break

            # Only start draggin if we didn't click on a body
            if not clicked_body:
                self.dragging = True
                self.last_mouse_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        if event.type == pygame.MOUSEMOTION and self.dragging:
            dx = event.pos[0] - self.last_mouse_pos[0]
            dy = event.pos[1] - self.last_mouse_pos[1]
            self.camera_x -= dx / self.scale
            self.camera_y += dy / self.scale
            self.last_mouse_pos = event.pos

        # Mouse wheel zoom
        if event.type == pygame.MOUSEWHEEL:
            if event.y > 0:
                self.scale = min(2000, self.scale + 20)
            elif event.y < 0:
                self.scale = max(40, self.scale - 20)

    def update_physics(self, time_delta):
        """Update the physics simulation for one frame"""
        # Continuous key input for camera panning
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.camera_y += self.camera_speed * time_delta
        if keys[pygame.K_s]:
            self.camera_y -= self.camera_speed * time_delta
        if keys[pygame.K_a]:
            self.camera_x -= self.camera_speed * time_delta
        if keys[pygame.K_d]:
            self.camera_x += self.camera_speed * time_delta

        # Rewind controls (continuous while left is held)
        if keys[pygame.K_LEFT]:
            self.paused = True
            self.rewinding = True
            if self.sim.rewind_one_step():
                self.elapsed_sim_time = max(0.0, self.sim.time)
                # Pop trails for all bodies
                for trail in self.trails:
                    if len(trail) > 0:
                        trail.pop()

        # Speed adjustment with cooldown
        self.speed_change_cooldown -= time_delta
        if self.speed_change_cooldown <= 0.0:
            if keys[pygame.K_UP]:
                self.speed_multiplier += 0.01
                self.speed_change_cooldown = self.SPEED_CHANGE_DELAY
            elif keys[pygame.K_DOWN]:
                self.speed_multiplier = max(0.01, self.speed_multiplier - 0.01)
                self.speed_change_cooldown = self.SPEED_CHANGE_DELAY

        # Physics update
        self.physics_accumulator += time_delta * self.speed_multiplier
        if not self.paused:
            self.elapsed_sim_time += time_delta * self.speed_multiplier
            self.elapsed_real_time += time_delta
            while self.physics_accumulator >= self.physics_dt:
                self.sim.step()
                self.physics_accumulator -= self.physics_dt

                # Update trails every physics step
                for i, body in enumerate(self.sim.bodies):
                    self.trails[i].append((body.pos[0], body.pos[1]))
                    while len(self.trails[i]) > self.max_trail_length:
                        self.trails[i].pop(0)
        else:
            self.physics_accumulator = 0.0

    def draw(self, screen):
        """Draw the simulation for one frame."""
        # Screen center
        center_x, center_y = self.window_width // 2, self.window_height // 2

        # Calculate system energy if enabled
        if self.show_energy:
            kinetic_energy = 0.0
            potential_energy = 0.0
            
            for body in self.sim.bodies:
                kinetic_energy += 0.5 * body.mass * np.linalg.norm(body.vel)**2
            
            for i, body1 in enumerate(self.bodies):
                for j, body2 in enumerate(self.bodies):
                    if i < j:
                        r = np.linalg.norm(body1.pos - body2.pos)
                        potential_energy -= self.sim.G * body1.mass * body2.mass / r
            
            total_energy = kinetic_energy + potential_energy

        # === DRAWING ===
        screen.fill((0, 0, 0))

        # Draw starfield
        for x, y, brightness in self.starfield:
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)

        # Draw grid if enabled
        if self.show_grid:
            grid_color = (40, 40, 40)
            grid_spacing = 0.5
            visible_width = self.window_width / self.scale
            visible_height = self.window_height / self.scale
            
            left_edge = self.camera_x - (visible_width / 2)
            right_edge = self.camera_x + (visible_width / 2)
            x_physics = ceil(left_edge / grid_spacing) * grid_spacing
            while x_physics <= right_edge:
                screen_x = int(center_x + ((x_physics - self.camera_x) * self.scale))
                pygame.draw.line(screen, grid_color, (screen_x, 0), (screen_x, self.window_height), 1)
                x_physics += grid_spacing
            
            bottom_edge = self.camera_y - (visible_height / 2)
            top_edge = self.camera_y + (visible_height / 2)
            y_physics = ceil(bottom_edge / grid_spacing) * grid_spacing
            while y_physics <= top_edge:
                screen_y = int(center_y - ((y_physics - self.camera_y) * self.scale))
                pygame.draw.line(screen, grid_color, (0, screen_y), (self.window_width, screen_y), 1)
                y_physics += grid_spacing

        # Draw trails for all bodies
        if self.show_trail:
            for i, trail in enumerate(self.trails):
                if len(trail) > 1:
                    color = BODY_COLORS[i % len(BODY_COLORS)]
                    trail_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
                    
                    trail_screen = []
                    for px, py in trail:
                        sx = int(center_x + ((px - self.camera_x) * self.scale))
                        sy = int(center_y - ((py - self.camera_y) * self.scale))
                        trail_screen.append((sx, sy))
                    
                    for j in range(len(trail_screen) - 1):
                        alpha = int(255 * (j + 1) / len(trail_screen))
                        pygame.draw.line(trail_surface, (*color, alpha), 
                                        trail_screen[j], trail_screen[j + 1], 1)
                    
                    screen.blit(trail_surface, (0, 0))

        # Draw all bodies
        for i, body in enumerate(self.sim.bodies):
            # Convert position to screen coordinates
            body_screen_x = center_x + ((body.pos[0] - self.camera_x) * self.scale)
            body_screen_y = center_y - ((body.pos[1] - self.camera_y) * self.scale)
            
            # Fixed body radius
            body_radius = 8
            body_border_radius = body_radius + 2
            
            # Get color from palette
            color = BODY_COLORS[i % len(BODY_COLORS)]
            
            # Highlight selected body - must be drawn first to appear underneath
            if self.selected_body_index == i:
                pygame.draw.circle(screen, (255, 0, 0), (int(body_screen_x), int(body_screen_y)), body_border_radius)
            
            pygame.draw.circle(screen, color, (int(body_screen_x), int(body_screen_y)), body_radius)


        # === HUD ===
        # TOP-RIGHT: Technical info
        fps_text = self.primary_hud_font.render(f"FPS: {self.clock.get_fps():.0f}", True, (255, 255, 255))
        zoom_text = self.primary_hud_font.render(f"Zoom: {(self.scale / 200):.2f}x", True, (255, 255, 255))
        bodies_text = self.primary_hud_font.render(f"Bodies: {len(self.sim.bodies)}", True, (255, 255, 255))
        screen.blit(fps_text, (self.window_width - fps_text.get_width() - 10, 10))
        screen.blit(zoom_text, (self.window_width - zoom_text.get_width() - 10, 40))
        screen.blit(bodies_text, (self.window_width - bodies_text.get_width() - 10, 70))

        # TOP-LEFT: Simulation timing
        sim_speed_text = self.primary_hud_font.render(f"Speed: {(self.speed_multiplier * 10):.1f}x", True, (255, 255, 255))
        elapsed_sim_time_text = self.primary_hud_font.render(f"Sim Time: {self.elapsed_sim_time:.2f} years", True, (255, 255, 255))
        elapsed_real_time_text = self.primary_hud_font.render(f"Real Time: {self.elapsed_real_time:.2f}s", True, (255, 255, 255))
        screen.blit(sim_speed_text, (10, 10))
        screen.blit(elapsed_sim_time_text, (10, 40))
        screen.blit(elapsed_real_time_text, (10, 70))

        # MIDDLE-LEFT: Energy display if enabled
        if self.show_energy:
            ke_text = self.primary_hud_font.render(f"KE: {kinetic_energy:.4e}", True, (100, 255, 100))
            pe_text = self.primary_hud_font.render(f"PE: {potential_energy:.4e}", True, (255, 100, 100))
            te_text = self.primary_hud_font.render(f"Total: {total_energy:.4e}", True, (255, 255, 100))
            screen.blit(ke_text, (10, self.window_height // 2 - 30))
            screen.blit(pe_text, (10, self.window_height // 2))
            screen.blit(te_text, (10, self.window_height // 2 + 30))

        # BOTTOM-LEFT: Scale bar
        scale_bar_color = (200, 200, 200)
        scale_bar_x = 20
        scale_bar_y = self.window_height - 40
        scale_bar_length = int(0.5 * self.scale)
        pygame.draw.line(screen, scale_bar_color, (scale_bar_x, scale_bar_y), (scale_bar_x + scale_bar_length, scale_bar_y), 2)
        pygame.draw.line(screen, scale_bar_color, (scale_bar_x, scale_bar_y - 5), (scale_bar_x, scale_bar_y + 5), 2)
        pygame.draw.line(screen, scale_bar_color, (scale_bar_x + scale_bar_length, scale_bar_y - 5), (scale_bar_x + scale_bar_length, scale_bar_y + 5), 2)
        scale_label = self.secondary_hud_font.render("0.5 AU", True, scale_bar_color)
        screen.blit(scale_label, (scale_bar_x, scale_bar_y - 30))

        # === BODY INFO PANEL (Bottom-Right) ===
        if self.selected_body_index is not None:
            body = self.sim.bodies[self.selected_body_index]
            
            # Get body name and other attributes
            body_name = body.name
            body_type = getattr(body, 'type', "body")
            body_mass = body.mass
            body_vel = body.vel
            body_vel_magnitude = np.linalg.norm(body_vel)

            # Find distance to closest other body
            min_distance = float('inf')
            closest_body_name = "N/A"
            for i, other_body in enumerate(self.sim.bodies):
                if i != self.selected_body_index:
                    distance = np.linalg.norm(body.pos - other_body.pos)
                    if distance < min_distance:
                        min_distance = distance
                        closest_body_name = other_body.name
            
            # Render all text surfaces first to measure them
            name_text = self.bold_hud_font.render(body_name, True, (255, 255, 255))
            type_text = self.primary_panel_font.render(f"({body_type})", True, (200, 200, 200))
            mass_text = self.primary_panel_font.render(f"Mass: {body_mass:.3g} M⊙", True, (255, 255, 255))
            vel_mag_text = self.primary_panel_font.render(f"Velocity: {body_vel_magnitude:.3g} AU/yr", True, (255, 255, 255))
            vel_kms_text = self.primary_panel_font.render(f"         ({velocity_to_km_per_s(body_vel_magnitude):.3g} km/s)", True, (200, 200, 200))
            vel_vec_text = self.secondary_panel_font.render(f"(vx: {body_vel[0]:.3g}, vy: {body_vel[1]:.3g}) AU/yr", True, (200, 200, 200))
            distance_text = self.primary_panel_font.render(f"Closest Body: {closest_body_name} ({min_distance:.3g} AU)", True, (255, 255, 255))
            
            # Calculate required width
            name_width = name_text.get_width()
            type_width = type_text.get_width()
            combined_name_type_width = name_width + 5 + type_width  # 5 for spacing
            max_width = max(
                combined_name_type_width,
                mass_text.get_width(),
                vel_mag_text.get_width(),
                vel_kms_text.get_width(),
                vel_vec_text.get_width(),
                distance_text.get_width()
            )
            
            # Panel dimensions with dynamic width based on longest line of text
            min_panel_width = 400
            panel_width = max(min_panel_width, max_width + 20)  # +20 for padding
            panel_height = 200
            panel_x = self.window_width - panel_width - 20
            panel_y = self.window_height - panel_height - 20
            
            # Create semi-transparent background
            info_panel = pygame.Surface((panel_width, panel_height))
            info_panel.set_alpha(200)
            info_panel.fill((40, 40, 40))
            screen.blit(info_panel, (panel_x, panel_y))
            
            # Draw close button (X in top-right of panel)
            close_button_x = panel_x + panel_width - 25
            close_button_y = panel_y + 5
            close_button_size = 20

            # Store close button rect for click detection
            self.close_button_rect = pygame.Rect(close_button_x, close_button_y, close_button_size, close_button_size)

            # Check if mouse is hovering over close button
            mouse_pos = pygame.mouse.get_pos()
            is_hovering = self.close_button_rect.collidepoint(mouse_pos)
            
            # X button background (brighter red when hovering)
            close_bg_color = (200, 70, 70) if is_hovering else (80, 40, 40)
            pygame.draw.rect(screen, close_bg_color, 
                        (close_button_x, close_button_y, close_button_size, close_button_size))
            
            # X text
            x_text = self.secondary_hud_font.render("×", True, (255, 255, 255))
            screen.blit(x_text, (close_button_x + 4, close_button_y - 2))
            
            # Draw body info text
            screen.blit(name_text, (panel_x + 10, panel_y + 10))
            screen.blit(type_text, (panel_x + 10 + name_width + 5, panel_y + 10 + 4)) # Slight offset to align with name
            screen.blit(mass_text, (panel_x + 10, panel_y + 40))   # Normal spacing of 25 pixels, 30 here to add extra space
            screen.blit(vel_mag_text, (panel_x + 10, panel_y + 65))
            screen.blit(vel_kms_text, (panel_x + 10, panel_y + 90))
            screen.blit(vel_vec_text, (panel_x + 10, panel_y + 115))
            screen.blit(distance_text, (panel_x + 10, panel_y + 140))

        # === PAUSE/REWIND INDICATOR (Center-Top) ===
        if self.rewinding:
            # Rewind indicator
            indicator_text = self.icon_font.render(f"{self.REWIND_ICON} REWINDING", True, (255, 100, 100))
            indicator_bg = pygame.Surface((indicator_text.get_width() + 40, indicator_text.get_height() + 20))
            indicator_bg.set_alpha(200)
            indicator_bg.fill((40, 20, 20))
            
            indicator_x = (self.window_width - indicator_bg.get_width()) // 2
            indicator_y = 20
            
            screen.blit(indicator_bg, (indicator_x, indicator_y))
            screen.blit(indicator_text, (indicator_x + 20, indicator_y + 10))

        elif self.paused:
            # Pause indicator
            indicator_text = self.icon_font.render(f"{self.PAUSE_ICON} PAUSED", True, (255, 255, 100))
            indicator_bg = pygame.Surface((indicator_text.get_width() + 40, indicator_text.get_height() + 20))
            indicator_bg.set_alpha(200)
            indicator_bg.fill((40, 40, 20))
            
            indicator_x = (self.window_width - indicator_bg.get_width()) // 2
            indicator_y = 20
            
            screen.blit(indicator_bg, (indicator_x, indicator_y))
            screen.blit(indicator_text, (indicator_x + 20, indicator_y + 10))

        pygame.display.flip()

    def get_requested_next_view(self):
        """Return next view if users wants to exit (i.e., ESC pressed)."""
        next_view = self._next_view
        self._next_view = None # Reset after reading
        return next_view