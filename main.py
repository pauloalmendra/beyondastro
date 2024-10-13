import numpy as np
from astropy.time import Time
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
from lisa.satellite import Satellite
from scipy.spatial.transform import Rotation as R
from sunsensor import SunSensor

# Define the initial time and orbit (Sun-synchronous orbit, 700 km altitude)
initial_epoch = Time.now()
orbit = Orbit.circular(Earth, alt=700 * u.km, inc=1.71 * u.rad, epoch=initial_epoch)

# Create satellite instance
mass = 500  # kg
satellite = Satellite(orbit=orbit, mass=mass)


# Sensor position in the satellite's body frame (0.5 meters along the x-axis)
sensor_position = [0.5, 0, 0]  # x = 0.5m

# Rotation of 20 degrees around the z-axis, converted to a quaternion
rotation_degrees = 20  # Rotate by 20 degrees around the z-axis
sensor_orientation = R.from_euler('z', rotation_degrees, degrees=True).as_quat()

# Create the Sun Sensor
sun_sensor = SunSensor(name="Sun Sensor", position=sensor_position, orientation=sensor_orientation)


# Create a list to store positions
positions = []

# Define time span (24 hours) and time step (10 minutes)
total_duration = 24 * 3600  # 24 hours in seconds
time_step = 10 * 60  # 10 minutes in seconds

# Propagate the orbit for 24 hours and store positions
current_time = initial_epoch
for _ in range(int(total_duration / time_step)):
    satellite.orbit = satellite.orbit.propagate(current_time)
    position = satellite.orbit.r.to(u.km).value  # Get the satellite's position
    current_time += time_step * u.s  # Update time by 10 minutes
    positions.append(position)

# Convert positions list to numpy array for easy plotting
positions = np.array(positions)
# print(positions)