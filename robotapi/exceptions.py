"""Custom exceptions for robotapi."""


class RobotAPIError(Exception):
    """Base exception for all robotapi errors."""
    pass


class RobotConnectionError(RobotAPIError):
    """Connection-related errors."""
    pass


class CommandError(RobotAPIError):
    """Command execution errors."""
    pass


class ObstacleDetectedError(RobotAPIError):
    """Obstacle detected during movement."""
    pass
