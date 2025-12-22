from physics import circular_orbit_velocity
from body import Body
import numpy as np
from units import G_AU

def create_simple_system():
    """Create a simple star-planet system with a circular orbit."""
    # Central star
    star = Body(
        mass=1.0,   # Solar masses
        position=[0, 0],  # At origin
        velocity=[0, 0]   # Stationary  
    )

    # Planet (Earth-like)
    # Distance: 1 AU (Earth's orbital radius)
    orbital_radius = 1.0  # AU

    # Planet mass: Earth is about 3x10^-6 solar masses
    # (Earth mass = 5.972×10^24 kg, Solar mass = 1.989×10^30 kg)
    planet_mass = 3.0e-6  # Solar masses

    # Calculate circular orbit velocity
    # For circular orbit: v = sqrt(G * M / r)
    # With G = 39.478 AU³/(M☉·year²), M = 1.0 M☉, r = 1.0 AU
    # v = sqrt(39.478 * 1.0 / 1.0) = sqrt(39.478) ≈ 6.283 AU/year
    # This equals 2π AU/year (one orbit circumference per year)
    orbital_speed = circular_orbit_velocity(star.mass, orbital_radius, G_AU)

    # Create planet at 1 AU on x-axis, moving in +y direction
    planet = Body(
        mass=planet_mass,   # 3.0e-6 Solar masses
        position=[orbital_radius, 0],  # 1 AU on x-axis
        velocity=[0, orbital_speed]     # Velocity in +y direction AU/year
    )

    return [star, planet], G_AU

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