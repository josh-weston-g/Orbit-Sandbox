import numpy as np
from body import Body
from simulation import Simulation
from physics import circular_orbit_velocity

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

def create_decaying_orbit():
    """Create a system where the planet spirals into the star."""
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

    # Calculate orbital speed and reduce it for decay
    speed = circular_orbit_velocity(star.mass, orbital_radius, G) * np.sqrt(2)
    speed *= 1.2

    # Place planet on x-axis, moving in +y direction for decaying orbit
    planet = Body(
        position=[orbital_radius, 0],
        velocity=[0, speed],
        mass=planet_mass
    )

    return [star, planet], G

def main():
    """Set up and run the simulation."""
    # Create the system
    bodies, G = create_decaying_orbit()
    
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
    main()