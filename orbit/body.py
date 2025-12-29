import numpy as np

class Body:
    def __init__(self, position, velocity, mass):
        self.pos = np.array(position, dtype=float)   # [x, y]
        self.vel = np.array(velocity, dtype=float)   # [vx, vy]
        self.mass = float(mass)                      # scalar

    def apply_acceleration(self, acceleration, dt):
        """Update velocity based on acceleration and time step.
            Uses semi-implicit Euler integration.
            acceleration: np.array([ax, ay])
            dt: timestep (float)
        """
        self.vel += acceleration * dt

    def update_position(self, dt):
        """Update position based on current velocity and time step.
            Uses semi-implicit Euler integration.
            dt: timestep (float)
        """
        self.pos += self.vel * dt

    def __repr__(self):
        return f"Body(pos={self.pos}, vel={self.vel}, mass={self.mass})"