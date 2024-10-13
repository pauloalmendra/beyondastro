import numpy as np
from scipy.spatial.transform import Rotation as R

class BaseActuator:
    def __init__(self, name: str, position: list, orientation: list, max_torque: float):
        self.name = name
        self.position = np.array(position)
        self.orientation = np.array(orientation)
        self.max_torque = max_torque

    def apply_torque(self, satellite):
        raise NotImplementedError("This method should be implemented by subclasses")

    def get_orientation_matrix(self):
        return R.from_quat(self.orientation).as_matrix()


class ReactionWheel(BaseActuator):
    def __init__(self, name: str, position: list, orientation: list, max_torque: float):
        super().__init__(name, position, orientation, max_torque)

    def apply_torque(self, satellite, commanded_torque):
        torque = np.clip(commanded_torque, -self.max_torque, self.max_torque)
        orientation_matrix = self.get_orientation_matrix()
        local_torque = np.array([torque, 0, 0])
        body_frame_torque = orientation_matrix @ local_torque
        satellite.apply_body_frame_torque(body_frame_torque)
        return body_frame_torque
    
