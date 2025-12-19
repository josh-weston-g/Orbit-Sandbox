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
    scale = 1.0  # pixels per unit distance

    # Physics timing
    physics_dt = 0.01  # Must match sim.dt
    physics_accumulator = 0.0
    speed_multiplier = 50.0  # Can be adjusted to speed up or slow down simulation
    last_printed_speed = round(speed_multiplier)

    # Create the physics simulation
    sim = Simulation(bodies, G=G, dt=0.01)
    planet = bodies[1]
    star = bodies[0]

    # Trail settings
    trail = []
    max_trail_length = 50

    # Main loop
    print("Controls: SPACE to pause/resume, UP/DOWN to adjust speed, R to reset, ESC to return to menu")
    print(f"Initial speed multiplier: {last_printed_speed}x")
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
                    sim = Simulation(bodies, G=G, dt=0.01) # New simulation
                    planet = bodies[1]
                    star = bodies[0]
                    trail = [] # Clear trail
                    print("Simulation reset.")
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    run_visualization(None)  # Show menu again
                    return
                elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                    scale *= 1.1
                elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                    scale = max(1/5, scale / 1.1)  # Prevent too much zoom out - stops when planets get to min size
                
            # Mouse wheel for zooming
            if event.type == pygame.MOUSEWHEEL:
                # Zoom in/out
                if event.y > 0:
                    scale *= 1.1
                elif event.y < 0:
                    scale = max(1/5, scale / 1.1)  # Prevent too much zoom out - stops when planets get to min size

        # Adjust speed multiplier with up/down keys - allows for holding keys down
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            speed_multiplier += 0.1
            if round(speed_multiplier) != last_printed_speed:
                last_printed_speed = round(speed_multiplier)
                print(f"Speed multiplier: {last_printed_speed}x")
        elif keys[pygame.K_DOWN]:
            speed_multiplier = max(1.0, speed_multiplier - 0.1)
            if round(speed_multiplier) != last_printed_speed:
                last_printed_speed = round(speed_multiplier)
                print(f"Speed multiplier: {last_printed_speed}x")

        # How much real time passed since last frame?
        frame_time = clock.tick(FPS) / 1000.0  # milliseconds to seconds
        physics_accumulator += frame_time * speed_multiplier
        
        # Run enough physics steps to catch up
        if not paused:
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

        screen.fill((0, 0, 0))  # Clear screen with black
        
        # Add current position to trail
        trail.append((int(planet_screen_x), int(planet_screen_y)))
        if len(trail) > max_trail_length:
            trail.pop(0)  # Remove oldest point
        
        # Draw the trail
        if len(trail) > 1:
            # Create one surface for the entire trail
            trail_surface = pygame.Surface((800, 600), pygame.SRCALPHA)
            
            # Draw all segments on it
            for i in range(len(trail) - 1):
                alpha = int(255 * (i + 1) / len(trail))
                pygame.draw.line(trail_surface, (255, 255, 255, alpha), 
                                trail[i], trail[i + 1], 1)
            
            # Blit surface onto main screen
            screen.blit(trail_surface, (0, 0))
        
        # Draw the star
        pygame.draw.circle(screen, (255, 255, 0), (int(star_screen_x), int(star_screen_y)), max(3, int(15 * scale)))
        # Draw the planet
        pygame.draw.circle(screen, (255, 255, 255), (int(planet_screen_x), int(planet_screen_y)), max(1.2, int(6 * scale)))

        pygame.display.flip()  # Update the display

    # Cleanup
    pygame.quit()