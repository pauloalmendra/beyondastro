import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from astropy.time import Time
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
from lisa.satellite import Satellite

# Define the initial time and orbit (Sun-synchronous orbit, 700 km altitude)
initial_epoch = Time.now()
orbit = Orbit.circular(Earth, alt=700 * u.km, inc=1.71 * u.rad, epoch=initial_epoch)

# Create satellite instance
mass = 500  # kg
satellite = Satellite(orbit=orbit, mass=mass)

# Create a list to store positions
positions = []

# Define time span (24 hours) and time step (10 minutes)
total_duration = 24 * 3600  # 24 hours in seconds
time_step = 1 * 60  # 10 minutes in seconds

# Earth's angular velocity (radians per second)
earth_angular_velocity = 7.2921159e-5  # radians per second (~15 degrees per hour)

# Propagate the orbit for 24 hours and store positions
current_time = initial_epoch
for _ in range(int(total_duration / time_step)):
    satellite.orbit = satellite.orbit.propagate(current_time)
    position = satellite.orbit.r.to(u.km).value  # Get the satellite's position

    # Apply Earth's rotation to the satellite's position
    elapsed_time = (_ * time_step)  # Elapsed time in seconds
    rotation_angle = earth_angular_velocity * elapsed_time  # Rotation angle in radians

    # Rotation matrix around Earth's Z-axis
    rotation_matrix = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle), 0],
                                [np.sin(rotation_angle), np.cos(rotation_angle), 0],
                                [0, 0, 1]])
    
    # Rotate the satellite's position
    rotated_position = np.dot(rotation_matrix, position)
    positions.append(rotated_position)  # Append the rotated position
    current_time += time_step * u.s  # Update time by 10 minutes

# Convert positions list to numpy array for easy plotting
positions = np.array(positions)

# Create figure for the animation
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot satellite's orbit path (initially empty, will be animated)
orbit_line, = ax.plot([], [], [], color='r', label='Satellite Orbit')

# Labels and plot adjustments
ax.set_xlabel('X (km)')
ax.set_ylabel('Y (km)')
ax.set_zlabel('Z (km)')
ax.set_title('Satellite Orbiting Earth with Earth’s Rotation')

# Set plot limits for better view
ax.set_xlim([-1.5 * Earth.R.to(u.km).value, 1.5 * Earth.R.to(u.km).value])
ax.set_ylim([-1.5 * Earth.R.to(u.km).value, 1.5 * Earth.R.to(u.km).value])
ax.set_zlim([-1.5 * Earth.R.to(u.km).value, 1.5 * Earth.R.to(u.km).value])

# Plot Earth's surface as a sphere
earth_radius = Earth.R.to(u.km).value
u_vals = np.linspace(0, 2 * np.pi, 100)
v_vals = np.linspace(0, np.pi, 100)
x_earth = earth_radius * np.outer(np.cos(u_vals), np.sin(v_vals))
y_earth = earth_radius * np.outer(np.sin(u_vals), np.sin(v_vals))
z_earth = earth_radius * np.outer(np.ones(np.size(u_vals)), np.cos(v_vals))

# Initialize Earth surface plot
earth_surface = ax.plot_surface(x_earth, y_earth, z_earth, color='b', alpha=0.3)

# Animation function to update the satellite's orbit
def animate(i):
    # Update the satellite orbit path
    orbit_line.set_data(positions[:i, 0], positions[:i, 1])
    orbit_line.set_3d_properties(positions[:i, 2])
    
    return orbit_line,

# Create the animation using FuncAnimation
ani = FuncAnimation(fig, animate, frames=len(positions), interval=50, blit=False)

# Show the animated plot
plt.show()
