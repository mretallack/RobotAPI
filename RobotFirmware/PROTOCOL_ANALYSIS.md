# ELEGOO Smart Robot Car V4.0 - Protocol Analysis

## Overview

The ELEGOO Smart Robot Car V4.0 uses a JSON-based protocol over TCP (port 100) via an ESP32-WROVER camera module that acts as a WiFi bridge to the Arduino-based robot controller.

## Architecture

```
Client (Python/App) 
    ↓ TCP Socket (port 100)
ESP32-WROVER Camera Module (WiFi AP)
    ↓ Serial (UART)
Arduino Mega (Robot Controller)
    ↓ Hardware
Motors, Servos, Sensors, LEDs
```

## Available Sensors

### 1. Ultrasonic Distance Sensor
- **Command**: `{"H": 22, "N": 21, "D1": 1}`
- **Response**: `"true"` (obstacle < 20cm) or `"false"` (clear)
- **Purpose**: Obstacle detection

### 2. IR Line Tracking Sensors (3x ITR20001)
- **Command**: `{"H": 22, "N": 22, "D1": 1}`
- **Response**: JSON with sensor states
- **Purpose**: Line following

### 3. Ground Detection (Wheel Encoders)
- **Command**: `{"H": 22, "N": 23}`
- **Response**: `"true"` (on ground) or `"false"` (lifted)
- **Purpose**: Detect if robot is lifted off ground

### 4. MPU6050 IMU (Gyroscope + Accelerometer)
- **Hardware**: MPU6050 6-axis sensor
- **Purpose**: Balance, orientation, motion detection
- **Note**: Not exposed via TCP protocol (internal use only)

### 5. Voltage Sensor
- **Hardware**: Battery voltage monitoring
- **Purpose**: Low battery detection
- **Note**: Not exposed via TCP protocol

### 6. IR Remote Receiver
- **Hardware**: IR receiver for remote control
- **Purpose**: Remote control input
- **Note**: Not exposed via TCP protocol

## Complete Command Protocol

### Motor Control

#### N=1: Individual Motor Control
```json
{"H": 22, "N": 1, "D1": motor_id, "D2": speed, "D3": direction}
```
- `D1`: Motor selection (1=left, 2=right)
- `D2`: Speed (0-255)
- `D3`: Direction (1=forward, 2=backward)

#### N=2: Car Direction Control (Timed)
```json
{"H": 22, "N": 2, "D1": direction, "D2": speed, "T": time_ms}
```
- `D1`: Direction (1-9, see below)
- `D2`: Speed (0-255)
- `T`: Duration in milliseconds

#### N=3: Car Direction Control (Continuous)
```json
{"H": 22, "N": 3, "D1": direction, "D2": speed}
```
- `D1`: Direction codes:
  - 1 = Forward
  - 2 = Backward
  - 3 = Left
  - 4 = Right
  - 5 = Left Forward
  - 6 = Left Backward
  - 7 = Right Forward
  - 8 = Right Backward
  - 9 = Stop

#### N=4: Motor Speed Control (Both Motors)
```json
{"H": 22, "N": 4, "D1": left_speed, "D2": right_speed}
```
- `D1`: Left motor speed (0-255)
- `D2`: Right motor speed (0-255)

### Servo Control

#### N=5: Servo Position Control
```json
{"H": 22, "N": 5, "D1": servo_id, "D2": angle}
```
- `D1`: Servo ID (1-4)
- `D2`: Angle (0-180 degrees)

#### N=106: Camera Servo Quick Control
```json
{"H": 22, "N": 106, "D1": direction}
```
- `D1`: Direction:
  - 1 = Tilt down
  - 2 = Tilt up
  - 3 = Pan right
  - 4 = Pan left
  - 5 = Center

### LED Control

#### N=7: LED Control (Timed)
```json
{"H": 22, "N": 7, "D1": led_id, "D2": red, "D3": green, "D4": blue, "T": time_ms}
```
- `D1`: LED position (1=left, 2=front, 3=right, 4=back, 5=center)
- `D2`: Red value (0-255)
- `D3`: Green value (0-255)
- `D4`: Blue value (0-255)
- `T`: Duration in milliseconds

#### N=8: LED Control (Continuous)
```json
{"H": 22, "N": 8, "D1": led_id, "D2": red, "D3": green, "D4": blue}
```
- Same parameters as N=7 but without time limit

#### N=105: LED Brightness Control
```json
{"H": 22, "N": 105, "D1": direction}
```
- `D1`: 1=increase brightness, 2=decrease brightness

### Sensor Queries

#### N=21: Ultrasonic Distance Check
```json
{"H": 22, "N": 21, "D1": 1}
```
- **Response**: `"true"` or `"false"`

#### N=22: Line Tracking Sensor Status
```json
{"H": 22, "N": 22, "D1": 1}
```
- **Response**: JSON with sensor states

#### N=23: Ground Detection
```json
{"H": 22, "N": 23}
```
- **Response**: `"true"` (on ground) or `"false"` (lifted)

### Mode Control

#### N=100: Stop All / Standby Mode
```json
{"N": 100}
```
- Stops all motors and enters standby mode

#### N=101: Autonomous Mode Selection
```json
{"H": 22, "N": 101, "D1": mode}
```
- `D1`: Mode:
  - 1 = Line tracking mode
  - 2 = Obstacle avoidance mode
  - 3 = Follow mode

#### N=102: Joystick Control Mode
```json
{"H": 22, "N": 102, "D1": direction}
```
- `D1`: Direction (1-9, same as N=3)

#### N=110: Programming Mode
```json
{"H": 22, "N": 110}
```
- Enters programming mode

## Heartbeat Protocol

- **Server → Client**: `{Heartbeat}` (every 1 second)
- **Client → Server**: `{Heartbeat}` (response)
- **Timeout**: 3 missed heartbeats = disconnect

## Camera Streaming

The ESP32-WROVER module provides a web interface for camera streaming:
- **URL**: `http://192.168.4.1/` (when connected to robot's WiFi AP)
- **Stream**: MJPEG video stream
- **Control**: Web interface for camera settings

## Hardware Components

### Sensors
- **Ultrasonic**: HC-SR04 (distance measurement)
- **IR Line Tracking**: 3x ITR20001 sensors
- **IMU**: MPU6050 (gyro + accelerometer)
- **Voltage**: Battery voltage monitor
- **IR Receiver**: Remote control input

### Actuators
- **Motors**: 2x DC motors with encoders
- **Servos**: 4x servos (typically 1 for camera pan/tilt)
- **LEDs**: RGB LEDs (FastLED library)

### Communication
- **ESP32-WROVER**: WiFi AP + Camera
- **Arduino Mega**: Main controller
- **Serial**: ESP32 ↔ Arduino (9600 baud)

## Missing from Current RobotAPI Implementation

1. **Line tracking sensors** (N=22)
2. **Ground detection** (N=23)
3. **LED control** (N=7, N=8, N=105)
4. **Individual motor control** (N=1, N=4)
5. **Servo control** (N=5)
6. **Autonomous modes** (N=101)
7. **Joystick mode** (N=102)
8. **Camera image capture** (ESP32 web interface only)
9. **Timed movements** (N=2)

## Recommendations for RobotAPI Enhancement

### High Priority
1. Add line tracking sensor API
2. Add ground detection API
3. Add LED control API
4. Add individual motor control
5. Add timed movement support

### Medium Priority
6. Add servo control for all 4 servos
7. Add autonomous mode switching
8. Add camera image capture via HTTP

### Low Priority
9. Add IMU data reading (requires protocol extension)
10. Add voltage monitoring (requires protocol extension)
11. Add IR remote passthrough
