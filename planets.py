# Real planet data (semi-major axis in AU, orbital period in years, mass in solar masses)
PLANETS = {
    'mercury': {
        'semi_major_axis': 0.387,
        'orbital_period': 0.241,
        'mass': 1.66e-7,  # ~0.055 Earth masses
        'color': (169, 169, 169)  # Gray
    },
    'venus': {
        'semi_major_axis': 0.723,
        'orbital_period': 0.615,
        'mass': 2.45e-6,  # ~0.815 Earth masses
        'color': (255, 198, 73)  # Yellowish
    },
    'earth': {
        'semi_major_axis': 1.0,
        'orbital_period': 1.0,
        'mass': 3.0e-6,
        'color': (100, 149, 237)  # Blue
    },
    'mars': {
        'semi_major_axis': 1.524,
        'orbital_period': 1.88,
        'mass': 3.23e-7,  # ~0.107 Earth masses
        'color': (188, 39, 50)  # Red
    },
    'jupiter': {
        'semi_major_axis': 5.203,
        'orbital_period': 11.86,
        'mass': 9.55e-4,  # ~318 Earth masses
        'color': (201, 153, 103)  # Orange-brown
    }
}