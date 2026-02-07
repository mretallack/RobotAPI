"""Pytest fixtures for robotapi tests."""

import socket
import threading
import json
import time
import pytest


class MockRobotServer:
    """Mock TCP server simulating robot protocol."""

    def __init__(self, port=10100):
        """Initialize mock server.
        
        Args:
            port: TCP port to listen on
        """
        self.port = port
        self._socket = None
        self._thread = None
        self._running = False
        self._client_socket = None
        self.commands_received = []
        self.obstacle_detected = False

    def start(self):
        """Start mock server."""
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._socket.bind(("127.0.0.1", self.port))
        self._socket.listen(1)
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        time.sleep(0.1)  # Give server time to start

    def stop(self):
        """Stop mock server."""
        self._running = False
        if self._client_socket:
            try:
                self._client_socket.close()
            except:
                pass
        if self._socket:
            try:
                self._socket.close()
            except:
                pass
        if self._thread:
            self._thread.join(timeout=1.0)

    def _run(self):
        """Server main loop."""
        self._socket.settimeout(0.5)
        
        while self._running:
            try:
                client, addr = self._socket.accept()
                self._client_socket = client
                self._handle_client(client)
            except socket.timeout:
                continue
            except:
                break

    def _handle_client(self, client):
        """Handle client connection."""
        client.settimeout(0.1)
        buffer = ""
        
        while self._running:
            try:
                # Send heartbeat periodically
                time.sleep(0.05)
                client.sendall(b"{Heartbeat}")
                
                # Receive commands
                try:
                    data = client.recv(1024)
                    if not data:
                        break
                    
                    buffer += data.decode("utf-8")
                    
                    # Handle heartbeat response
                    if "{Heartbeat}" in buffer:
                        buffer = buffer.replace("{Heartbeat}", "")
                    
                    # Parse complete JSON messages
                    while "}" in buffer:
                        end_pos = buffer.find("}")
                        msg = buffer[:end_pos + 1]
                        buffer = buffer[end_pos + 1:]
                        
                        if msg.strip():
                            try:
                                cmd = json.loads(msg)
                                self.commands_received.append(cmd)
                                
                                # Respond to obstacle detection
                                if cmd.get("N") == 21:
                                    response = "true" if self.obstacle_detected else "false"
                                    client.sendall(response.encode("utf-8"))
                            except:
                                pass
                except socket.timeout:
                    pass
                            
            except:
                break


@pytest.fixture
def mock_robot_server():
    """Provide mock robot server for testing."""
    server = MockRobotServer(port=10100)
    server.start()
    yield server
    server.stop()
