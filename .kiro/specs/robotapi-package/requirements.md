# Requirements: RobotAPI Python Package

## User Stories

### Package Installation

**WHEN** a user runs `pip install robotapi`  
**THE SYSTEM SHALL** install the package with all dependencies

**WHEN** a user imports `from robotapi import RobotController`  
**THE SYSTEM SHALL** provide access to the robot control interface

### Robot Connection

**WHEN** a user creates `RobotController("10.0.0.57")`  
**THE SYSTEM SHALL** establish TCP connection on port 100

**WHEN** the robot connection fails  
**THE SYSTEM SHALL** raise a ConnectionError with descriptive message

**WHEN** a user calls `disconnect()`  
**THE SYSTEM SHALL** close the TCP socket and cleanup resources

### Movement Control

**WHEN** a user calls `forward(duration=2.0, speed=50)`  
**THE SYSTEM SHALL** send movement command and monitor for obstacles

**WHEN** an obstacle is detected during forward movement  
**THE SYSTEM SHALL** stop immediately and return obstacle status

**WHEN** a user calls `backward(duration=2.0, speed=50)`  
**THE SYSTEM SHALL** move backward for specified duration without obstacle detection

**WHEN** a user calls `rotate_left(duration=1.0, speed=50)`  
**THE SYSTEM SHALL** rotate left for specified duration

**WHEN** a user calls `rotate_right(duration=1.0, speed=50)`  
**THE SYSTEM SHALL** rotate right for specified duration

**WHEN** a user calls `stop()`  
**THE SYSTEM SHALL** send emergency stop command immediately

### Obstacle Detection

**WHEN** a user calls `detect_obstacle()`  
**THE SYSTEM SHALL** query sensor and return True if obstacle within 20cm

**WHEN** a user calls `get_distance()`  
**THE SYSTEM SHALL** return distance to nearest obstacle in centimeters

### Camera Control

**WHEN** a user calls `camera_pan_left(count=3)`  
**THE SYSTEM SHALL** pan camera left 3 times with 100ms delay between movements

**WHEN** a user calls `camera_pan_right(count=3)`  
**THE SYSTEM SHALL** pan camera right 3 times with 100ms delay between movements

**WHEN** a user calls `camera_tilt_up(count=2)`  
**THE SYSTEM SHALL** tilt camera up 2 times

**WHEN** a user calls `camera_tilt_down(count=2)`  
**THE SYSTEM SHALL** tilt camera down 2 times

**WHEN** a user calls `camera_center()`  
**THE SYSTEM SHALL** reset camera to center position

**WHEN** a user calls `get_image()`  
**THE SYSTEM SHALL** capture and return current camera frame as image data

### Status Monitoring

**WHEN** a user calls `is_moving()`  
**THE SYSTEM SHALL** return True if robot is executing movement command

**WHEN** a user calls `is_connected()`  
**THE SYSTEM SHALL** return True if TCP connection is active

### Heartbeat Protocol

**WHEN** the robot sends `{Heartbeat}` message  
**THE SYSTEM SHALL** respond with `{Heartbeat}` to maintain connection

**WHEN** heartbeat response times out  
**THE SYSTEM SHALL** mark connection as lost and raise ConnectionError

### Error Handling

**WHEN** a command fails due to network error  
**THE SYSTEM SHALL** raise ConnectionError with error details

**WHEN** invalid parameters are provided  
**THE SYSTEM SHALL** raise ValueError with parameter requirements

**WHEN** a command is sent while disconnected  
**THE SYSTEM SHALL** raise ConnectionError indicating no active connection

## Acceptance Criteria

- Package installable via pip
- All movement commands execute correctly
- Obstacle detection prevents collisions
- Camera controls respond accurately
- Image capture returns valid image data
- Connection management handles errors gracefully
- Heartbeat maintains connection stability
- API matches documentation in README.md
