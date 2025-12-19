import numpy as np
from body import Body
from simulation import Simulation
from visualize import run_visualization
from systems import create_simple_system, create_elliptical_orbit, create_escape_trajectory
import argparse

def main(scenario):
    """Set up and run the simulation."""
    # Map scenario string to factory functions
    scenario_map = {
        'circular': create_simple_system,
        'elliptical': create_elliptical_orbit,
        'escape': create_escape_trajectory
    }

    # Get factory function and create system
    factory = scenario_map[scenario]
    bodies, G = factory()
    
    # Simulation parameters
    dt = 0.01  # Time step
    
    # Create simulation
    sim = Simulation(bodies, G=G, dt=dt)
    
    # Print initial conditions
    print("="*50)
    print(f"Orbit Simulation - {scenario.title()} Orbit")
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
    input("Press Enter to start the simulation...")
    print("="*50)
    
    # Run the simulation
    sim.run_continuous()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Orbit Simulation Sandbox. Run different orbital scenarios which conform to a correct Newtonian physics model.")
    parser.add_argument('--scenario', type=str, choices=['circular', 'elliptical', 'escape'], help='Choose the orbital scenario: circular, elliptical, or escape.')
    parser.add_argument('--visualize', action='store_true', help='Run the visualization instead of console simulation.')
    args = parser.parse_args()
    if args.visualize:
        run_visualization(args.scenario)
    else:
        # Console mode: scenario is required
        if args.scenario is None:
            parser.error("the following arguments are required: --scenario when not using --visualize")
        main(args.scenario)