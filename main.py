import numpy as np
from body import Body
from simulation import Simulation
from visualize import run_visualization
from systems import create_simple_system, create_elliptical_orbit, create_escape_trajectory
import argparse

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
        run_visualization()
    else:
        main()