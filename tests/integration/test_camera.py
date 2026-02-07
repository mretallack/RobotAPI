"""Integration tests for camera control."""

import pytest
from robotapi import RobotController


class TestCameraIntegration:
    """Integration tests for camera commands."""

    def test_camera_pan_left(self, mock_robot_server):
        """Test camera pan left."""
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            robot.camera_pan_left(count=2)
            
            # Check camera commands were sent
            commands = [cmd for cmd in mock_robot_server.commands_received if cmd.get("N") == 106]
            assert len(commands) >= 2
            assert commands[0]["D1"] == 4  # Pan left
            
        finally:
            robot.disconnect()

    def test_camera_pan_right(self, mock_robot_server):
        """Test camera pan right."""
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            robot.camera_pan_right(count=2)
            
            commands = [cmd for cmd in mock_robot_server.commands_received if cmd.get("N") == 106]
            assert len(commands) >= 2
            assert commands[0]["D1"] == 3  # Pan right
            
        finally:
            robot.disconnect()

    def test_camera_center(self, mock_robot_server):
        """Test camera center."""
        robot = RobotController("127.0.0.1", 10100)
        robot.connect()
        
        try:
            robot.camera_center()
            
            commands = [cmd for cmd in mock_robot_server.commands_received if cmd.get("N") == 106]
            assert len(commands) >= 1
            assert commands[0]["D1"] == 5  # Center
            
        finally:
            robot.disconnect()
