"""Obstacle avoidance example for RobotAPI.

Demonstrates forward movement with obstacle detection and avoidance.
"""

from robotapi import RobotController
import time

def main():
    """Run obstacle avoidance routine."""
    robot = RobotController("10.0.0.57")
    robot.connect()
    
    try:
        print("Starting obstacle avoidance routine...")
        
        for i in range(5):
            print(f"\nAttempt {i+1}: Moving forward...")
            
            # Try to move forward
            completed = robot.forward(duration=2.0, speed=50)
            
            if not completed:
                print("Obstacle detected! Taking evasive action...")
                
                # Back up
                print("Backing up...")
                robot.backward(duration=1.0, speed=50)
                
                # Rotate to avoid obstacle
                print("Rotating right to avoid...")
                robot.rotate_right(duration=1.5, speed=50)
                
                time.sleep(0.5)
            else:
                print("Path clear, continuing...")
        
        print("\nObstacle avoidance routine complete!")
        
    finally:
        robot.disconnect()


if __name__ == "__main__":
    main()
