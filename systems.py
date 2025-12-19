from physics import circular_orbit_velocity
from body import Body
import numpy as np

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