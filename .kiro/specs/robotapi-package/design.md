# Design: RobotAPI Python Package

## Architecture Overview

```
robotapi/
├── __init__.py              # Package exports
├── controller.py            # RobotController main class
├── connection.py            # TCP connection management
├── protocol.py              # JSON protocol encoding/decoding
├── heartbeat.py             # Heartbeat monitoring thread
└── exceptions.py            # Custom exceptions
```

## Component Design

### RobotController (controller.py)

Main user-facing class providing high-level API.

**Responsibilities:**
- Initialize connection
- Expose movement methods
- Expose camera methods
- Expose sensor methods
- Manage connection lifecycle

**Key Methods:**
```python
class RobotController:
    def __init__(ip: str, port: int = 100)
    def connect() -> None
    def disconnect() -> None
    def is_connected() -> bool
    
    # Movement
    def forward(duration: float, speed: int = 50) -> bool
    def backward(duration: float, speed: int = 50) -> bool
    def rotate_left(duration: float, speed: int = 50) -> bool
    def rotate_right(duration: float, speed: int = 50) -> bool
    def stop() -> None
    
    # Sensors
    def detect_obstacle() -> bool
    def get_distance() -> float
    def is_moving() -> bool
    
    # Camera
    def camera_pan_left(count: int = 1) -> None
    def camera_pan_right(count: int = 1) -> None
    def camera_tilt_up(count: int = 1) -> None
    def camera_tilt_down(count: int = 1) -> None
    def camera_center() -> None
    def get_image() -> bytes
```

### Connection Manager (connection.py)

Handles TCP socket operations.

**Responsibilities:**
- Establish TCP connection
- Send/receive data
- Handle socket errors
- Manage socket lifecycle
- Buffer management for partial messages

**Key Methods:**
```python
class Connection:
    def __init__(ip: str, port: int)
    def connect() -> None
    def disconnect() -> None
    def send(data: bytes) -> None
    def receive(timeout: float = 0.1) -> str
    def is_connected() -> bool
```

### Protocol Handler (protocol.py)

Encodes/decodes robot command protocol.

**Responsibilities:**
- Build JSON command messages
- Parse JSON responses
- Define command constants

**Key Functions:**
```python
def build_movement_cmd(direction: int, speed: int) -> dict
def build_obstacle_cmd() -> dict
def build_camera_cmd(direction: int) -> dict
def build_stop_cmd() -> dict
def parse_response(data: str) -> dict
```

**Command Constants:**
```python
CMD_MOVEMENT = 3
CMD_OBSTACLE = 21
CMD_CAMERA = 106
CMD_STOP = 100

DIR_LEFT = 1
DIR_RIGHT = 2
DIR_FORWARD = 3
DIR_BACKWARD = 4

CAM_TILT_DOWN = 1
CAM_TILT_UP = 2
CAM_PAN_RIGHT = 3
CAM_PAN_LEFT = 4
CAM_CENTER = 5
```

### Heartbeat Monitor (heartbeat.py)

Background thread managing connection keepalive.

**Responsibilities:**
- Listen for `{Heartbeat}` messages
- Respond to heartbeats
- Detect connection loss
- Process obstacle detection responses during movement

**Key Methods:**
```python
class HeartbeatMonitor:
    def __init__(connection: Connection)
    def start() -> None
    def stop() -> None
    def wait_for_duration(duration: float, callback: Callable = None) -> bool
```

### Custom Exceptions (exceptions.py)

```python
class RobotAPIError(Exception):
    """Base exception"""

class ConnectionError(RobotAPIError):
    """Connection failures"""

class CommandError(RobotAPIError):
    """Command execution failures"""

class ObstacleDetectedError(RobotAPIError):
    """Obstacle detected during movement"""
```

## Sequence Diagrams

### Forward Movement with Obstacle Detection

```
User -> Controller: forward(2.0, 50)
Controller -> Connection: send(movement_cmd)
Controller -> Heartbeat: wait_for_duration(2.0, obstacle_check)
loop Every 100ms
    Robot -> Heartbeat: {Heartbeat}
    Heartbeat -> Connection: send({Heartbeat})
    Heartbeat -> Connection: send(obstacle_cmd)
    Robot -> Heartbeat: {"obstacle": false}
end
alt Obstacle Detected
    Robot -> Heartbeat: {"obstacle": true}
    Heartbeat -> Controller: return False
    Controller -> Connection: send(stop_cmd)
else Duration Complete
    Heartbeat -> Controller: return True
    Controller -> Connection: send(stop_cmd)
end
```

### Camera Pan with Image Capture

```
User -> Controller: camera_pan_left(3)
loop 3 times
    Controller -> Connection: send(camera_cmd)
    Controller: sleep(100ms)
end
User -> Controller: get_image()
Controller -> Connection: send(image_request_cmd)
Connection -> Robot: request
Robot -> Connection: image_data
Connection -> Controller: image_bytes
Controller -> User: return image_bytes
```

## Implementation Considerations

### Thread Safety
- Heartbeat runs in background thread
- Use threading.Lock for socket operations
- Queue commands if needed for sequential execution

### Error Recovery
- Retry connection on transient failures (max 3 attempts)
- Graceful degradation if heartbeat fails
- Clear error messages for user debugging

### Performance
- Non-blocking socket operations with timeout
- Efficient buffer management for message parsing
- Minimal overhead for heartbeat monitoring

### Testing Strategy
- **Unit tests**: Mock socket for isolated component testing
- **Integration tests**: Mock robot server simulating real protocol
- **Example-based tests**: Run examples against mock robot to verify real-world usage
- **Coverage target**: >90% code coverage
- **Test fixtures**: Reusable mock robot server in conftest.py
- **CI/CD**: All tests run on every commit

## Package Structure

```
robotapi/
├── setup.py                 # Package configuration
├── pyproject.toml          # Build system requirements
├── README.md               # Documentation
├── LICENSE                 # MIT License
├── .gitignore             # Git ignore patterns
├── robotapi/
│   ├── __init__.py
│   ├── controller.py
│   ├── connection.py
│   ├── protocol.py
│   ├── heartbeat.py
│   └── exceptions.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py             # Pytest fixtures (mock robot server)
│   ├── test_controller.py      # Unit tests
│   ├── test_connection.py      # Unit tests
│   ├── test_protocol.py        # Unit tests
│   ├── test_heartbeat.py       # Unit tests
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── test_movement.py    # Integration tests
│   │   ├── test_camera.py      # Integration tests
│   │   └── test_sensors.py     # Integration tests
│   └── examples/
│       ├── __init__.py
│       ├── test_basic_movement.py
│       ├── test_obstacle_avoidance.py
│       └── test_camera_scan.py
└── examples/
    ├── basic_movement.py
    ├── obstacle_avoidance.py
    └── camera_scan.py
```

## Dependencies

```
# setup.py dependencies
install_requires = []  # No external dependencies for core

# Development dependencies
dev_requires = [
    "pytest>=7.0",
    "pytest-cov>=4.0",      # Coverage reporting
    "pytest-asyncio>=0.21",  # Async test support
    "black>=22.0",
    "isort>=5.0",
    "mypy>=0.990"
]
```

## Test Infrastructure

### Mock Robot Server (conftest.py)

Pytest fixture providing simulated robot for testing:

```python
@pytest.fixture
def mock_robot_server():
    """Start mock TCP server simulating robot protocol"""
    server = MockRobotServer(port=10100)
    server.start()
    yield server
    server.stop()

class MockRobotServer:
    """Simulates robot TCP protocol for testing"""
    - Responds to heartbeats
    - Simulates obstacle detection
    - Tracks command history
    - Configurable responses
```

## Configuration

No configuration files needed - all parameters passed to constructor.

## Future Enhancements

- Async/await API support
- WebSocket alternative to TCP
- Video streaming support
- Sensor data logging
- Command replay/recording
