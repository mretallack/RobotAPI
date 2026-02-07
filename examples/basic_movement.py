"""Basic movement example for RobotAPI.

Demonstrates simple forward, backward, and rotation movements.
"""

from robotapi import RobotController

def main():
    """Run basic movement sequence."""
    # Connect to robot
    robot = RobotController("10.0.0.57")
    robot.connect()
    
    try:
        print("Moving forward for 2 seconds...")
        robot.forward(duration=2.0, speed=50)
        
        print("Moving backward for 2 seconds...")
        robot.backward(duration=2.0, speed=50)
        
        print("Rotating left for 1 second...")
        robot.rotate_left(duration=1.0, speed=50)
        
        print("Rotating right for 1 second...")
        robot.rotate_right(duration=1.0, speed=50)
        
        print("Movement sequence complete!")
        
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
