import numpy as np
from body import Body
from simulation import Simulation
from physics import circular_orbit_velocity
import argparse

def create_simple_system():
    """Create a simple star-planet system with a circular orbit."""
    # Constants
    G = 1.0

    # Star at origin (stationary)
    star = Body(
        position=[0, 0],
        velocity=[0, 0],
        mass=1000
    )

    # Planet parameters
    orbital_radius = 100.0
    planet_mass = 1.0

    # Calculate orbital speed
    speed = circular_orbit_velocity(star.mass, orbital_radius, G)

    # Place planet on x-axis, moving in +y direction for circular orbit
    planet = Body(
        position=[orbital_radius, 0],
        velocity=[0, speed],
        mass=planet_mass
    )

    return [star, planet], G

def create_elliptical_orbit():
    """Create a system with an elliptical orbit."""
    # Constants
    G = 1.0

    # Star at origin (stationary)
    star = Body(
        position=[0, 0],
        velocity=[0, 0],
        mass=1000
    )

    # Planet parameters
    orbital_radius = 100.0
    planet_mass = 1.0

    # Calculate orbital speed and reduce it to create ellipse
    speed = circular_orbit_velocity(star.mass, orbital_radius, G) * 0.7

    # Place planet on x-axis, moving in +y direction
    planet = Body(
        position=[orbital_radius, 0],
        velocity=[0, speed],
        mass=planet_mass
    )

    return [star, planet], G

def create_escape_trajectory():
    """Create a system where the planet escapes to infinity."""
    # Constants
    G = 1.0

    # Star at origin (stationary)
    star = Body(
        position=[0, 0],
        velocity=[0, 0],
        mass=1000
    )

    # Planet parameters
    orbital_radius = 100.0
    planet_mass = 1.0

    # Calculate escape velocity and exceed it
    circular_speed = circular_orbit_velocity(star.mass, orbital_radius, G)
    escape_speed = circular_speed * np.sqrt(2)
    speed = escape_speed * 1.2  # 20% above escape velocity

    # Place planet on x-axis, moving in +y direction
    planet = Body(
        position=[orbital_radius, 0],
        velocity=[0, speed],
        mass=planet_mass
    )

    return [star, planet], G

def main():
    """Set up and run the simulation."""
    # Create the system (choose one):
    # bodies, G = create_simple_system()      # Circular orbit
    bodies, G = create_elliptical_orbit()   # Elliptical orbit
    # bodies, G = create_escape_trajectory()   # Escape trajectory
    
    # Simulation parameters
    dt = 0.01  # Time step
    
    # Create simulation
    sim = Simulation(bodies, G=G, dt=dt)
    
    # Print initial conditions
    print("="*50)
    print("Orbit Simulation - Simple Star-Planet System")
    print("="*50)
    print(f"\nStar:")
    print(f"  Mass: {bodies[0].mass}")
    print(f"  Position: {bodies[0].pos}")
    print(f"\nPlanet:")
    print(f"  Mass: {bodies[1].mass}")
    print(f"  Position: {bodies[1].pos}")
    print(f"  Velocity: {bodies[1].vel}")
    print(f"  Speed: {np.linalg.norm(bodies[1].vel):.4f}")
    print(f"\nSimulation Parameters:")
    print(f"  G: {G}")
    print(f"  dt: {dt}")
    print("\nPress Ctrl+C to stop the simulation\n")
    print("="*50)
    
    # Run the simulation
    sim.run_continuous()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orbit Simulation Sandbox. Run different orbital scenarios which conform to a correct Newtonian physics model.")
    parser.add_argument('--visualize', action='store_true', help='Run the visualization instead of console simulation.')
    args = parser.parse_args()
    if args.visualize:
        print("Visualization mode is not implemented in this script yet. Please run visualize.py separately.")
    else:
        main()