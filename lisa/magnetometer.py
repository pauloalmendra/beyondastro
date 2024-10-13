import numpy as np

class Magnetometer:
    def __init__(self, name, position, orientation, sensitivity=1.0, bias=None, noise_std=0.001):
        """
        Initialize the Magnetometer with position, orientation, and error parameters.

        Parameters:
        - name (str): The name or ID of the magnetometer.
        - position (list): Position of the magnetometer in the satellite body frame [x, y, z].
        - orientation (list): Orientation of the magnetometer in quaternion form [q0, q1, q2, q3].
        - sensitivity (float): Sensitivity or gain factor applied to the magnetic field reading.
        - bias (list): Constant bias vector [Bx, By, Bz] applied to the reading (in microteslas).
        - noise_std (float): Standard deviation of Gaussian noise added to the reading (in microteslas).
        """
        self.name = name
        self.position = np.array(position)
        self.orientation = np.array(orientation)
        self.sensitivity = sensitivity
        self.bias = np.array(bias) if bias is not None else np.zeros(3)
        self.noise_std = noise_std

    def read(self, magnetic_field_body_frame):
        """
        Simulate reading the magnetic field vector with errors.

        Parameters:
        - magnetic_field_body_frame (list): The true magnetic field vector in the satellite's body frame [Bx, By, Bz].

        Returns:
        - Noisy magnetic field vector in the sensor's local frame.
        """
        # Apply sensitivity (gain)
        measured_field = self.sensitivity * np.array(magnetic_field_body_frame)
        
        # Apply bias
        measured_field += self.bias
        
        # Add random Gaussian noise
        noisy_measured_field = measured_field + np.random.normal(0, self.noise_std, size=3)
        
        return noisy_measured_field
