"""Camera scanning example for RobotAPI.

Demonstrates camera control for scanning the environment.
"""

from robotapi import RobotController
import time

def main():
    """Run camera scanning routine."""
    robot = RobotController("10.0.0.57")
    robot.connect()
    
    try:
        print("Starting camera scan...")
        
        # Center camera first
        print("Centering camera...")
        robot.camera_center()
        time.sleep(0.5)
        
        # Pan left scan
        print("Scanning left...")
        for i in range(3):
            robot.camera_pan_left(count=1)
            print(f"  Position {i+1}/3")
            time.sleep(0.5)
        
        # Return to center
        print("Returning to center...")
        robot.camera_center()
        time.sleep(0.5)
        
        # Pan right scan
        print("Scanning right...")
        for i in range(3):
            robot.camera_pan_right(count=1)
            print(f"  Position {i+1}/3")
            time.sleep(0.5)
        
        # Return to center
        print("Returning to center...")
        robot.camera_center()
        
        # Tilt scan
        print("Scanning vertical...")
        robot.camera_tilt_up(count=2)
        time.sleep(0.5)
        robot.camera_tilt_down(count=2)
        time.sleep(0.5)
        robot.camera_center()
        
        print("\nCamera scan complete!")
        
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
