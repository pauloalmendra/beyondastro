# sensors.py
import numpy as np

class BaseSensor:
    def __init__(self, name, noise_std=0.01):
        self.name = name
        self.noise_std = noise_std
    
    def read(self):
        raise NotImplementedError("This method should be implemented by subclasses")
    
    def add_noise(self, value):
        return value + np.random.normal(0, self.noise_std)

class SunSensor(BaseSensor):
    def __init__(self, noise_std=0.01):
        super().__init__("Sun Sensor", noise_std)
    
    def read(self, satellite_attitude):
        # Simulate sun direction based on attitude
        sun_direction = [1, 0, 0]  # Mock value
        return self.add_noise(sun_direction)
