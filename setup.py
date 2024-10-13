# setup.py
from setuptools import setup, find_packages

setup(
    name='lisas',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'poliastro',
        'numpy',
        'astropy',
        # Add other dependencies here
    ],
)
