"""Integration tests for robot movement."""

import pytest
from robotapi import RobotController


class TestMovementIntegration:
    """Integration tests for movement commands."""

    def test_forward_movement(self, mock_robot_server):
        """Test forward movement with mock robot."""
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            result = robot.forward(duration=0.3, speed=50)
            assert result is True
            
            # Check commands were sent
            commands = [cmd for cmd in mock_robot_server.commands_received if cmd.get("N") == 3]
            assert len(commands) > 0
            assert commands[0]["D1"] == 3  # Forward direction
            
        finally:
            robot.disconnect()

    def test_backward_movement(self, mock_robot_server):
        """Test backward movement with mock robot."""
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            result = robot.backward(duration=0.3, speed=50)
            assert result is True
            
            commands = [cmd for cmd in mock_robot_server.commands_received if cmd.get("N") == 3]
            assert len(commands) > 0
            assert commands[0]["D1"] == 4  # Backward direction
            
        finally:
            robot.disconnect()

    def test_rotation_left(self, mock_robot_server):
        """Test left rotation with mock robot."""
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            result = robot.rotate_left(duration=0.3, speed=50)
            assert result is True
            
            commands = [cmd for cmd in mock_robot_server.commands_received if cmd.get("N") == 3]
            assert len(commands) > 0
            assert commands[0]["D1"] == 1  # Left direction
            
        finally:
            robot.disconnect()

    def test_rotation_right(self, mock_robot_server):
        """Test right rotation with mock robot."""
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            result = robot.rotate_right(duration=0.3, speed=50)
            assert result is True
            
            commands = [cmd for cmd in mock_robot_server.commands_received if cmd.get("N") == 3]
            assert len(commands) > 0
            assert commands[0]["D1"] == 2  # Right direction
            
        finally:
            robot.disconnect()

    def test_obstacle_detection(self, mock_robot_server):
        """Test obstacle detection during forward movement."""
        mock_robot_server.obstacle_detected = True
        
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            result = robot.forward(duration=0.5, speed=50)
            assert result is False  # Should stop due to obstacle
            
        finally:
            robot.disconnect()
