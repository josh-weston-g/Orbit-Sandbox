"""
Unit system for orbital mechanics.

We use astronommical units to keep numbers manageable:
- Distance: 1 AU (Astronomical Unit) = Earth-Sun distance
- Mass: 1 M☉ (Solar Mass) = Mass of the Sun
- Time: 1 year = Earth's orbital period

This keeps all numbers human-scale while keeping the physics correct.
"""

# Conversion factors to SI units
AU_IN_METERS = 1.496e11        # 1 AU in meters
SOLAR_MASS_IN_KG = 1.989e30    # 1 Solar Mass in kilograms
YEAR_TO_SECONDS = 3.154e7      # 1 year in seconds (365.25 days)

# SI value of G (gravitational constant)
G_SI = 6.67430e-11  # m³/(kg·s²)

# Calculate G in our unit system (AU³/(M☉·year²))
# Starting from: G_SI = 6.674e-11 m³/(kg·s²)
# We need: G_AU in AU³/(M☉·year²)
#
# The math:
# G_AU = G_SI * (1 M☉ / 1 kg) * (1 year / 1 second)² * (1 meter / 1 AU)³
#
# Breaking it down:
# - Multiply by M☉/kg to convert kg → M☉ in the denominator
# - Multiply by (year/second)² to convert s² → year² in the denominator  
# - Multiply by (meter/AU)³ to convert m³ → AU³ in the numerator

G_AU = G_SI * SOLAR_MASS_IN_KG * (YEAR_TO_SECONDS ** 2) / (AU_IN_METERS ** 3)

# === Conversion functions for display ===
# These convert from our internal units to SI units for display purposes.

def distance_to_km(distance_au):
    """
    Convert distance from AU to kilometers.

    :param distance_au: Distance in astronomical units (AU)
    :return: Distance in kilometers (km)
    Example: distance_to_km(1) -> 149,600,000 km
    """
    return distance_au * AU_IN_METERS / 1000.0 # meters to kilometers

def distance_to_au(distance_au):
    """
    Convert distance from AU to AU (identity function).
    
    This exists for consistency - sometimes we want to display in AU directly.

    :param distance_au: Distance in astronomical units (AU)
    :return: Distance in astronomical units (AU)
    Example: 1.0 AU -> 1.0 AU
    """
    return distance_au

def velocity_to_km_per_s(velocity_au_per_year):
    """
    Convert velocity from AU/year to kilometers/second.

    :param velocity_au_per_year: Velocity in AU per year
    :return: Velocity in kilometers per second (km/s)
    Example: Earth's orbital velocity ~6.28 AU/year -> ~29.78 km/s

    Math:
    - 1 AU/year = (1.496e11 meters) / (3.154e7 seconds) = ~4738 m/s = ~4.738 km/s
    """
    meters_per_second = velocity_au_per_year * AU_IN_METERS / YEAR_TO_SECONDS
    return meters_per_second / 1000.0  # Convert to km/s

def time_to_years(time_years):
    """
    Convert time from years to years (identity function).
    
    This exists for consistency - sometimes we want to display in years directly.

    :param time_years: Time in years
    :return: Time in years
    Example: 1.0 year -> 1.0 year
    """
    return time_years

def time_to_days(time_years):
    """
    Convert time from years to days.
    
    :param time_years: Time in years
    :return: Time in days
    Example: 1.0 year -> 365.25 days
    """
    return time_years * 365.25 # Average days in a year including leap years