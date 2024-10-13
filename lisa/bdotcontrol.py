import numpy as np

class BDotController:
    def __init__(self, magnetometers, magnetorquers, gain, inertia_tensor, drag_coefficient, cross_section_area):
        """
        Initialize the B-Dot controller with added inertia tensor and aerodynamic parameters.
        
        Parameters:
        - magnetometers (list): List of magnetometers.
        - magnetorquers (list): List of magnetorquers.
        - gain (float): Gain factor used in the control law.
        - inertia_tensor (numpy array): 3x3 matrix representing the satellite's inertia tensor (kg·m²).
        - drag_coefficient (float): Drag coefficient for aerodynamic torque modeling.
        - cross_section_area (float): Effective cross-sectional area of the satellite in m².
        """
        self.magnetometers = magnetometers
        self.magnetorquers = magnetorquers
        self.gain = gain
        self.inertia_tensor = np.array(inertia_tensor)
        self.previous_magnetic_field = None
        self.drag_coefficient = drag_coefficient
        self.cross_section_area = cross_section_area

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

    def compute_aerodynamic_torque(self, velocity_vector, air_density):
        """
        Compute the aerodynamic disturbance torque acting on the satellite.
        
        Parameters:
        - velocity_vector (numpy array): The satellite's velocity vector relative to the atmosphere [vx, vy, vz] in m/s.
        - air_density (float): The local atmospheric density in kg/m³.
        
        Returns:
        - aerodynamic_torque (numpy array): The aerodynamic torque vector [Tx, Ty, Tz] in Nm.
        """
        # Compute the drag force magnitude: F_drag = 0.5 * C_d * A * rho * v^2
        speed = np.linalg.norm(velocity_vector)
        drag_force_magnitude = 0.5 * self.drag_coefficient * self.cross_section_area * air_density * speed**2
        
        # Assume drag torque is proportional to drag force (acting perpendicular to velocity)
        drag_torque = drag_force_magnitude * np.cross(velocity_vector, [0, 0, 1])  # Torque axis is perpendicular to velocity
        
        return drag_torque

    def update_angular_velocity(self, angular_velocity, applied_torque, dt):
        """
        Update the satellite's angular velocity based on the applied torque and inertia tensor.
        
        Parameters:
        - angular_velocity (numpy array): The current angular velocity vector [wx, wy, wz] in rad/s.
        - applied_torque (numpy array): The applied torque vector [Tx, Ty, Tz] in Nm.
        - dt (float): The time step in seconds.
        
        Returns:
        - new_angular_velocity (numpy array): The updated angular velocity vector [wx, wy, wz].
        """
        # Compute the angular acceleration: alpha = I^(-1) * T
        angular_acceleration = np.linalg.inv(self.inertia_tensor) @ applied_torque
        
        # Update the angular velocity: w_new = w_old + alpha * dt
        new_angular_velocity = angular_velocity + angular_acceleration * dt
        
        return new_angular_velocity
