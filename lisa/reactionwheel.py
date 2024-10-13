import numpy as np

class ReactionWheel:
    def __init__(self, name, position, orientation, max_torque, noise_std=0.01, bias=0.0):
        """
        Initialize the reaction wheel with position, orientation, and error parameters.

        Parameters:
        - name (str): The name or ID of the reaction wheel.
        - position (list): The position of the wheel in the satellite's body frame [x, y, z] in meters.
        - orientation (list): The orientation of the wheel in quaternion form [q0, q1, q2, q3].
        - max_torque (float): The maximum torque the reaction wheel can provide (in Nm).
        - noise_std (float): Standard deviation of the Gaussian noise applied to the torque.
        - bias (float): Constant bias error added to the torque command.
        """
        self.name = name
        self.position = np.array(position)
        self.orientation = np.array(orientation)
        self.max_torque = max_torque
        self.noise_std = noise_std
        self.bias = bias

    def apply_torque(self, commanded_torque):
        """
        Apply the torque from the reaction wheel, including noise and bias.

        Parameters:
        - commanded_torque (float): The commanded torque (Nm).

        Returns:
        - Actual applied torque (in Nm) after applying noise and bias.
        """
        # Add noise and bias to the commanded torque
        actual_torque = commanded_torque + np.random.normal(0, self.noise_std) + self.bias
        
        # Limit the torque to the maximum torque of the wheel
        actual_torque = np.clip(actual_torque, -self.max_torque, self.max_torque)
        
        return actual_torque
