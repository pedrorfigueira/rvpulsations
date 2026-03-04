"""
rvpulsim
--------

Simulation of stellar pulsation effects on radial-velocity observations.

This package provides tools to:

- compute asteroseismic scaling relations
- simulate pulsation signals in RV time series
- estimate nightly RV scatter from p-mode oscillations
"""

from importlib.metadata import version

from .simulation import simulate_nightly_rv
from .scaling import asteroseismic_scaling


__version__ = version("rvpulsim")

__all__ = [
    "simulate_nightly_rv",
    "asteroseismic_scaling",
    "__version__",
]
