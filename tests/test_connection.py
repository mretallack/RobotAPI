"""Unit tests for connection module."""

import socket
import pytest
from unittest.mock import Mock, patch, MagicMock
from robotapi.connection import Connection
from robotapi.exceptions import RobotConnectionError


class TestConnectionInit:
    """Test connection initialization."""

    def test_init(self):
        """Test connection initialization."""
        conn = Connection("10.0.0.57", 100)
        assert conn.ip == "10.0.0.57"
        assert conn.port == 100
        assert not conn.is_connected()


class TestConnectionConnect:
    """Test connection establishment."""

    @patch("socket.socket")
    def test_connect_success(self, mock_socket_class):
        """Test successful connection."""
        mock_sock = Mock()
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        conn.connect()
        
        assert conn.is_connected()
        mock_sock.connect.assert_called_once_with(("10.0.0.57", 100))
        mock_sock.settimeout.assert_called_once_with(0.1)

    @patch("socket.socket")
    def test_connect_failure(self, mock_socket_class):
        """Test connection failure."""
        mock_sock = Mock()
        mock_sock.connect.side_effect = socket.error("Connection refused")
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        
        with pytest.raises(RobotConnectionError, match="Failed to connect"):
            conn.connect()
        
        assert not conn.is_connected()


class TestConnectionDisconnect:
    """Test connection closing."""

    @patch("socket.socket")
    def test_disconnect(self, mock_socket_class):
        """Test disconnection."""
        mock_sock = Mock()
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        conn.connect()
        conn.disconnect()
        
        assert not conn.is_connected()
        mock_sock.close.assert_called_once()

    def test_disconnect_when_not_connected(self):
        """Test disconnect when not connected."""
        conn = Connection("10.0.0.57")
        conn.disconnect()  # Should not raise
        assert not conn.is_connected()


class TestConnectionSend:
    """Test sending data."""

    @patch("socket.socket")
    def test_send_success(self, mock_socket_class):
        """Test successful send."""
        mock_sock = Mock()
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        conn.connect()
        conn.send(b"test data")
        
        mock_sock.sendall.assert_called_once_with(b"test data")

    def test_send_not_connected(self):
        """Test send when not connected."""
        conn = Connection("10.0.0.57")
        
        with pytest.raises(RobotConnectionError, match="Not connected"):
            conn.send(b"test")

    @patch("socket.socket")
    def test_send_failure(self, mock_socket_class):
        """Test send failure."""
        mock_sock = Mock()
        mock_sock.sendall.side_effect = socket.error("Send failed")
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        conn.connect()
        
        with pytest.raises(RobotConnectionError, match="Send failed"):
            conn.send(b"test")
        
        assert not conn.is_connected()


class TestConnectionReceive:
    """Test receiving data."""

    @patch("socket.socket")
    def test_receive_complete_message(self, mock_socket_class):
        """Test receiving complete message."""
        mock_sock = Mock()
        mock_sock.recv.return_value = b'{"status": "ok"}'
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        conn.connect()
        message = conn.receive()
        
        assert message == '{"status": "ok"}'

    @patch("socket.socket")
    def test_receive_partial_then_complete(self, mock_socket_class):
        """Test receiving partial then complete message."""
        mock_sock = Mock()
        mock_sock.recv.side_effect = [b'{"status":', b' "ok"}']
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        conn.connect()
        
        # First receive - partial
        message = conn.receive()
        assert message is None
        
        # Second receive - complete
        message = conn.receive()
        assert message == '{"status": "ok"}'

    @patch("socket.socket")
    def test_receive_timeout(self, mock_socket_class):
        """Test receive timeout."""
        mock_sock = Mock()
        mock_sock.recv.side_effect = socket.timeout()
        mock_socket_class.return_value = mock_sock
        
        conn = Connection("10.0.0.57")
        conn.connect()
        message = conn.receive()
        
        assert message is None

    def test_receive_not_connected(self):
        """Test receive when not connected."""
        conn = Connection("10.0.0.57")
        
        with pytest.raises(RobotConnectionError, match="Not connected"):
            conn.receive()


class TestConnectionContextManager:
    """Test context manager support."""

    @patch("socket.socket")
    def test_context_manager(self, mock_socket_class):
        """Test using connection as context manager."""
        mock_sock = Mock()
        mock_socket_class.return_value = mock_sock
        
        with Connection("10.0.0.57") as conn:
            assert conn.is_connected()
        
        mock_sock.close.assert_called_once()
