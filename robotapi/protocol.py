"""Protocol encoding/decoding for robot communication."""

import json
from typing import Dict, Any, Optional

# Command numbers
CMD_MOVEMENT = 3
CMD_OBSTACLE = 21
CMD_CAMERA = 106
CMD_STOP = 100

# Movement directions
DIR_LEFT = 1
DIR_RIGHT = 2
DIR_FORWARD = 3
DIR_BACKWARD = 4

# Camera directions
CAM_TILT_DOWN = 1
CAM_TILT_UP = 2
CAM_PAN_RIGHT = 3
CAM_PAN_LEFT = 4
CAM_CENTER = 5


def build_movement_cmd(direction: int, speed: int) -> Dict[str, Any]:
    """Build movement command.
    
    Args:
        direction: Movement direction (DIR_LEFT, DIR_RIGHT, DIR_FORWARD, DIR_BACKWARD)
        speed: Speed value (0-100)
        
    Returns:
        Command dictionary
    """
    return {"H": 22, "N": CMD_MOVEMENT, "D1": direction, "D2": speed}


def build_obstacle_cmd() -> Dict[str, Any]:
    """Build obstacle detection command.
    
    Returns:
        Command dictionary
    """
    return {"H": 22, "N": CMD_OBSTACLE, "D1": 1}


def build_camera_cmd(direction: int) -> Dict[str, Any]:
    """Build camera control command.
    
    Args:
        direction: Camera direction (CAM_TILT_DOWN, CAM_TILT_UP, CAM_PAN_RIGHT, 
                   CAM_PAN_LEFT, CAM_CENTER)
        
    Returns:
        Command dictionary
    """
    return {"H": 22, "N": CMD_CAMERA, "D1": direction}


def build_stop_cmd() -> Dict[str, Any]:
    """Build stop command.
    
    Returns:
        Command dictionary
    """
    return {"N": CMD_STOP}


def encode_command(cmd: Dict[str, Any]) -> bytes:
    """Encode command dictionary to JSON bytes.
    
    Args:
        cmd: Command dictionary
        
    Returns:
        JSON-encoded bytes
    """
    return json.dumps(cmd).encode("utf-8")


def parse_response(data: str) -> Optional[Dict[str, Any]]:
    """Parse JSON response from robot.
    
    Args:
        data: Response string
        
    Returns:
        Parsed dictionary or None if not valid JSON
    """
    data = data.strip()
    
    # Handle heartbeat
    if data == "{Heartbeat}":
        return {"type": "heartbeat"}
    
    # Handle obstacle detection responses
    if "true" in data.lower():
        return {"type": "obstacle", "detected": True}
    if "false" in data.lower():
        return {"type": "obstacle", "detected": False}
    
    # Try to parse as JSON
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return None
