import pygame
from simulation import Simulation
from body import Body
from main import create_simple_system, create_elliptical_orbit, create_escape_trajectory

# Initialize Pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Orbit Simulation Visualization")

# Create a clock to control frame rate
clock = pygame.time.Clock()
FPS = 280
paused = False

# Physics timing
physics_dt = 0.01  # Must match sim.dt
physics_accumulator = 0.0
speed_multiplier = 50.0  # Can be adjusted to speed up or slow down simulation
last_printed_speed = round(speed_multiplier)

# Create the physics simulation
bodies, G = create_elliptical_orbit()
sim = Simulation(bodies, G=G, dt=0.01)
planet = bodies[1]
star = bodies[0]

# Trail settings
trail = []
max_trail_length = 50

# Main loop
print("Controls: SPACE to pause/resume, UP/DOWN to adjust speed")
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
                pass

    # Adjust speed multiplier with up/down keys - allows for holding keys down
    keys = pygame.key.get_pressed()
    current_speed = round
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
    scale = 1.0  # pixels per unit distance
    
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
        pygame.draw.lines(screen, (255, 255, 255), False, trail, 3)
    
    # Draw the star
    pygame.draw.circle(screen, (255, 255, 0), (int(star_screen_x), int(star_screen_y)), 15)
    # Draw the planet
    pygame.draw.circle(screen, (255, 255, 255), (int(planet_screen_x), int(planet_screen_y)), 10)

    pygame.display.flip()  # Update the display

# Cleanup
pygame.quit()