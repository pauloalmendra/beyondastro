# actuators.py
class BaseActuator:
    def __init__(self, name, max_torque):
        self.name = name
        self.max_torque = max_torque

    def apply_torque(self, satellite):
        raise NotImplementedError("This method should be implemented by subclasses")

class ReactionWheel(BaseActuator):
    def __init__(self, max_torque, axis):
        super().__init__("Reaction Wheel", max_torque)
        self.axis = axis
    
    def apply_torque(self, satellite, torque):
        # Apply torque to the satellite along the specific axis
        pass
