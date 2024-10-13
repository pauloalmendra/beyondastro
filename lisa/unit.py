import numpy as np
from scipy.spatial.transform import Rotation as R

class Unit:
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

    def read(self):
        """Simulates reading sensor data. To be implemented by subclasses."""
        raise NotImplementedError("This method should be implemented by subclasses")

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
