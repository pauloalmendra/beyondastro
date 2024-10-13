import numpy as np

class BDotController:
    def __init__(self, magnetometers, magnetorquers, gain):
        """
        Initialize the B-Dot controller.
        
        Parameters:
        - magnetometers (list): List of magnetometers.
        - magnetorquers (list): List of magnetorquers.
        - gain (float): Gain factor used in the control law.
        """
        self.magnetometers = magnetometers
        self.magnetorquers = magnetorquers
        self.gain = gain
        self.previous_magnetic_field = None

    def read_magnetic_field(self):
        """
        Read the magnetic field vector from the magnetometers and average the readings.
        
        Returns:
        - magnetic_field_avg (numpy array): Averaged magnetic field vector [Bx, By, Bz] in μT.
        """
        magnetic_fields = [mag.read([0, 0, 0]) for mag in self.magnetometers]  # Simulate zero field in the absence of actual readings
        magnetic_field_avg = np.mean(magnetic_fields, axis=0)
        return magnetic_field_avg

    def compute_b_dot(self, current_magnetic_field, dt):
        """
        Compute the B-dot (rate of change of magnetic field).
        
        Parameters:
        - current_magnetic_field (numpy array): The current magnetic field vector [Bx, By, Bz] in μT.
        - dt (float): The time step in seconds.
        
        Returns:
        - b_dot (numpy array): The rate of change of the magnetic field vector [dBx/dt, dBy/dt, dBz/dt] in μT/s.
        """
        if self.previous_magnetic_field is None:
            self.previous_magnetic_field = current_magnetic_field
            return np.zeros(3)  # No previous reading, return zero
        
        # Compute B-dot as the difference in magnetic field divided by the time step
        b_dot = (current_magnetic_field - self.previous_magnetic_field) / dt
        self.previous_magnetic_field = current_magnetic_field
        
        return b_dot

    def apply_control(self, b_dot):
        """
        Apply the B-dot control law using the magnetorquers.
        
        Parameters:
        - b_dot (numpy array): The B-dot vector [dBx/dt, dBy/dt, dBz/dt] in μT/s.
        
        Returns:
        - applied_moments (list): List of the actual applied magnetic moments for each magnetorquer.
        """
        # Desired magnetic moment is proportional to -B_dot
        desired_moment = -self.gain * b_dot
        
        # Apply the moment using each magnetorquer
        applied_moments = []
        for magnetorquer in self.magnetorquers:
            # Apply the magnetic moment to the magnetorquer
            applied_moment = magnetorquer.apply_magnetic_moment(desired_moment)
            applied_moments.append(applied_moment)
        
        return applied_moments
