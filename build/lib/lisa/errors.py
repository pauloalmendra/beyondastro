# errors.py
import numpy as np

class ErrorModel:
    def __init__(self, bias=0.0, noise_std=0.01):
        self.bias = bias
        self.noise_std = noise_std

    def apply_error(self, true_value):
        noisy_value = true_value + self.bias + np.random.normal(0, self.noise_std)
        return noisy_value
