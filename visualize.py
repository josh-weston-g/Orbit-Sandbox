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

# Physics timing
physics_dt = 0.01  # Must match sim.dt
physics_accumulator = 0.0
speed_multiplier = 100.0  # Can be adjusted to speed up or slow down simulation

# Create the physics simulation
bodies, G = create_elliptical_orbit()
sim = Simulation(bodies, G=G, dt=0.01)
planet = bodies[1]
star = bodies[0]

# Trail settings
trail = []
max_trail_length = 50

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # How much real time passed since last frame?
    frame_time = clock.tick(FPS) / 1000.0  # milliseconds to seconds
    physics_accumulator += frame_time * speed_multiplier
    
    # Run enough physics steps to catch up
    steps_this_frame = 0
    while physics_accumulator >= physics_dt:
        sim.step()
        physics_accumulator -= physics_dt
        steps_this_frame += 1
    
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