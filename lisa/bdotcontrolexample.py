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

# Initialize the B-Dot controller with magnetometers and magnetorquers
controller = BDotController(
    magnetometers=[magnetometer1],
    magnetorquers=[magnetorquer1, magnetorquer2, magnetorquer3],
    gain=0.1  # Control gain
)

# Simulation parameters
dt = 1.0  # Time step (in seconds)
simulation_steps = 10  # Number of simulation steps

# Simulate control
for step in range(simulation_steps):
    # Read the magnetic field
    magnetic_field = controller.read_magnetic_field()
    
    # Compute the B-dot (rate of change of magnetic field)
    b_dot = controller.compute_b_dot(magnetic_field, dt)
    
    # Apply the control law to generate torque
    applied_moments = controller.apply_control(b_dot)
    
    print(f"Step {step + 1}:")
    print(f"Magnetic field: {magnetic_field} μT")
    print(f"B-dot: {b_dot} μT/s")
    print(f"Applied magnetic moments: {applied_moments} Am²\n")
