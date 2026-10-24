import pybullet as p
import pybullet_data
import joblib
import time

from robot import MobileRobot
from environment import Environment


# LOAD TRAINED MODEL

MODEL_PATH = "models/random_forest_robot_controller.pkl"

model = joblib.load(MODEL_PATH)

print("AI model loaded successfully!")


# CONNECT TO PYBULLET

p.connect(p.GUI)

p.setAdditionalSearchPath(
    pybullet_data.getDataPath()
)

p.setGravity(
    0,
    0,
    -9.81
)


# CREATE PLANE

p.loadURDF("plane.urdf")


# CREATE ENVIRONMENT

environment = Environment()


# CREATE ROBOT

robot = MobileRobot(
    position=[0, 0, 0.15]
)


# AI CONTROL LOOP

print("\nStarting AI-controlled robot...")
print("Close the PyBullet window to stop.\n")


try:

    while p.isConnected():

        # Read sensors

        sensors = robot.get_distance_sensors()

        front = sensors["front"]
        left = sensors["left"]
        right = sensors["right"]


        # Prepare ML input

        import pandas as pd
        X = pd.DataFrame(
    [[front, left, right]],
    columns=[
        "front_distance",
        "left_distance",
        "right_distance"
    ]
)


        # Predict action

        action = model.predict(X)[0]


        # Display sensor readings

        print(
            f"Front: {front:.2f} m | "
            f"Left: {left:.2f} m | "
            f"Right: {right:.2f} m | "
            f"AI: {action}"
        )


        # Execute AI decision

        if action == "FORWARD":

            robot.move_forward()

        elif action == "LEFT":

            robot.turn_left()

        elif action == "RIGHT":

            robot.turn_right()


        # Simulation

        p.stepSimulation()

        time.sleep(0.02)


except KeyboardInterrupt:

    print("\nSimulation stopped.")


finally:

    if p.isConnected():

        p.disconnect()

    print("Disconnected.")