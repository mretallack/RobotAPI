# RobotAPI

Python package for controlling WiFi-connected robot cars via TCP socket communication.

## Overview

RobotAPI provides a clean Python interface for robot control, sensor monitoring, and camera operations. Extracted from the BlocklyRobot project, it offers a pip-installable package for programmatic robot interaction.

## Features

### Movement Control
- **Forward/Backward**: Move robot with configurable speed and duration
- **Rotate Left/Right**: Precise rotation control
- **Obstacle Detection**: Automatic stopping when obstacles detected within 20cm
- **Emergency Stop**: Immediate halt of all movement

### Camera Control
- **Pan**: Left/right camera positioning
- **Tilt**: Up/down camera angle adjustment
- **Center**: Reset camera to default position
- **Image Capture**: Retrieve camera frames

### Sensor Monitoring
- **Obstacle Detection**: Real-time distance sensing
- **Movement Status**: Check if robot is currently executing commands
- **Connection Status**: Monitor TCP connection health

## Installation

```bash
pip install robotapi
```

Or install from source:

```bash
git clone git@github.com:mretallack/RobotAPI.git
cd RobotAPI
pip install -e .
```

## Quick Start

```python
from robotapi import RobotController

# Connect to robot
robot = RobotController("10.0.0.57")

# Move forward for 2 seconds
robot.forward(duration=2.0, speed=50)

# Check for obstacles
if robot.detect_obstacle():
    print("Obstacle detected!")

# Pan camera left
robot.camera_pan_left(count=3)

# Get camera image
image = robot.get_image()

# Disconnect
robot.disconnect()
```

## API Reference

### RobotController

#### Connection
- `__init__(ip_address, port=100)` - Initialize robot connection
- `connect()` - Establish TCP connection
- `disconnect()` - Close connection
- `is_connected()` - Check connection status

#### Movement
- `forward(duration, speed=50)` - Move forward with obstacle detection
- `backward(duration, speed=50)` - Move backward
- `rotate_left(duration, speed=50)` - Rotate left
- `rotate_right(duration, speed=50)` - Rotate right
- `stop()` - Emergency stop

#### Sensors
- `detect_obstacle()` - Check for obstacles (returns bool)
- `get_distance()` - Get distance to nearest obstacle (cm)
- `is_moving()` - Check if robot is executing movement

#### Camera
- `camera_pan_left(count=1)` - Pan camera left
- `camera_pan_right(count=1)` - Pan camera right
- `camera_tilt_up(count=1)` - Tilt camera up
- `camera_tilt_down(count=1)` - Tilt camera down
- `camera_center()` - Reset camera to center
- `get_image()` - Capture and return image frame

## Protocol

Commands are sent as JSON over TCP port 100:

```json
{"H": 22, "N": 3, "D1": 3, "D2": 50}
```

- `H`: Header (22 for most commands)
- `N`: Command number
  - `3`: Movement
  - `21`: Obstacle detection
  - `106`: Camera control
  - `100`: Stop
- `D1`: Direction/parameter 1
- `D2`: Speed/parameter 2

### Movement Directions (N=3)
- `1`: Left
- `2`: Right
- `3`: Forward
- `4`: Backward

### Camera Directions (N=106)
- `1`: Tilt down
- `2`: Tilt up
- `3`: Pan right
- `4`: Pan left
- `5`: Center

## Requirements

- Python 3.7+
- Network connectivity to robot
- Robot must be listening on TCP port 100

## Architecture

```
RobotController
├── Connection Manager (TCP socket handling)
├── Command Queue (sequential execution)
├── Heartbeat Monitor (connection keepalive)
├── Movement Controller (motor commands)
├── Sensor Interface (obstacle detection)
└── Camera Controller (servo + image capture)
```

## Development

```bash
# Clone repository
git clone git@github.com:mretallack/RobotAPI.git
cd RobotAPI

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/

# Format code
black robotapi/
isort robotapi/
```

## Examples

See `examples/` directory for:
- Basic movement patterns
- Obstacle avoidance algorithms
- Camera scanning routines
- Sensor monitoring loops

## License

MIT License

## Contributing

Pull requests welcome. Please ensure:
- Code follows PEP 8 style guidelines
- Tests pass for all changes
- Documentation updated for new features

## Related Projects

- [BlocklyRobot](https://github.com/mretallack/BlocklyRobot) - Visual programming interface using this API
