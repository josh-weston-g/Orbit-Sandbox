import pygame
import numpy as np
import random
from math import ceil
from orbit.simulation import Simulation
from orbit.loader import SystemLoader

# Resolution mapping
RESOLUTION_MAP = {
    '720p': (1280, 720),
    '1080p': (1920, 1080),
    '1440p': (2560, 1440)
}

# Color palette for bodies
BODY_COLORS = [
    (255, 255, 0),    # Yellow
    (100, 150, 255),  # Blue
    (255, 100, 100),  # Red
    (100, 255, 100),  # Green
    (255, 150, 50),   # Orange
    (200, 100, 255),  # Purple
    (255, 255, 255),  # White
    (0, 255, 255),    # Cyan
]

def show_menu():
    """Show a simple menu to choose orbital scenario. Returns scenario string or None."""
    pygame.init()
    
    # Get available systems
    available_systems = SystemLoader.list_systems("data/systems")
    
    # Calculate window height based on number of systems
    num_systems = len(available_systems) if available_systems else 1
    title_space = 100  # Space for title at top
    exit_button_space = 100  # Space for exit button at bottom
    button_width = 400
    button_height = 60
    button_x = 150
    button_spacing = 70
    start_y = 100
    window_height = title_space + (num_systems * button_spacing) + exit_button_space
    
    screen = pygame.display.set_mode((700, window_height))
    pygame.display.set_caption("Orbit Simulator - Choose Scenario")

    # Load fonts
    try:
        font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 32)
        title_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Bold.ttf", 48)
    except FileNotFoundError:
        print("⚠ JetBrains Mono Nerd Font not found, using system font")
        font = pygame.font.Font(None, 32)
        title_font = pygame.font.Font(None, 48)

    # Create buttons dynamically from available systems
    buttons = {}
    for i, (system_name, system_path) in enumerate(available_systems):
        button_y = start_y + (i * button_spacing)
        buttons[system_name] = {
            'rect': pygame.Rect(button_x, button_y, button_width, button_height),
            'path': system_path,
            'display_name': system_name.replace('_', ' ').title()
        }
    
    # Add exit button at the bottom
    exit_y = start_y + (len(available_systems) * button_spacing) + 30
    buttons['exit'] = {
        'rect': pygame.Rect(button_x, exit_y, button_width, button_height),
        'path': None,
        'display_name': 'Exit'
    }

    button_color = (70, 70, 70)
    hover_color = (100, 100, 100)
    text_color = (255, 255, 255)
    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return None
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for system_name, button_data in buttons.items():
                    if button_data['rect'].collidepoint(mouse_pos):
                        if system_name == 'exit':
                            pygame.quit()
                            return None
                        else:
                            pygame.quit()
                            return button_data['path']  # Return the file path instead of scenario name
                    
        screen.fill((30, 30, 30))

        title_text = title_font.render("Choose Orbital Scenario", True, text_color)
        title_rect = title_text.get_rect(center=(350, 50))  # Fixed from (350, 30)
        screen.blit(title_text, title_rect)

        screen.fill((30, 30, 30))

        # Draw title
        title_text = title_font.render("Choose Orbital Scenario", True, text_color)
        title_rect = title_text.get_rect(center=(350, 50))  # Fixed from (350, 30)
        screen.blit(title_text, title_rect)

        # If no systems found, show error message
        if not available_systems:
            error_text = font.render("No systems found in data/systems/", True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(350, 300))
            screen.blit(error_text, error_rect)
        else:
            # Draw buttons
            for system_name, button_data in buttons.items():
                rect = button_data['rect']
                color = hover_color if rect.collidepoint(mouse_pos) else button_color
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, text_color, rect, 2)
                
                # Use display_name for button text
                text = font.render(button_data['display_name'], True, text_color)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)


def run_visualization(scenario, planet_data, resolution):
    """Run the orbit simulation visualization using Pygame."""
    # If no scenario provided, show menu
    if scenario is None:
        scenario = show_menu()
        if scenario is None:
            return
    
    # Load system from JSON file
    bodies, G, metadata = SystemLoader.load_from_file(scenario)

    # Initialize Pygame
    pygame.init()

    # Font Setup
    try:
        icon_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 48)
        primary_hud_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 24)
        secondary_hud_font = pygame.font.Font("assets/fonts/JetBrainsMonoNerdFont-Regular.ttf", 20)
    except FileNotFoundError:
        print("⚠ JetBrains Mono Nerd Font not found, using system font")
        icon_font = pygame.font.Font(None, 48)
        primary_hud_font = pygame.font.Font(None, 24)
        secondary_hud_font = pygame.font.Font(None, 20)

    # Nerd Font icon codes
    PAUSE_ICON = "\uf04c"
    REWIND_ICON = "\uf04a"
    # Set resolution
    if resolution == 'auto':
        display_info = pygame.display.Info()
        window_width, window_height = display_info.current_w, display_info.current_h
        screen = pygame.display.set_mode((window_width, window_height), pygame.NOFRAME)
    else:
        window_width, window_height = RESOLUTION_MAP[resolution]
        screen = pygame.display.set_mode((window_width, window_height))

    pygame.display.set_caption("Orbit Simulation Visualization")

    # Create clock and timing
    clock = pygame.time.Clock()
    FPS = 60
    scale = 200  # pixels per AU
    elapsed_sim_time = 0.0
    elapsed_real_time = 0.0

    # Create simulation
    sim = Simulation(bodies, G=G, dt=0.001)

    # Physics timing
    physics_dt = sim.dt
    physics_accumulator = 0.0
    speed_multiplier = 0.1

    # Speed change settings
    speed_change_cooldown = 0.0
    SPEED_CHANGE_DELAY = 0.1

    # Trail settings - one trail per body
    max_trail_length = 200
    trails = [[] for _ in sim.bodies]  # List of trails, one per body

    # Camera settings
    camera_x, camera_y = 0.0, 0.0
    camera_speed = 1.0
    dragging = False
    last_mouse_pos = (0, 0)

    # Toggle states
    paused = False
    rewinding  = False
    show_grid = False
    show_trail = True
    show_energy = False

    # Create static starfield background
    starfield = []
    for _ in range(160):
        x = random.randint(0, window_width)
        y = random.randint(0, window_height)
        brightness = random.randint(100, 255)
        starfield.append((x, y, brightness))

    print("Controls: \033[96mW,A,S,D\033[0m pan, \033[96mSPACE\033[0m pause, \033[96mLEFT\033[0m rewind (paused), \033[96mUP/DOWN\033[0m speed, \033[96m+/-\033[0m zoom, \033[96mR\033[0m reset, \033[96mG\033[0m grid, \033[96mT\033[0m trail, \033[96mE\033[0m energy, \033[96mESC\033[0m menu")

    # Initialize frame_time before main loop
    frame_time = 0.0

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Reset simulation
                    bodies, G, metadata = SystemLoader.load_from_file(scenario)
                    sim = Simulation(bodies, G=G, dt=0.001)
                    trails = [[] for _ in sim.bodies]
                    elapsed_sim_time = 0.0
                    elapsed_real_time = 0.0
                    camera_x, camera_y = 0.0, 0.0
                    print("Simulation reset.")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run_visualization(None, planet_data, resolution)
                    return
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    scale = min(2000, scale * 1.1)
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    scale = max(50, scale / 1.1)
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
                elif event.key == pygame.K_t:
                    show_trail = not show_trail
                elif event.key == pygame.K_e:
                    show_energy = not show_energy
                elif event.key == pygame.K_LEFT:
                    paused = True # Ensure sim is paused when starting rewind
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    rewinding = False

            # Mouse drag for panning
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                dragging = True
                last_mouse_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                dragging = False
            if event.type == pygame.MOUSEMOTION and dragging:
                dx = event.pos[0] - last_mouse_pos[0]
                dy = event.pos[1] - last_mouse_pos[1]
                camera_x -= dx / scale
                camera_y += dy / scale
                last_mouse_pos = event.pos

            # Mouse wheel zoom
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    scale = min(2000, scale + 20)
                elif event.y < 0:
                    scale = max(40, scale - 20)

        # Continuous key input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera_y += camera_speed * frame_time
        if keys[pygame.K_s]:
            camera_y -= camera_speed * frame_time
        if keys[pygame.K_a]:
            camera_x -= camera_speed * frame_time
        if keys[pygame.K_d]:
            camera_x += camera_speed * frame_time

        # Rewind controls (while paused)
        if keys[pygame.K_LEFT]:
            paused = True
            rewinding = True
            if sim.rewind_one_step():
                elapsed_sim_time = max(0.0, sim.time)
                # Pop trails for all bodies
                for trail in trails:
                    if len(trail) > 0:
                        trail.pop()

        frame_time = clock.tick(FPS) / 1000.0

        # Speed adjustment
        speed_change_cooldown -= frame_time
        if speed_change_cooldown <= 0.0:
            if keys[pygame.K_UP]:
                speed_multiplier += 0.01
                speed_change_cooldown = SPEED_CHANGE_DELAY
            elif keys[pygame.K_DOWN]:
                speed_multiplier = max(0.01, speed_multiplier - 0.01)
                speed_change_cooldown = SPEED_CHANGE_DELAY

        # Physics update
        physics_accumulator += frame_time * speed_multiplier
        if not paused:
            elapsed_sim_time += frame_time * speed_multiplier
            elapsed_real_time += frame_time
            while physics_accumulator >= physics_dt:
                sim.step()
                physics_accumulator -= physics_dt

                # Update trails every physics step
                for i, body in enumerate(sim.bodies):
                    trails[i].append((body.pos[0], body.pos[1]))
                    while len(trails[i]) > max_trail_length:
                        trails[i].pop(0)
        else:
            physics_accumulator = 0.0

        # Screen center
        center_x, center_y = window_width // 2, window_height // 2

        # Calculate system energy if enabled
        if show_energy:
            kinetic_energy = 0.0
            potential_energy = 0.0
            
            for body in sim.bodies:
                kinetic_energy += 0.5 * body.mass * np.linalg.norm(body.vel)**2
            
            for i, body1 in enumerate(sim.bodies):
                for j, body2 in enumerate(sim.bodies):
                    if i < j:
                        r = np.linalg.norm(body1.pos - body2.pos)
                        potential_energy -= sim.G * body1.mass * body2.mass / r
            
            total_energy = kinetic_energy + potential_energy

        # === DRAWING ===
        screen.fill((0, 0, 0))

        # Draw starfield
        for x, y, brightness in starfield:
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)

        # Draw grid if enabled
        if show_grid:
            grid_color = (40, 40, 40)
            grid_spacing = 0.5
            visible_width = window_width / scale
            visible_height = window_height / scale
            
            left_edge = camera_x - (visible_width / 2)
            right_edge = camera_x + (visible_width / 2)
            x_physics = ceil(left_edge / grid_spacing) * grid_spacing
            while x_physics <= right_edge:
                screen_x = int(center_x + ((x_physics - camera_x) * scale))
                pygame.draw.line(screen, grid_color, (screen_x, 0), (screen_x, window_height), 1)
                x_physics += grid_spacing
            
            bottom_edge = camera_y - (visible_height / 2)
            top_edge = camera_y + (visible_height / 2)
            y_physics = ceil(bottom_edge / grid_spacing) * grid_spacing
            while y_physics <= top_edge:
                screen_y = int(center_y - ((y_physics - camera_y) * scale))
                pygame.draw.line(screen, grid_color, (0, screen_y), (window_width, screen_y), 1)
                y_physics += grid_spacing

        # Draw trails for all bodies
        if show_trail:
            for i, trail in enumerate(trails):
                if len(trail) > 1:
                    color = BODY_COLORS[i % len(BODY_COLORS)]
                    trail_surface = pygame.Surface((window_width, window_height), pygame.SRCALPHA)
                    
                    trail_screen = []
                    for px, py in trail:
                        sx = int(center_x + ((px - camera_x) * scale))
                        sy = int(center_y - ((py - camera_y) * scale))
                        trail_screen.append((sx, sy))
                    
                    for j in range(len(trail_screen) - 1):
                        alpha = int(255 * (j + 1) / len(trail_screen))
                        pygame.draw.line(trail_surface, (*color, alpha), 
                                        trail_screen[j], trail_screen[j + 1], 1)
                    
                    screen.blit(trail_surface, (0, 0))

        # Draw all bodies
        for i, body in enumerate(sim.bodies):
            # Convert position to screen coordinates
            body_screen_x = center_x + ((body.pos[0] - camera_x) * scale)
            body_screen_y = center_y - ((body.pos[1] - camera_y) * scale)
            
            # Fixed body radius (can be made mass-dependent later)
            body_radius = 8
            
            # Get color from palette
            color = BODY_COLORS[i % len(BODY_COLORS)]
            
            pygame.draw.circle(screen, color, (int(body_screen_x), int(body_screen_y)), body_radius)

        # === HUD ===
        screen_width = screen.get_width()
        screen_height = screen.get_height()

        # TOP-RIGHT: Technical info
        fps_text = primary_hud_font.render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
        zoom_text = primary_hud_font.render(f"Zoom: {(scale / 200):.2f}x", True, (255, 255, 255))
        bodies_text = primary_hud_font.render(f"Bodies: {len(sim.bodies)}", True, (255, 255, 255))
        screen.blit(fps_text, (screen_width - fps_text.get_width() - 10, 10))
        screen.blit(zoom_text, (screen_width - zoom_text.get_width() - 10, 40))
        screen.blit(bodies_text, (screen_width - bodies_text.get_width() - 10, 70))

        # TOP-LEFT: Simulation timing
        sim_speed_text = primary_hud_font.render(f"Speed: {(speed_multiplier * 10):.1f}x", True, (255, 255, 255))
        elapsed_sim_time_text = primary_hud_font.render(f"Sim Time: {elapsed_sim_time:.2f} years", True, (255, 255, 255))
        elapsed_real_time_text = primary_hud_font.render(f"Real Time: {elapsed_real_time:.2f}s", True, (255, 255, 255))
        screen.blit(sim_speed_text, (10, 10))
        screen.blit(elapsed_sim_time_text, (10, 40))
        screen.blit(elapsed_real_time_text, (10, 70))

        # MIDDLE-LEFT: Energy display if enabled
        if show_energy:
            ke_text = primary_hud_font.render(f"KE: {kinetic_energy:.4e}", True, (100, 255, 100))
            pe_text = primary_hud_font.render(f"PE: {potential_energy:.4e}", True, (255, 100, 100))
            te_text = primary_hud_font.render(f"Total: {total_energy:.4e}", True, (255, 255, 100))
            screen.blit(ke_text, (10, screen_height // 2 - 30))
            screen.blit(pe_text, (10, screen_height // 2))
            screen.blit(te_text, (10, screen_height // 2 + 30))

        # BOTTOM-LEFT: Scale bar
        scale_bar_color = (200, 200, 200)
        scale_bar_x = 20
        scale_bar_y = screen_height - 40
        scale_bar_length = int(0.5 * scale)
        pygame.draw.line(screen, scale_bar_color, (scale_bar_x, scale_bar_y), (scale_bar_x + scale_bar_length, scale_bar_y), 2)
        pygame.draw.line(screen, scale_bar_color, (scale_bar_x, scale_bar_y - 5), (scale_bar_x, scale_bar_y + 5), 2)
        pygame.draw.line(screen, scale_bar_color, (scale_bar_x + scale_bar_length, scale_bar_y - 5), (scale_bar_x + scale_bar_length, scale_bar_y + 5), 2)
        scale_label = secondary_hud_font.render("0.5 AU", True, scale_bar_color)
        screen.blit(scale_label, (scale_bar_x, scale_bar_y - 30))

        # === PAUSE/REWIND INDICATOR (Center-Top) ===
        if rewinding:
            # Rewind indicator
            indicator_text = icon_font.render(f"{REWIND_ICON} REWINDING", True, (255, 100, 100))
            indicator_bg = pygame.Surface((indicator_text.get_width() + 40, indicator_text.get_height() + 20))
            indicator_bg.set_alpha(200)
            indicator_bg.fill((40, 20, 20))
            
            indicator_x = (screen_width - indicator_bg.get_width()) // 2
            indicator_y = 20
            
            screen.blit(indicator_bg, (indicator_x, indicator_y))
            screen.blit(indicator_text, (indicator_x + 20, indicator_y + 10))

        elif paused:
            # Pause indicator
            indicator_text = icon_font.render(f"{PAUSE_ICON} PAUSED", True, (255, 255, 100))
            indicator_bg = pygame.Surface((indicator_text.get_width() + 40, indicator_text.get_height() + 20))
            indicator_bg.set_alpha(200)
            indicator_bg.fill((40, 40, 20))
            
            indicator_x = (screen_width - indicator_bg.get_width()) // 2
            indicator_y = 20
            
            screen.blit(indicator_bg, (indicator_x, indicator_y))
            screen.blit(indicator_text, (indicator_x + 20, indicator_y + 10))

        pygame.display.flip()

    pygame.quit()
