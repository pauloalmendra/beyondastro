import numpy as np
from scipy.spatial.transform import Rotation as R

class SunSensor():
    def __init__(self, name: str, position: list, orientation: list, noise_std: float = 0.01):
        """
        Base class for all units.

        Parameters:
        - name (str): A unique name or identifier for the unit.
        - position (list): The position of the unit in the satellite body frame [x, y, z].
        - orientation (list): The orientation of the unit as a quaternion [q0, q1, q2, q3].
        - noise_std (float): Standard deviation of the Gaussian noise.
        """
        self.name        = name
        self.position    = np.array(position)    # Position in body frame
        self.orientation = np.array(orientation) # Orientation in quaternion format
        self.noise_std   = noise_std

    def read(self, sun_direction):
        """
        Simulates reading the sun direction based on the satellite's orientation.
        Parameters:
        - sun_direction (list): The actual sun direction vector in the satellite's body frame.
        """
        # Transform sun direction from body frame to sensor frame
        sensor_rotation_matrix = self.get_orientation_matrix()
        sun_direction_sensor_frame = sensor_rotation_matrix.T @ np.array(sun_direction)

        # Add noise to the sensor reading
        noisy_sun_direction = self.add_noise(sun_direction_sensor_frame)
        
        return noisy_sun_direction

    def add_noise(self, value):
        """Adds Gaussian noise to the sensor reading."""
        return value + np.random.normal(0, self.noise_std)

    def get_orientation_matrix(self):
        """
        Converts the quaternion orientation into a rotation matrix.
        Returns:
        - rotation_matrix: 3x3 rotation matrix from body frame to sensor frame.
        """
        return R.from_quat(self.orientation).as_matrix()
