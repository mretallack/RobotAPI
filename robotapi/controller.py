"""Robot controller - main API interface."""

import time
import threading
from typing import Optional, Callable
from robotapi.connection import Connection
from robotapi.protocol import (
    build_movement_cmd,
    build_obstacle_cmd,
    build_camera_cmd,
    build_stop_cmd,
    encode_command,
    parse_response,
    DIR_FORWARD,
    DIR_BACKWARD,
    DIR_LEFT,
    DIR_RIGHT,
    CAM_PAN_LEFT,
    CAM_PAN_RIGHT,
    CAM_TILT_UP,
    CAM_TILT_DOWN,
    CAM_CENTER,
)
from robotapi.exceptions import RobotConnectionError, ObstacleDetectedError


class HeartbeatMonitor:
    """Monitors heartbeat and handles responses during operations."""

    def __init__(self, connection: Connection):
        """Initialize heartbeat monitor.
        
        Args:
            connection: Active connection to robot
        """
        self.connection = connection
        self._lock = threading.Lock()
        self._running = False

    def wait_for_duration(
        self, duration: float, callback: Optional[Callable[[dict], bool]] = None
    ) -> bool:
        """Wait for specified duration while handling heartbeats.
        
        Args:
            duration: Duration in seconds
            callback: Optional callback for processing responses.
                     Should return False to stop early, True to continue.
        
        Returns:
            True if duration completed, False if stopped early by callback
        """
        count = int(duration * 10)  # 100ms intervals
        
        for _ in range(count):
            try:
                with self._lock:
                    message = self.connection.receive(timeout=0.1)
                    
                    if message:
                        response = parse_response(message)
                        
                        if response and response.get("type") == "heartbeat":
                            # Respond to heartbeat
                            self.connection.send(b"{Heartbeat}")
                        
                        # Call callback if provided
                        if callback and response:
                            if not callback(response):
                                return False
                                
            except RobotConnectionError:
                raise
            
            time.sleep(0.1)
        
        return True


class RobotController:
    """Main robot control interface."""

    def __init__(self, ip: str, port: int = 100):
        """Initialize robot controller.
        
        Args:
            ip: Robot IP address
            port: TCP port (default 100)
        """
        self.ip = ip
        self.port = port
        self._connection = Connection(ip, port)
        self._heartbeat: Optional[HeartbeatMonitor] = None
        self._moving = False
        self._obstacle_detected = False

    def connect(self) -> None:
        """Establish connection to robot."""
        self._connection.connect()
        self._heartbeat = HeartbeatMonitor(self._connection)

    def disconnect(self) -> None:
        """Close connection to robot."""
        if self._moving:
            self.stop()
        self._connection.disconnect()
        self._heartbeat = None

    def is_connected(self) -> bool:
        """Check if connected to robot."""
        return self._connection.is_connected()

    def _send_command(self, cmd: dict) -> None:
        """Send command to robot."""
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        self._connection.send(encode_command(cmd))

    def stop(self) -> None:
        """Emergency stop - halt all movement."""
        if self.is_connected():
            self._send_command(build_stop_cmd())
            self._moving = False

    def forward(self, duration: float, speed: int = 50) -> bool:
        """Move forward with obstacle detection.
        
        Args:
            duration: Duration in seconds
            speed: Speed (0-100)
            
        Returns:
            True if completed, False if obstacle detected
            
        Raises:
            RobotConnectionError: If not connected
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        self._moving = True
        self._obstacle_detected = False
        
        # Start forward movement
        self._send_command(build_movement_cmd(DIR_FORWARD, speed))
        
        def check_obstacle(response: dict) -> bool:
            if response.get("type") == "heartbeat":
                # Check for obstacles on each heartbeat
                self._send_command(build_obstacle_cmd())
            elif response.get("type") == "obstacle":
                if response.get("detected"):
                    self._obstacle_detected = True
                    return False  # Stop early
            return True
        
        try:
            completed = self._heartbeat.wait_for_duration(duration, check_obstacle)
        finally:
            self.stop()
        
        return completed and not self._obstacle_detected

    def backward(self, duration: float, speed: int = 50) -> bool:
        """Move backward.
        
        Args:
            duration: Duration in seconds
            speed: Speed (0-100)
            
        Returns:
            True when completed
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        self._moving = True
        self._send_command(build_movement_cmd(DIR_BACKWARD, speed))
        
        try:
            self._heartbeat.wait_for_duration(duration)
        finally:
            self.stop()
        
        return True

    def rotate_left(self, duration: float, speed: int = 50) -> bool:
        """Rotate left.
        
        Args:
            duration: Duration in seconds
            speed: Speed (0-100)
            
        Returns:
            True when completed
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        self._moving = True
        self._send_command(build_movement_cmd(DIR_LEFT, speed))
        
        try:
            self._heartbeat.wait_for_duration(duration)
        finally:
            self.stop()
        
        return True

    def rotate_right(self, duration: float, speed: int = 50) -> bool:
        """Rotate right.
        
        Args:
            duration: Duration in seconds
            speed: Speed (0-100)
            
        Returns:
            True when completed
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        self._moving = True
        self._send_command(build_movement_cmd(DIR_RIGHT, speed))
        
        try:
            self._heartbeat.wait_for_duration(duration)
        finally:
            self.stop()
        
        return True

    def detect_obstacle(self) -> bool:
        """Check for obstacles.
        
        Returns:
            True if obstacle detected
        """
        result = self._obstacle_detected
        self._obstacle_detected = False
        return result

    def get_distance(self) -> float:
        """Get distance to nearest obstacle.
        
        Returns:
            Distance in cm (placeholder - not implemented in protocol)
        """
        # Not implemented in current robot protocol
        return 0.0

    def is_moving(self) -> bool:
        """Check if robot is currently moving.
        
        Returns:
            True if moving
        """
        return self._moving

    def camera_pan_left(self, count: int = 1) -> None:
        """Pan camera left.
        
        Args:
            count: Number of pan steps
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        for _ in range(count):
            self._send_command(build_camera_cmd(CAM_PAN_LEFT))
            time.sleep(0.1)

    def camera_pan_right(self, count: int = 1) -> None:
        """Pan camera right.
        
        Args:
            count: Number of pan steps
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        for _ in range(count):
            self._send_command(build_camera_cmd(CAM_PAN_RIGHT))
            time.sleep(0.1)

    def camera_tilt_up(self, count: int = 1) -> None:
        """Tilt camera up.
        
        Args:
            count: Number of tilt steps
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        for _ in range(count):
            self._send_command(build_camera_cmd(CAM_TILT_UP))
            time.sleep(0.1)

    def camera_tilt_down(self, count: int = 1) -> None:
        """Tilt camera down.
        
        Args:
            count: Number of tilt steps
        """
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        for _ in range(count):
            self._send_command(build_camera_cmd(CAM_TILT_DOWN))
            time.sleep(0.1)

    def camera_center(self) -> None:
        """Reset camera to center position."""
        if not self.is_connected():
            raise RobotConnectionError("Not connected")
        
        self._send_command(build_camera_cmd(CAM_CENTER))
        time.sleep(0.1)

    def get_image(self) -> bytes:
        """Capture camera image.
        
        Returns:
            Image data as bytes (placeholder - not implemented in protocol)
        """
        # Not implemented in current robot protocol
        return b""

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()

