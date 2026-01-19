import numpy as np
from .body import Body
from .physics import compute_acceleration

class Simulation:
    def __init__(self, bodies, G=1.0, dt=0.001):
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

        # History tracking for rewind
        self.history = [] # List of (positions, velocities, accelerations)
        self.max_history = 1000 # Store up to 1000 snapshots

    def _compute_total_acceleration(self, body):
        """
        Calculate total gravitational acceleration on a body from all other bodies.

        param: body: Body object to compute acceleration for

        returns: np.array([ax, ay]) total acceleration vector
        """
        total_acc = np.zeros(2, dtype=float)
        
        for other in self.bodies:
            if other is not body: # Skip self
                total_acc += compute_acceleration(body, other, self.G)

        return total_acc
    
    def save_state(self):
        """Save current state of all bodies to history."""
        snapshot = []
        for body in self.bodies:
            snapshot.append({
                'pos': body.pos.copy(),
                'vel': body.vel.copy(),
                'acc': body.acc.copy()
            })
        self.history.append(snapshot)

        # Limit history size
        if len(self.history) > self.max_history:
            self.history.pop(0) # Remove oldest snapshot

    def step(self):
        """Execute one simulation step using N-body Velocity Verlet integration."""

        # Phase 1: Calculate old accelerations for all bodies
        for body in self.bodies:
            body.old_acc = self._compute_total_acceleration(body)

        # Phase 2: Update all positions using old accelerations
        for body in self.bodies:
            body.pos += body.vel * self.dt + 0.5 * body.old_acc * (self.dt**2)

        # Phase 3: Calculate new accelerations for all bodies at updated positions
        for body in self.bodies:
            body.new_acc = self._compute_total_acceleration(body)

        # Phase 4: Update all velocities using average of old and new accelerations
        for body in self.bodies:
            body.vel += 0.5 * (body.old_acc + body.new_acc) * self.dt
            body.acc = body.new_acc  # Store current acceleration for visualization or other uses
        
        # Advance time
        self.time += self.dt

        # Save stat
        self.save_state()

    def rewind_one_step(self):
        """Rewind the simulation by one saved state."""
        if len(self.history) > 0:
            snapshot = self.history.pop()   # Get and remove last snapshot
            # Restore all bodies to that state
            for i, body in enumerate(self.bodies):
                body.pos = snapshot[i]['pos']
                body.vel = snapshot[i]['vel']
                body.acc = snapshot[i]['acc']

            # Decrease sim time
            self.time -= self.dt

            return True # Successfully rewound
        return False # No history to rewind
    
    def run(self, num_steps):
        """Run the simulation for a given number of steps."""
        for i in range(num_steps):
            self.step()
            
            # Print state every step
            planet = self.bodies[1]  # Assume second body is planet
            distance = np.linalg.norm(planet.pos)
            speed = np.linalg.norm(planet.vel)
            print(f"t={self.time:8.2f} | pos=[{planet.pos[0]:7.2f},{planet.pos[1]:7.2f}] | r={distance:6.2f} | v={speed:.4f}")
    
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

    def run_and_log(self, num_steps, log_interval=10, filename="orbit_data.csv"):
        """Run the simulation and log positions at specified intervals.
        
            param num_steps: total number of steps to run
            param log_interval: log positions every N steps
            returns: list of logged positions
        """
        with open(filename, 'w') as f:
            f.write("time,x,y,vx,vy,distance,speed\n")

            for i in range(num_steps):
                self.step()
                
                if i % log_interval == 0:
                    planet = self.bodies[1]  # Assume second body is planet
                    distance = np.linalg.norm(planet.pos)
                    speed = np.linalg.norm(planet.vel)
                    f.write(f"{self.time},{planet.pos[0]},{planet.pos[1]},{planet.vel[0]},{planet.vel[1]},{distance},{speed}\n")

        print(f"\nLogged {num_steps//log_interval} data points to '{filename}'")
    
    def get_positions(self):
        """Return current positions of all bodies."""
        return [body.pos.copy() for body in self.bodies]
    
    def get_state(self):
        """Return full state of all bodies."""
        return [(body.pos.copy(), body.vel.copy()) for body in self.bodies]