# tests/test_satellite.py
import pytest
from lisa.satellite import Satellite
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
from astropy.time import Time

def test_satellite_orbit_propagation():
    
    # Initial orbit at 700 km altitude
    orbit = Orbit.circular(Earth, alt=700 * u.km)
    mass = 500  # kg

    satellite = Satellite(orbit=orbit, mass=mass)

    # Propagate the orbit for 60 seconds
    dt = 60  # seconds
    satellite.step(dt)

    # Check if the position and velocity have been updated
    new_position = satellite.get_position()
    new_velocity = satellite.get_velocity()

    assert new_position is not None
    assert new_velocity is not None
    assert len(new_position) == 3
    assert len(new_velocity) == 3
