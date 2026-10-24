import pybullet as p
import pybullet_data
import time
import csv
import os
import random
import math

from robot import MobileRobot
from controller import ObstacleAvoidanceController


# --------------------------------
# Simulation settings
# --------------------------------

NUM_EPISODES = 20
STEPS_PER_EPISODE = 500

MAX_SENSOR_DISTANCE = 5.0


# --------------------------------
# Start PyBullet
# --------------------------------

physics_client = p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.81)

p.loadURDF("plane.urdf")


# --------------------------------
# Create obstacle
# --------------------------------

def create_obstacle(position):

    collision = p.createCollisionShape(
        p.GEOM_BOX,
        halfExtents=[0.4, 0.4, 0.5]
    )

    visual = p.createVisualShape(
        p.GEOM_BOX,
        halfExtents=[0.4, 0.4, 0.5]
    )

    return p.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=collision,
        baseVisualShapeIndex=visual,
        basePosition=position
    )


# --------------------------------
# Output
# --------------------------------

output_directory = "data/raw"

os.makedirs(output_directory, exist_ok=True)

output_file = os.path.join(
    output_directory,
    "robot_data.csv"
)


# --------------------------------
# Create dataset
# --------------------------------

with open(output_file, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "episode",
        "step",
        "x",
        "y",
        "z",
        "front_distance",
        "left_distance",
        "right_distance",
        "velocity_x",
        "velocity_y",
        "velocity_z",
        "action"
    ])


    # --------------------------------
    # Episodes
    # --------------------------------

    for episode in range(NUM_EPISODES):

        print(
            f"\nStarting episode "
            f"{episode + 1}/{NUM_EPISODES}"
        )


        # Remove previous obstacles
        for body in range(
            p.getNumBodies()
        ):

            # Body 0 is the floor
            if body != 0:

                p.removeBody(body)


        # --------------------------------
        # Random robot start
        # --------------------------------

        start_x = random.uniform(-2, 2)
        start_y = random.uniform(-2, 2)

        start_yaw = random.uniform(
            -math.pi,
            math.pi
        )

        robot = MobileRobot(
            position=[
                start_x,
                start_y,
                0.15
            ]
        )

        # Set random orientation
        orientation = p.getQuaternionFromEuler(
            [0, 0, start_yaw]
        )

        p.resetBasePositionAndOrientation(
            robot.robot_id,
            [start_x, start_y, 0.15],
            orientation
        )


        # --------------------------------
        # Random obstacles
        # --------------------------------

        for _ in range(
            random.randint(5, 10)
        ):

            obstacle_x = random.uniform(
                -4,
                4
            )

            obstacle_y = random.uniform(
                -4,
                4
            )

            # Avoid spawning obstacle
            # directly on robot
            if (
                abs(obstacle_x - start_x) < 1
                and
                abs(obstacle_y - start_y) < 1
            ):
                continue

            create_obstacle(
                [
                    obstacle_x,
                    obstacle_y,
                    0.5
                ]
            )


        # --------------------------------
        # Controller
        # --------------------------------

        controller = ObstacleAvoidanceController(
            safe_distance=1.0
        )


        # --------------------------------
        # Simulation
        # --------------------------------

        for step in range(
            STEPS_PER_EPISODE
        ):

            if not p.isConnected():

                print(
                    "PyBullet disconnected."
                )

                break


            # Sensor readings
            sensors = (
                robot.get_distance_sensors()
            )


            # Robot state
            position = (
                robot.get_position()
            )

            linear_velocity, _ = (
                robot.get_velocity()
            )


            # Controller decision
            action = (
                controller.choose_action(
                    sensors
                )
            )


            # Execute action

            if action == "FORWARD":

                robot.move_forward()

            elif action == "LEFT":

                robot.turn_left()

            elif action == "RIGHT":

                robot.turn_right()

            elif action == "STOP":

                robot.stop()


            # Save sample

            writer.writerow([
                episode,
                step,
                position[0],
                position[1],
                position[2],
                sensors["front"],
                sensors["left"],
                sensors["right"],
                linear_velocity[0],
                linear_velocity[1],
                linear_velocity[2],
                action
            ])


            # Advance simulation

            p.stepSimulation()

            time.sleep(1 / 240)


print("\nData collection complete!")

print(
    f"Dataset saved to: {output_file}"
)

p.disconnect()