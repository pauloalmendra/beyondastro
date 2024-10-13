import pytest
from sunsensor import BaseSensor, SunSensor
import numpy as np
from scipy.spatial.transform import Rotation as R


def test_sun_sensor_reading():
    sun_sensor = SunSensor(name="Sun Sensor", position=[0, 1, 0], orientation=[1, 0, 0, 0], noise_std=0.02)
    sun_direction = [1, 0, 0]  # Example sun direction vector in the body frame

    # Perform the read operation
    reading = sun_sensor.read(sun_direction)

    # Assert that the reading is a numpy array
    assert isinstance(reading, np.ndarray)
    # Assert that the reading is not exactly the same as the sun direction (noise added)
    assert not np.array_equal(reading, sun_direction)
