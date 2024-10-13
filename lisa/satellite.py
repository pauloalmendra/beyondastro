# satellite.py
import numpy as np
from poliastro.bodies import Earth
from poliastro.twobody import Orbit
from astropy import units as u
from astropy.time import Time
from scipy.spatial.transform import Rotation as R

class Satellite:
    def __init__(self, orbit: Orbit, mass: float, inertia_tensor=None, attitude=None, angular_velocity=None):
        """
        Initializes the Satellite object.

        Parameters:
        - orbit (poliastro.twobody.Orbit): The satellite's initial orbit.
        - mass: Mass of the satellite (kg).
        - inertia_tensor: 3x3 numpy array representing the inertia tensor (kg·m²).
        - attitude: Initial attitude quaternion [q0, q1, q2, q3].
        - angular_velocity: Initial angular velocity vector [ωx, ωy, ωz] in rad/s.
        """
        self.orbit = orbit
        self.mass = mass

        # Set the inertia tensor (diagonal by default)
        if inertia_tensor is None:
            self.inertia_tensor = np.diag([10.0, 10.0, 10.0])
        else:
            self.inertia_tensor = np.array(inertia_tensor)

        # Initial attitude quaternion
        if attitude is None:
            self.attitude = np.array([1.0, 0.0, 0.0, 0.0])  # Identity quaternion
        else:
            self.attitude = np.array(attitude)

        # Initial angular velocity
        if angular_velocity is None:
            self.angular_velocity = np.array([0.0, 0.0, 0.0])
        else:
            self.angular_velocity = np.array(angular_velocity)

        self.instruments = []

        # Total torque accumulated during a time step
        self.total_torque = np.array([0.0, 0.0, 0.0])

    def add_instrument(self, instrument):
        """Adds a sensor to the satellite."""
        self.instrument.append(instrument)

    def apply_torque(self, torque):
        """Accumulates torque to be applied during the time step."""
        self.total_torque += np.array(torque)

    def propagate_orbit(self, time_delta):
        """
        Propagates the satellite's orbit forward by a time delta.

        Parameters:
        - time_delta: The time to propagate the orbit forward (in seconds).
        """
        time_span = Time.now() + time_delta * u.s
        self.orbit = self.orbit.propagate(time_span)

    def get_position(self):
        """Returns the satellite's current position in the orbit frame (ECI)."""
        return self.orbit.r.to(u.km)

    def get_velocity(self):
        """Returns the satellite's current velocity in the orbit frame (ECI)."""
        return self.orbit.v.to(u.km / u.s)

    def step(self, dt):
        """
        Advances the satellite's state by a time step dt.
        - Updates orbit and attitude.
        """
        # Propagate orbit with poliastro
        self.propagate_orbit(dt)

        # Update rotational dynamics (attitude and angular velocity)
        angular_acceleration = np.linalg.inv(self.inertia_tensor) @ self.total_torque
        self.angular_velocity += angular_acceleration * dt

        self._update_attitude(dt)

        # Reset total torque
        self.total_torque = np.array([0.0, 0.0, 0.0])

    def _update_attitude(self, dt):
        """Updates the satellite's attitude quaternion based on angular velocity."""
        omega = self.angular_velocity
        omega_quat = np.concatenate([[0.0], omega])
        q = self.attitude
        q_dot = 0.5 * self._quaternion_multiply(q, omega_quat)
        self.attitude += q_dot * dt
        self.attitude = self.attitude / np.linalg.norm(self.attitude)

    @staticmethod
    def _quaternion_multiply(q1, q2):
        """Multiplies two quaternions."""
        w0, x0, y0, z0 = q1
        w1, x1, y1, z1 = q2
        return np.array([
            w0*w1 - x0*x1 - y0*y1 - z0*z1,
            w0*x1 + x0*w1 + y0*z1 - z0*y1,
            w0*y1 - x0*z1 + y0*w1 + z0*x1,
            w0*z1 + x0*y1 - y0*x1 + z0*w1
        ])
