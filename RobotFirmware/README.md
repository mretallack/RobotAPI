# Robot Firmware

This directory contains the original ELEGOO Smart Robot Car V4.0 firmware.

## Contents

- **ESP32_CameraServer_AP_20210107/** - ESP32-WROVER camera module firmware (WiFi bridge)
- **SmartRobotCarV4.0_V0_20210104/** - Arduino Mega robot controller firmware
- **PROTOCOL_ANALYSIS.md** - Complete protocol documentation

## WiFi Configuration

### Original Mode: Access Point (AP)

The original firmware creates a WiFi Access Point:

**File**: `ESP32_CameraServer_AP_20210107/CameraWebServer_AP.cpp`

```cpp
// Line 126-130
WiFi.mode(WIFI_AP);
WiFi.softAP(mac_default, password);
```

**Default Settings:**
- **SSID**: `ELEGOO-XXXX` (where XXXX is chip ID)
- **Password**: Empty string `""` (no password)
- **IP Address**: `192.168.4.1`
- **TCP Port**: `100` (robot control)
- **HTTP Port**: `80` (camera stream)

**Usage:**
1. Robot creates WiFi AP on boot
2. Connect your device to robot's WiFi
3. Access camera at `http://192.168.4.1`
4. Control via TCP socket on port 100

### Modified Mode: WiFi Client (Station)

To connect the robot to your existing WiFi network instead:

**Modify**: `ESP32_CameraServer_AP_20210107/CameraWebServer_AP.cpp`

Replace lines 126-130 with:

```cpp
// Connect to existing WiFi network
WiFi.mode(WIFI_STA);
WiFi.begin("YOUR_SSID", "YOUR_PASSWORD");

// Wait for connection
while (WiFi.status() != WL_CONNECTED) {
  delay(500);
  Serial.print(".");
}

Serial.println("");
Serial.println("WiFi connected");
Serial.print("IP address: ");
Serial.println(WiFi.localIP());
```

**Benefits:**
- Robot joins your home network
- Access from any device on network
- No need to switch WiFi networks
- Can control multiple robots

**Usage:**
1. Flash modified firmware
2. Robot connects to your WiFi on boot
3. Find robot's IP address (check serial output or router)
4. Access camera at `http://ROBOT_IP`
5. Control via TCP socket on `ROBOT_IP:100`

## Flashing Firmware

### ESP32-WROVER Camera Module

**Requirements:**
- Arduino IDE with ESP32 board support
- USB cable (USB-C or Micro-USB depending on module)

**Steps:**
1. Open `ESP32_CameraServer_AP_20210107.ino` in Arduino IDE
2. Select **Board**: "ESP32 Wrover Module"
3. Select **Port**: Your ESP32's COM port
4. Click **Upload**

**Libraries Required:**
- ESP32 Camera library (built-in)
- WiFi library (built-in)

### Arduino Mega Robot Controller

**Requirements:**
- Arduino IDE
- USB cable (USB-B)

**Steps:**
1. Open `SmartRobotCarV4.0_V0_20210104.ino` in Arduino IDE
2. Install required libraries (see `addLibrary/` folder):
   - FastLED
   - IRremote
   - NewPing
3. Select **Board**: "Arduino Mega 2560"
4. Select **Port**: Your Arduino's COM port
5. Click **Upload**

## Communication Flow

```
Python Client (RobotAPI)
    ↓ TCP Socket (port 100)
ESP32-WROVER (WiFi Bridge)
    ↓ Serial UART (9600 baud)
Arduino Mega (Robot Controller)
    ↓ Hardware Control
Motors, Servos, Sensors, LEDs
```

## Protocol

See `PROTOCOL_ANALYSIS.md` for complete command reference.

**Quick Reference:**
- Movement: `{"H": 22, "N": 3, "D1": direction, "D2": speed}`
- Obstacle: `{"H": 22, "N": 21, "D1": 1}`
- Camera: `{"H": 22, "N": 106, "D1": direction}`
- Stop: `{"N": 100}`

## Troubleshooting

### ESP32 Won't Flash
- Hold BOOT button while uploading
- Check USB cable supports data (not just power)
- Try lower upload speed (115200 instead of 921600)

### Robot Not Responding
- Check ESP32 ↔ Arduino serial connection (RX2/TX2)
- Verify baud rate is 9600
- Check power supply (batteries charged)

### WiFi Connection Issues (AP Mode)
- SSID format: `ELEGOO-XXXX` where XXXX is chip ID
- Default: No password (open network)
- IP is always `192.168.4.1`

### WiFi Connection Issues (Station Mode)
- Check SSID and password are correct
- Ensure 2.4GHz WiFi (ESP32 doesn't support 5GHz)
- Check serial monitor for IP address
- Router must allow client-to-client communication

## Original Source

ELEGOO Smart Robot Car Kit V4.0
- GitHub: https://github.com/elegooofficial/ELEGOO-Smart-Robot-Car-Kit-V4.0
- License: See original repository
