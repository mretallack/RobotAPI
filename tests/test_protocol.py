"""Unit tests for protocol module."""

import json
import pytest
from robotapi import protocol


class TestCommandBuilders:
    """Test command building functions."""

    def test_build_movement_cmd(self):
        """Test movement command builder."""
        cmd = protocol.build_movement_cmd(protocol.DIR_FORWARD, 50)
        assert cmd == {"H": 22, "N": 3, "D1": 3, "D2": 50}

    def test_build_obstacle_cmd(self):
        """Test obstacle detection command builder."""
        cmd = protocol.build_obstacle_cmd()
        assert cmd == {"H": 22, "N": 21, "D1": 1}

    def test_build_camera_cmd(self):
        """Test camera control command builder."""
        cmd = protocol.build_camera_cmd(protocol.CAM_PAN_LEFT)
        assert cmd == {"H": 22, "N": 106, "D1": 4}

    def test_build_stop_cmd(self):
        """Test stop command builder."""
        cmd = protocol.build_stop_cmd()
        assert cmd == {"N": 100}


class TestCommandEncoding:
    """Test command encoding."""

    def test_encode_command(self):
        """Test encoding command to JSON bytes."""
        cmd = {"N": 100}
        encoded = protocol.encode_command(cmd)
        assert isinstance(encoded, bytes)
        assert json.loads(encoded.decode("utf-8")) == cmd


class TestResponseParsing:
    """Test response parsing."""

    def test_parse_heartbeat(self):
        """Test parsing heartbeat response."""
        result = protocol.parse_response("{Heartbeat}")
        assert result == {"type": "heartbeat"}

    def test_parse_obstacle_true(self):
        """Test parsing obstacle detected response."""
        result = protocol.parse_response("true")
        assert result == {"type": "obstacle", "detected": True}

    def test_parse_obstacle_false(self):
        """Test parsing no obstacle response."""
        result = protocol.parse_response("false")
        assert result == {"type": "obstacle", "detected": False}

    def test_parse_json(self):
        """Test parsing JSON response."""
        result = protocol.parse_response('{"status": "ok"}')
        assert result == {"status": "ok"}

    def test_parse_invalid(self):
        """Test parsing invalid response."""
        result = protocol.parse_response("invalid")
        assert result is None


class TestConstants:
    """Test protocol constants."""

    def test_command_constants(self):
        """Test command number constants."""
        assert protocol.CMD_MOVEMENT == 3
        assert protocol.CMD_OBSTACLE == 21
        assert protocol.CMD_CAMERA == 106
        assert protocol.CMD_STOP == 100

    def test_direction_constants(self):
        """Test direction constants."""
        assert protocol.DIR_LEFT == 1
        assert protocol.DIR_RIGHT == 2
        assert protocol.DIR_FORWARD == 3
        assert protocol.DIR_BACKWARD == 4

    def test_camera_constants(self):
        """Test camera direction constants."""
        assert protocol.CAM_TILT_DOWN == 1
        assert protocol.CAM_TILT_UP == 2
        assert protocol.CAM_PAN_RIGHT == 3
        assert protocol.CAM_PAN_LEFT == 4
        assert protocol.CAM_CENTER == 5
