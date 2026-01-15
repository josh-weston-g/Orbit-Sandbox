from .physics import circular_orbit_velocity
from .body import Body
import numpy as np
from .units import G_AU

def create_simple_system(planet_data):
    """Create a simple star-planet system with a circular orbit."""
    # Central star
    star = Body(
        mass=1.0,   # Solar masses
        position=[0, 0],  # At origin
        velocity=[0, 0]   # Stationary  
    )

    # Planet (Earth-like)
    # Distance: 1 AU (Earth's orbital radius)
    orbital_radius = planet_data['semi_major_axis']  # AU

    # Planet mass: Earth is about 3x10^-6 solar masses
    # (Earth mass = 5.972×10^24 kg, Solar mass = 1.989×10^30 kg)
    planet_mass = planet_data['mass']  # Solar masses
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

def create_elliptical_orbit(planet_data):
    """Create a system with an elliptical orbit (Earth at 70% circular velocity)."""
    # Central star
    star = Body(
        mass=1.0,   # Solar masses
        position=[0, 0],
        velocity=[0, 0]
    )

    # Planet (Earth-like, slower velocity for elliptical orbit)
    orbital_radius = planet_data['semi_major_axis']  # AU
    planet_mass = planet_data['mass']  # Solar masses (Earth)

    # Calculate circular orbit speed, then reduce to 70% to create ellipse
    circular_speed = circular_orbit_velocity(star.mass, orbital_radius, G_AU)
    orbital_speed = circular_speed * 0.7

    planet = Body(
        mass=planet_mass,
        position=[orbital_radius, 0],
        velocity=[0, orbital_speed]
    )

    return [star, planet], G_AU

def create_escape_trajectory(planet_data):
    """Create a system where the planet escapes to infinity (120% escape velocity)."""
    # Central star
    star = Body(
        mass=1.0,   # Solar masses
        position=[0, 0],
        velocity=[0, 0]
    )

    # Planet (Earth-like, at escape velocity)
    orbital_radius = planet_data['semi_major_axis']  # AU
    planet_mass = planet_data['mass']  # Solar masses (Earth)

    # Calculate escape velocity: v_escape = sqrt(2) * v_circular
    # Then exceed it by 20%
    circular_speed = circular_orbit_velocity(star.mass, orbital_radius, G_AU)
    escape_speed = circular_speed * np.sqrt(2)
    orbital_speed = escape_speed * 1.2  # 20% above escape velocity

    planet = Body(
        mass=planet_mass,
        position=[orbital_radius, 0],
        velocity=[0, orbital_speed]
    )

    return [star, planet], G_AU

def create_binary_stars(planet_data=None):
    """Create a binary star system with two equal-mass stars orbiting their common center of mass.
    
        param: planet_data: Ignored for this scenario.    
    """
    
    # Two stars of equal mass (1.0 solar mass each)
    star_mass = 1.0
    separation = 1.0
    position_offset = separation / 2.0
    
    # Correct formula for binary orbit:
    # v = sqrt(G * M / (2 * separation))
    orbital_speed = np.sqrt(G_AU * star_mass / (2 * separation))
    
    # Star 1: right side, moving upward
    star1 = Body(
        mass=star_mass,
        position=[position_offset, 0],
        velocity=[0, orbital_speed]
    )
    
    # Star 2: left side, moving downward (opposite velocity)
    star2 = Body(
        mass=star_mass,
        position=[-position_offset, 0],
        velocity=[0, -orbital_speed]
    )
    
    return [star1, star2], G_AU

def create_three_body(planet_data=None):
    """Create a simple three-body system - rotating equilateral triangle."""
    
    mass = 1.0
    radius = 1.0  # Distance from center to each body
    
    # Place bodies in equilateral triangle, rotating clockwise
    import numpy as np
    
    # 120 degree spacing
    angle1 = 0
    angle2 = 2 * np.pi / 3
    angle3 = 4 * np.pi / 3
    
    # Orbital speed for three equal masses in triangle
    # v = sqrt(G * M / (sqrt(3) * r))
    v = np.sqrt(G_AU * mass / (np.sqrt(3) * radius))
    
    body1 = Body(
        mass=mass,
        position=[radius * np.cos(angle1), radius * np.sin(angle1)],
        velocity=[-v * np.sin(angle1), v * np.cos(angle1)]
    )
    
    body2 = Body(
        mass=mass,
        position=[radius * np.cos(angle2), radius * np.sin(angle2)],
        velocity=[-v * np.sin(angle2), v * np.cos(angle2)]
    )
    
    body3 = Body(
        mass=mass,
        position=[radius * np.cos(angle3), radius * np.sin(angle3)],
        velocity=[-v * np.sin(angle3), v * np.cos(angle3)]
    )
    
    return [body1, body2, body3], G_AU

def create_solar_system(planet_data=None):
    """Create inner solar system (Sun + 4 inner planets)."""
    
    from .planets import PLANETS
    
    # Sun at origin, stationary
    sun = Body(mass=1.0, position=[0, 0], velocity=[0, 0])
    
    bodies = [sun]
    
    # Inner planets with circular orbits
    inner_planets = ['mercury', 'venus', 'earth', 'mars']
    
    for planet_name in inner_planets:
        planet_data = PLANETS[planet_name]
        a = planet_data['semi_major_axis']  # AU
        mass = planet_data['mass']  # Solar masses
        
        # Circular orbit velocity
        v = circular_orbit_velocity(1.0, a, G_AU)  # Orbit around Sun
        
        planet = Body(
            mass=mass,
            position=[a, 0],  # Start on x-axis
            velocity=[0, v]   # Velocity in +y direction
        )
        bodies.append(planet)
    
    return bodies, G_AU