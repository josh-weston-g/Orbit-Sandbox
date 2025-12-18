import numpy as np
from body import Body
from physics import compute_acceleration

class Simulation:
    def __init__(self, bodies, G=1.0, dt=0.01):
        """
        Initialize the simulation.
        
        Args:
            bodies: list of Body objects
            G: gravitational constant
            dt: time step for integration
        """
        self.bodies = bodies
        self.G = G
        self.dt = dt
        self.time = 0.0 # Track simulation time

    def step(self):
        """Execute one simulation step."""
        # For now, assume first body is the source (star)
        # and all others orbit it
        source = self.bodies[0]
        
        for body in self.bodies[1:]:
            # Compute acceleration due to source
            acceleration = compute_acceleration(body, source, self.G)

            # Update velocity (semi-implicit Euler step 1)
            body.apply_acceleration(acceleration, self.dt)

            # Update position (semi-implicit Euler step 2)
            body.update_position(self.dt)
        
        # Advance time
        self.time += self.dt
    
    def run(self, num_steps):
        """Run the simulation for a given number of steps."""
        for _ in range(num_steps):
            self.step()
    
    def run_continuous(self, print_interval=1000):
        """Run the simulation continuously until interrupted.
        
            param print_interval: print position every N steps (0 = no printing)
        """
        try:
            step_count = 0
            while True:
                self.step()
                step_count += 1
                
                # Print progress periodically
                if print_interval > 0 and step_count % print_interval == 0:
                    planet = self.bodies[1]  # Assume second body is planet
                    distance = np.linalg.norm(planet.pos)
                    speed = np.linalg.norm(planet.vel)
                    print(f"t={self.time:8.2f} | pos=[{planet.pos[0]:7.2f}, {planet.pos[1]:7.2f}] | r={distance:6.2f} | v={speed:6.4f}")
        except KeyboardInterrupt:
            print(f"\n{'='*60}")
            print(f"Simulation stopped at t={self.time:.2f} ({step_count} steps)")
            print(f"{'='*60}")
    
    def get_positions(self):
        """Return current positions of all bodies."""
        return [body.pos.copy() for body in self.bodies]
    
    def get_state(self):
        """Return full state of all bodies."""
        return [(body.pos.copy(), body.vel.copy()) for body in self.bodies]