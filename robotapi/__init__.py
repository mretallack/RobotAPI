"""RobotAPI - Python package for controlling WiFi-connected robot cars."""

__version__ = "0.1.0"

from robotapi.controller import RobotController
from robotapi.exceptions import (
    RobotAPIError,
    RobotConnectionError,
    CommandError,
    ObstacleDetectedError,
)

__all__ = [
    "RobotController",
    "RobotAPIError",
    "RobotConnectionError",
    "CommandError",
    "ObstacleDetectedError",
]
