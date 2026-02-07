"""TCP connection management for robot communication."""

import socket
import time
from typing import Optional
from robotapi.exceptions import RobotConnectionError


class Connection:
    """Manages TCP socket connection to robot."""

    def __init__(self, ip: str, port: int = 100):
        """Initialize connection.
        
        Args:
            ip: Robot IP address
            port: TCP port (default 100)
        """
        self.ip = ip
        self.port = port
        self._socket: Optional[socket.socket] = None
        self._buffer = ""

    def connect(self) -> None:
        """Establish TCP connection to robot.
        
        Raises:
            RobotConnectionError: If connection fails
        """
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.connect((self.ip, self.port))
            self._socket.settimeout(0.1)
            self._buffer = ""
        except (socket.error, OSError) as e:
            self._socket = None
            raise RobotConnectionError(f"Failed to connect to {self.ip}:{self.port}: {e}")

    def disconnect(self) -> None:
        """Close TCP connection."""
        if self._socket:
            try:
                self._socket.close()
            except (socket.error, OSError):
                pass
            finally:
                self._socket = None
                self._buffer = ""

    def is_connected(self) -> bool:
        """Check if connection is active.
        
        Returns:
            True if connected, False otherwise
        """
        return self._socket is not None

    def send(self, data: bytes) -> None:
        """Send data to robot.
        
        Args:
            data: Bytes to send
            
        Raises:
            RobotConnectionError: If not connected or send fails
        """
        if not self._socket:
            raise RobotConnectionError("Not connected")

        try:
            self._socket.sendall(data)
        except (socket.error, OSError, BrokenPipeError, ConnectionResetError) as e:
            self.disconnect()
            raise RobotConnectionError(f"Send failed: {e}")

    def receive(self, timeout: float = 0.1) -> Optional[str]:
        """Receive data from robot with message buffering.
        
        Args:
            timeout: Receive timeout in seconds
            
        Returns:
            Complete message string or None if no complete message available
            
        Raises:
            RobotConnectionError: If not connected or receive fails
        """
        if not self._socket:
            raise RobotConnectionError("Not connected")

        try:
            self._socket.settimeout(timeout)
            data = self._socket.recv(1024)
            
            if not data:
                # Connection closed
                self.disconnect()
                raise RobotConnectionError("Connection closed by robot")
            
            # Add to buffer
            self._buffer += data.decode("utf-8")
            
            # Check for complete message (ends with })
            if "}" in self._buffer:
                end_pos = self._buffer.find("}")
                message = self._buffer[:end_pos + 1]
                self._buffer = self._buffer[end_pos + 1:]
                return message
            
            return None
            
        except socket.timeout:
            return None
        except (socket.error, OSError, ConnectionResetError, BrokenPipeError) as e:
            self.disconnect()
            raise RobotConnectionError(f"Receive failed: {e}")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.disconnect()
