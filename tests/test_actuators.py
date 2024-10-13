# tests/test_actuators.py
import pytest
from lisa.actuators import BaseActuator, ReactionWheel
import numpy as np

def test_base_actuator_init():
    actuator = BaseActuator(name="Test Actuator", position=[1, 0, 0], orientation=[1, 0, 0, 0], max_torque=0.5)
    assert actuator.name == "Test Actuator"
    assert np.array_equal(actuator.position, np.array([1, 0, 0]))
    assert np.array_equal(actuator.orientation, np.array([1, 0, 0, 0]))

def test_reaction_wheel_torque():
    reaction_wheel = ReactionWheel(name="Wheel 1", position=[0.5, 0.5, 0], orientation=[1, 0, 0, 0], max_torque=0.1)

    class MockSatellite:
        def __init__(self):
            self.total_torque = 0

        def apply_body_frame_torque(self, torque):
            self.total_torque += torque

    satellite = MockSatellite()

    torque_applied = reaction_wheel.apply_torque(satellite, commanded_torque=0.05)
    
    assert np.array_equal(torque_applied, np.array([0.05, 0, 0]))
    assert np.array_equal(satellite.total_torque, np.array([0.05, 0, 0]))

