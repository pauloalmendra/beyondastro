# control.py
class PDController:
    def __init__(self, kp, kd):
        self.kp = kp
        self.kd = kd

    def compute_torque(self, error, error_rate):
        return self.kp * error + self.kd * error_rate
