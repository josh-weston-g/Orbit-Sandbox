import numpy as np

class Body:
    def __init__(self, position, velocity, mass, name=None, body_type="body"):
        self.pos = np.array(position, dtype=float)   # [x, y]
        self.vel = np.array(velocity, dtype=float)   # [vx, vy]
        self.acc = np.zeros(2, dtype=float)          # [ax, ay]
        self.mass = float(mass)                      # scalar

        # Body identification
        self.name = name if name is not None else "Unnamed"
        self.type = body_type

        # Temporary storage for Velocity Verlet integration
        self.old_acc = np.zeros(2, dtype=float) # Acceleration at start of time step
        self.new_acc = np.zeros(2, dtype=float) # Acceleration at end of time step

    def apply_acceleration(self, acceleration, dt):
        """Update velocity based on acceleration and time step.
        
        NOTE: This method is provided for alternative integration methods.
        The main simulation uses Velocity Verlet integration directly.
        
        Uses semi-implicit Euler integration.
            acceleration: np.array([ax, ay])
            dt: timestep (float)
        """
        self.vel += acceleration * dt

    def update_position(self, dt):
        """Update position based on current velocity and time step.
        
        NOTE: This method is provided for alternative integration methods.
        The main simulation uses Velocity Verlet integration directly.
        
        Uses semi-implicit Euler integration.
            dt: timestep (float)
        """
        self.pos += self.vel * dt

    def __repr__(self):
        return f"Body(pos={self.pos}, vel={self.vel}, mass={self.mass})"