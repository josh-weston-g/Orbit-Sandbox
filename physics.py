import numpy as np
from body import Body

def compute_acceleration(body, source, G=1.0):
    """
    Compute gravitational acceleration on 'body' due to 'source'.
    
    Args:
        body: Body object being affected
        source: Body object causing the gravitational pull
        G: Gravitational constant (default 1.0 for scaled units)
    
    Returns:
        np.array([ax, ay]) - acceleration vector
    """

    # Vector from body to source - points from body to source
    r_vec = source.pos - body.pos
    
    # Calculate distance
    r = np.linalg.norm(r_vec)
    if r < 1e-10:
        return np.zeros(2)  # Avoid division by zero; no acceleration if too close
    
    # Calculate direction as a unit vector
    r_hat = r_vec / r
    
    # Gravitational acceleration magnitude
    a_magnitude = (G * source.mass) / (r**2)
    
    # Acceleration vector
    acceleration = a_magnitude * r_hat
    
    return acceleration

def circular_orbit_velocity(central_mass, radius, G=1.0):
    """
    Calculate the speed needed for a circular orbit around 'source' at a given 'radius'.

    param central_mass: Mass of the central body being orbited
    param radius: Distance from source to orbiting body
    param G: Gravitational constant (default 1.0 for scaled units)

    returns float - orbital speed

    Notes:
        Returns speed only; direction must be perpendicular to radius vector for circular orbit.
    """
    return np.sqrt(G * central_mass / radius)