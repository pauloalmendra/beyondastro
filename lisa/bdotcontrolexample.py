import numpy as np
from magnetometer import Magnetometer
from magnetorquer import Magnetorquer
from bdotcontrol import BDotController
from scipy.spatial.transform import Rotation as R

# Initialize the magnetometers (2 magnetometers for this example)
magnetometer1 = Magnetometer(
    name="Magnetometer 1",
    position=[0.5, 0, 0],
    orientation=R.from_euler('xyz', [0, 0, 0], degrees=True).as_quat(),
    bias=[0.1, 0.0, 0.0],
    noise_std=0.01
)
magnetometer2 = Magnetometer(
    name="Magnetometer 2",
    position=[-0.5, 0, 0],
    orientation=R.from_euler('xyz', [0, 0, 0], degrees=True).as_quat(),
    bias=[-0.05, 0.1, 0.0],
    noise_std=0.01
)

# Initialize the magnetorquers (3 magnetorquers in this example)
magnetorquer1 = Magnetorquer(
    name="Magnetorquer 1",
    position=[0, 0, 0],
    orientation=R.from_euler('xyz', [0, 0, 0], degrees=True).as_quat(),
    max_magnetic_moment=0.05
)
magnetorquer2 = Magnetorquer(
    name="Magnetorquer 2",
    position=[0, 0, 0],
    orientation=R.from_euler('xyz', [90, 0, 0], degrees=True).as_quat(),
    max_magnetic_moment=0.05
)
magnetorquer3 = Magnetorquer(
    name="Magnetorquer 3",
    position=[0, 0, 0],
    orientation=R.from_euler('xyz', [0, 90, 0], degrees=True).as_quat(),
    max_magnetic_moment=0.05
)

# Satellite parameters
inertia_tensor = [[10, 0, 0], [0, 15, 0], [0, 0, 12]]  # Inertia tensor in kg·m²
drag_coefficient = 2.2  # Example drag coefficient
cross_section_area = 1.0  # Example cross-sectional area in m²

# Initialize the B-Dot controller
controller = BDotController(
    magnetometers=[magnetometer1, magnetometer2],
    magnetorquers=[magnetorquer1, magnetorquer2, magnetorquer3],
    gain=0.1,  # Control gain
    inertia_tensor=inertia_tensor,
    drag_coefficient=drag_coefficient,
    cross_section_area=cross_section_area
)

# Simulation parameters
dt = 1.0  # Time step (in seconds)
simulation_steps = 10  # Number of simulation steps
angular_velocity = np.array([0.1, 0.1, 0.1])  # Initial angular velocity (rad/s)

# Simulate control
for step in range(simulation_steps):
    # Read the magnetic field
    magnetic_field = controller.read_magnetic_field()
    
    # Compute the B-dot (rate of change of magnetic field)
    b_dot = controller.compute_b_dot(magnetic_field, dt)
    
    # Apply the control law to generate torque
    applied_moments = controller.apply_control(b_dot)
    
    # Compute aerodynamic disturbance (assuming velocity and air density)
    velocity_vector = np.array([7500, 0, 0])  # Example velocity vector (m/s)
    air_density = 1e-9  # Example air density in kg/m³ (typical for low Earth orbit)
    aerodynamic_torque = controller.compute_aerodynamic_torque(velocity_vector, air_density)
    
    # Total applied torque (sum of control torque and aerodynamic torque)
    total_applied_torque = np.sum(applied_moments, axis=0) + aerodynamic_torque
    
    # Update the satellite's angular velocity based on applied torque
    angular_velocity = controller.update_angular_velocity(angular_velocity, total_applied_torque, dt)
    
    print(f"Step {step + 1}:")
    print(f"Magnetic field: {magnetic_field} μT")
    print(f"B-dot: {b_dot} μT/s")
    print(f"Applied magnetic moments: {applied_moments} Am²")
    print(f"Aerodynamic torque: {aerodynamic_torque} Nm")
    print(f"New angular velocity: {angular_velocity} rad/s\n")
