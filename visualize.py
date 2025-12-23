import pygame
from simulation import Simulation
from body import Body
from systems import create_simple_system, create_elliptical_orbit, create_escape_trajectory

def show_menu():
    """Show a simple menu to choose orbital scenario. Returns scenario string or None."""
    pygame.init()
    screen = pygame.display.set_mode((600, 450))
    pygame.display.set_caption("Orbit Simulator - Choose Scenario")

    # Defin button rectangles (x, y, width, height)
    button_width = 400
    button_height = 60
    button_x = 100 # Centered horizontally

    buttons = {
        'circular': pygame.Rect(button_x, 80, button_width, button_height),
        'elliptical': pygame.Rect(button_x, 160, button_width, button_height),
        'escape': pygame.Rect(button_x, 240, button_width, button_height),
        'exit': pygame.Rect(button_x, 350, button_width, button_height)
    }

    # Button colors
    button_color = (70, 70, 70)
    hover_color = (100, 100, 100)
    text_color = (255, 255, 255)

    # Font for button text
    font = pygame.font.Font(None, 36)
    
    clock = pygame.time.Clock()
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                return None # User closed window
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check which button was clicked
                for scenario, rect in buttons.items():
                    if rect.collidepoint(mouse_pos):
                        pygame.quit()  # Close menu window
                        return scenario  # Return chosen scenario
                    
        # Draw everything
        screen.fill((30, 30, 30))  # Background color

        # Draw title
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Choose Orbital Scenario", True, text_color)
        title_rect = title_text.get_rect(center=(300, 30))
        screen.blit(title_text, title_rect)

        # Draw buttons
        for scenario, rect in buttons.items():
            # Change color if mouse is hovering
            color = hover_color if rect.collidepoint(mouse_pos) else button_color
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, text_color, rect, 2) # Border

            # Draw button text
            text = font.render(scenario.title(), True, text_color)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS

def run_visualization(scenario):
    """Run the orbit simulation visualization using Pygame."""
    # If no scenario provided, show menu to choose one
    if scenario is None:
        scenario = show_menu()
        if scenario is None or scenario == 'exit':
            return  # User exited menu
    
    # Map scenario string to factory functions
    scenario_map = {
        'circular': create_simple_system,
        'elliptical': create_elliptical_orbit,
        'escape': create_escape_trajectory
    }
    # Get factory function and create system
    factory = scenario_map[scenario]
    bodies, G = factory()

    # Initialize Pygame
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Orbit Simulation Visualization")

    # Create a clock to control frame rate
    clock = pygame.time.Clock()
    FPS = 60
    paused = False
    scale = 200  # pixels per unit distance
    elapsed_time = 0.0


    # Create the physics simulation
    sim = Simulation(bodies, G=G, dt=0.001)
    planet = bodies[1]
    star = bodies[0]

    # Physics timing
    physics_dt = sim.dt  # Must match sim.dt
    physics_accumulator = 0.0
    speed_multiplier = 0.1  # 10 real seconds per simulated year

    # Key delay settings
    speed_change_cooldown= 0.0 # Timer for speed changes
    SPEED_CHANGE_DELAY = 0.1 # Seconds between speed changes
    
    # Trail settings
    trail = []
    max_trail_length = 50

    # Setting States
    # Grid toggle
    show_grid = False
    # Trail toggle
    show_trail = True

    # Create static starfield
    starfield = []
    import random
    for _ in range(100):  # 100 starts
        x = random.randint(0, 800) # Screen width
        y = random.randint(0, 600) # Screen height
        brightness = random.randint(100, 255)
        starfield.append((x, y, brightness))

    # Main loop
    print("Controls: \033[96mSPACE\033[0m to pause/resume, \033[96mUP/DOWN\033[0m to adjust speed, \033[96mR\033[0m to reset, \033[96mG\033[0m to toggle grid, \033[96mT\033[0m to toggle trail, \033[96mESC\033[0m to return to menu")

    # Create font for HUD
    hud_font = pygame.font.Font(None, 24)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_r:
                    # Reset simulation - to be added
                    bodies, G = factory() # Recreate bodies from same factory
                    sim = Simulation(bodies, G=G, dt=0.001) # New simulation
                    planet = bodies[1]
                    star = bodies[0]
                    trail = [] # Clear trail
                    elapsed_time = 0.0 # Reset elapsed time
                    print("Simulation reset.")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run_visualization(None)  # Show menu again
                    return
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    scale *= 1.1
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    scale = max(1/5, scale / 1.1)  # Prevent too much zoom out - stops when planets get to min size
                elif event.key == pygame.K_g:
                    show_grid = not show_grid
                    print(f"Grid {'enabled' if show_grid else 'disabled'}.")
                elif event.key == pygame.K_t:
                    show_trail = not show_trail
                    print(f"Trail {'enabled' if show_trail else 'disabled'}.")

            # Mouse wheel for zooming
            if event.type == pygame.MOUSEWHEEL:
                # Zoom in/out
                if event.y > 0:
                    scale *= 1.1
                elif event.y < 0:
                    scale = max(1/5, scale / 1.1)  # Prevent too much zoom out - stops when planets get to min size

        frame_time = clock.tick(FPS) / 1000.0  # milliseconds to seconds
        # Adjust speed multiplier with up/down keys - allows for holding keys down
        keys = pygame.key.get_pressed()
        speed_change_cooldown -= frame_time
        if speed_change_cooldown <= 0.0:
            if keys[pygame.K_UP]:
                speed_multiplier += 0.01
                speed_change_cooldown = SPEED_CHANGE_DELAY
            elif keys[pygame.K_DOWN]:
                speed_multiplier = max(0.01, speed_multiplier - 0.01)
                speed_change_cooldown = SPEED_CHANGE_DELAY

        # How much real time passed since last frame?
        physics_accumulator += frame_time * speed_multiplier
        
        # Run enough physics steps to catch up and update elapsed time
        if not paused:
            elapsed_time += frame_time * speed_multiplier
            while physics_accumulator >= physics_dt:
                sim.step()
                physics_accumulator -= physics_dt
        else:
            physics_accumulator = 0.0  # Prevent accumulation while paused
        
        # Convert physics coorrdinates to screen coordinates
        # Physics: (0,0) is center, +x right, +y up
        # Screen: (0,0) is top-left, +x right, +y down
        center_x, center_y = 400, 300
        
        # Convert planet position
        planet_screen_x = center_x + (planet.pos[0] * scale)
        planet_screen_y = center_y - (planet.pos[1] * scale) # Flip y-axis

        # Convert star position
        star_screen_x = center_x + (star.pos[0] * scale)
        star_screen_y = center_y - (star.pos[1] * scale) # Flip y-axis

        # Calculate stats for HUD for using numpy
        import numpy as np
        distance = np.linalg.norm(planet.pos - star.pos)
        velocity = np.linalg.norm(planet.vel)

        screen.fill((0, 0, 0))  # Clear screen with black

        # Draw starfield
        for x, y, brightness in starfield:
            pygame.draw.circle(screen, (brightness, brightness, brightness), (x, y), 1)
        
        # Draw grid if enabled
        if show_grid:
            grid_color = (40, 40, 40)  # Dark gray
            grid_spacing = 0.5  # Spacing in physics units
            
            # Calculate how many grid lines we need based on screen size and scale
            # We need to cover the visible area in physics space
            visible_width = screen.get_width() / scale  # How many physics units wide is the screen?
            visible_height = screen.get_height() / scale  # How many physics units tall?
            
            # Draw vertical lines (parallel to y-axis)
            # Start from center and go left and right
            x_physics = 0  # Start at origin
            while x_physics <= visible_width / 2:
                # Convert physics x to screen x for both positive and negative
                screen_x_pos = int(center_x + (x_physics * scale))
                screen_x_neg = int(center_x + (-x_physics * scale))
                
                # Draw line from top to bottom of screen
                pygame.draw.line(screen, grid_color, (screen_x_pos, 0), (screen_x_pos, screen.get_height()), 1)
                if x_physics != 0:  # Don't draw center line twice
                    pygame.draw.line(screen, grid_color, (screen_x_neg, 0), (screen_x_neg, screen.get_height()), 1)
                
                x_physics += grid_spacing
            
            # Draw horizontal lines (parallel to x-axis)
            y_physics = 0  # Start at origin
            while y_physics <= visible_height / 2:
                # Convert physics y to screen y for both positive and negative
                screen_y_pos = int(center_y - (y_physics * scale))  # Remember: screen y is flipped
                screen_y_neg = int(center_y - (-y_physics * scale))
                
                # Draw line from left to right of screen
                pygame.draw.line(screen, grid_color, (0, screen_y_pos), (screen.get_width(), screen_y_pos), 1)
                if y_physics != 0:  # Don't draw center line twice
                    pygame.draw.line(screen, grid_color, (0, screen_y_neg), (screen.get_width(), screen_y_neg), 1)
                
                y_physics += grid_spacing
        
        # Update trail
        if not paused:
            trail.append((planet.pos[0], planet.pos[1]))
            if len(trail) > max_trail_length:
                trail.pop(0)  # Remove oldest point
        
        if show_trail:        
            # Draw the trail
            if len(trail) > 1:
                # Create one surface for the entire trail
                trail_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
                
                # Convert physics coordinates to screen coordinates
                trail_screen = []
                for px, py in trail:
                    screen_x = int(center_x + (px * scale))
                    screen_y = int(center_y - (py * scale))
                    trail_screen.append((screen_x, screen_y))
                
                # Draw all segments on it
                for i in range(len(trail_screen) - 1):
                    alpha = int(255 * (i + 1) / len(trail_screen))
                    pygame.draw.line(trail_surface, (40, 122, 184, alpha), 
                                    trail_screen[i], trail_screen[i + 1], 1)
                
                # Blit surface onto main screen
                screen.blit(trail_surface, (0, 0))
        
        # Draw the star
        star_radius = max(10, min(50, int(0.05 * scale)))  # Between 10-50 pixels
        pygame.draw.circle(screen, (255, 255, 0), (int(star_screen_x), int(star_screen_y)), star_radius)
        # Draw the planet
        planet_radius = max(4, min(20, int(0.02 * scale)))  # Between 4-20 pixels
        pygame.draw.circle(screen, (40, 122, 180), (int(planet_screen_x), int(planet_screen_y)), planet_radius)
        
        # Draw HUD
        fps_text = hud_font.render(f"FPS: {clock.get_fps():.0f}", True, (255, 255, 255))
        zoom_text = hud_font.render(f"Zoom: {scale:.2f}x", True, (255, 255, 255))
        sim_speed_text = hud_font.render(f"Sim Speed: {(speed_multiplier * 10):.1f}x", True, (255, 255, 255))
        elapsed_time_text = hud_font.render(f"Sim Time: {elapsed_time:.2f} years", True, (255, 255, 255))
        distance_text = hud_font.render(f"Distance: {distance:.2f} AU", True, (255, 255, 255))
        velocity_text = hud_font.render(f"Velocity: {velocity:.2f} AU/yr", True, (255, 255, 255))

        # Draw text on screen (right-aligned)
        screen_width = screen.get_width()
        screen.blit(fps_text, (screen_width - fps_text.get_width() - 10, 10))
        screen.blit(zoom_text, (screen_width - zoom_text.get_width() - 10, 35))
        screen.blit(sim_speed_text, (screen_width - sim_speed_text.get_width() - 10, 60))
        screen.blit(elapsed_time_text, (screen_width - elapsed_time_text.get_width() - 10, 85))
        screen.blit(distance_text, (screen_width - distance_text.get_width() - 10, 110))
        screen.blit(velocity_text, (screen_width - velocity_text.get_width() - 10, 135))

        pygame.display.flip()  # Update the display

    # Cleanup
    pygame.quit()