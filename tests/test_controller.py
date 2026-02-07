"""Unit tests for controller module."""

import pytest
from unittest.mock import Mock, patch, MagicMock
from robotapi.controller import RobotController, HeartbeatMonitor
from robotapi.exceptions import RobotConnectionError


class TestRobotControllerInit:
    """Test controller initialization."""

    def test_init(self):
        """Test controller initialization."""
        robot = RobotController("10.0.0.57", 100)
        assert robot.ip == "10.0.0.57"
        assert robot.port == 100
        assert not robot.is_connected()


class TestRobotControllerConnection:
    """Test connection management."""

    @patch("robotapi.controller.Connection")
    def test_connect(self, mock_conn_class):
        """Test connecting to robot."""
        mock_conn = Mock()
        mock_conn_class.return_value = mock_conn
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        mock_conn.connect.assert_called_once()

    @patch("robotapi.controller.Connection")
    def test_disconnect(self, mock_conn_class):
        """Test disconnecting from robot."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        mock_conn_class.return_value = mock_conn
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        robot.disconnect()
        
        mock_conn.disconnect.assert_called_once()


class TestRobotControllerMovement:
    """Test movement commands."""

    @patch("robotapi.controller.Connection")
    def test_forward_no_obstacle(self, mock_conn_class):
        """Test forward movement without obstacle."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        mock_conn.receive.return_value = None
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        result = robot.forward(0.2, 50)
        
        assert result is True
        assert mock_conn.send.called

    @patch("robotapi.controller.Connection")
    def test_backward(self, mock_conn_class):
        """Test backward movement."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        mock_conn.receive.return_value = None
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        result = robot.backward(0.2, 50)
        
        assert result is True
        assert mock_conn.send.called

    @patch("robotapi.controller.Connection")
    def test_rotate_left(self, mock_conn_class):
        """Test left rotation."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        mock_conn.receive.return_value = None
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        result = robot.rotate_left(0.2, 50)
        
        assert result is True
        assert mock_conn.send.called

    @patch("robotapi.controller.Connection")
    def test_rotate_right(self, mock_conn_class):
        """Test right rotation."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        mock_conn.receive.return_value = None
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        result = robot.rotate_right(0.2, 50)
        
        assert result is True
        assert mock_conn.send.called

    def test_movement_not_connected(self):
        """Test movement when not connected."""
        robot = RobotController("10.0.0.57")
        
        with pytest.raises(RobotConnectionError):
            robot.forward(1.0)


class TestRobotControllerCamera:
    """Test camera control."""

    @patch("robotapi.controller.Connection")
    def test_camera_pan_left(self, mock_conn_class):
        """Test camera pan left."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        robot.camera_pan_left(2)
        
        assert mock_conn.send.call_count >= 2

    @patch("robotapi.controller.Connection")
    def test_camera_pan_right(self, mock_conn_class):
        """Test camera pan right."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        robot.camera_pan_right(2)
        
        assert mock_conn.send.call_count >= 2

    @patch("robotapi.controller.Connection")
    def test_camera_center(self, mock_conn_class):
        """Test camera center."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        
        robot = RobotController("10.0.0.57")
        robot._connection = mock_conn
        robot.connect()
        
        robot.camera_center()
        
        assert mock_conn.send.called


class TestRobotControllerSensors:
    """Test sensor methods."""

    def test_detect_obstacle(self):
        """Test obstacle detection."""
        robot = RobotController("10.0.0.57")
        robot._obstacle_detected = True
        
        result = robot.detect_obstacle()
        
        assert result is True
        assert robot._obstacle_detected is False

    def test_is_moving(self):
        """Test movement status."""
        robot = RobotController("10.0.0.57")
        
        assert robot.is_moving() is False
        
        robot._moving = True
        assert robot.is_moving() is True


class TestRobotControllerContextManager:
    """Test context manager support."""

    @patch("robotapi.controller.Connection")
    def test_context_manager(self, mock_conn_class):
        """Test using controller as context manager."""
        mock_conn = Mock()
        mock_conn.is_connected.return_value = True
        mock_conn_class.return_value = mock_conn
        
        with RobotController("10.0.0.57") as robot:
            robot._connection = mock_conn
            assert robot is not None
        
        mock_conn.disconnect.assert_called()
