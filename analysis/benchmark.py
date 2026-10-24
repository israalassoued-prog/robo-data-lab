import os
import sys
import random

import numpy as np
import pandas as pd
import pybullet as p
import pybullet_data
import joblib

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from simulation.robot import MobileRobot


# CONFIGURATION


MODEL_PATH = "models/random_forest_robot_controller.pkl"

N_EPISODES = 20
MAX_STEPS = 1500
GOAL_X = 13.0


# ENVIRONMENT

def create_environment():

    obstacles = []

    obstacle_positions = [
        [3.0, 0.0, 0.5],
        [6.0, random.uniform(-2.0, 2.0), 0.5],
        [9.0, random.uniform(-2.0, 2.0), 0.5],
        [12.0, random.uniform(-2.0, 2.0), 0.5]
    ]

    obstacle_sizes = [
        [0.5, 2.0, 0.5],
        [0.5, 0.8, 0.5],
        [0.5, 0.8, 0.5],
        [0.5, 0.8, 0.5]
    ]

    for position, size in zip(
        obstacle_positions,
        obstacle_sizes
    ):

        collision_shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=size
        )

        visual_shape = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=size
        )

        obstacle_id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=position
        )

        obstacles.append(obstacle_id)

    return obstacles


# RULE-BASED CONTROLLER

def rule_based_action(sensors):

    front = sensors["front"]
    left = sensors["left"]
    right = sensors["right"]

    if front < 1.5:

        if left > right:
            return "LEFT"

        else:
            return "RIGHT"

    return "FORWARD"


# AI CONTROLLER

def ai_action(model, sensors):

    front = sensors["front"]
    left = sensors["left"]
    right = sensors["right"]

    X = pd.DataFrame(
        [[front, left, right]],
        columns=[
            "front_distance",
            "left_distance",
            "right_distance"
        ]
    )

    return model.predict(X)[0]


# EXECUTE ACTION

def execute_action(robot, action):

    if action == "FORWARD":

        robot.move_forward()

    elif action == "LEFT":

        robot.turn_left()

    elif action == "RIGHT":

        robot.turn_right()


# RUN ONE EPISODE

def run_episode(controller, model=None):

    p.connect(p.DIRECT)

    p.setAdditionalSearchPath(
        pybullet_data.getDataPath()
    )

    p.setGravity(
        0,
        0,
        -9.81
    )

    p.loadURDF("plane.urdf")

    robot = MobileRobot()

    obstacles = create_environment()

    turns = 0

    minimum_distance = float("inf")

    success = False
    collision = False

    for step in range(MAX_STEPS):

        # READ SENSORS

        sensors = robot.get_distance_sensors()

        front = float(sensors["front"])
        left = float(sensors["left"])
        right = float(sensors["right"])

        sensor_distances = {
            "front": front,
            "left": left,
            "right": right
        }

        minimum_distance = min(
            minimum_distance,
            front,
            left,
            right
        )

        # SELECT ACTION

        if controller == "RULE":

            action = rule_based_action(
                sensor_distances
            )

        else:

            action = ai_action(
                model,
                sensor_distances
            )

        # COUNT TURNS

        if action != "FORWARD":
            turns += 1

        # MOVE ROBOT

        execute_action(
            robot,
            action
        )

        p.stepSimulation()

        # CHECK COLLISION
        # ONLY WITH OBSTACLES

        contact_points = p.getContactPoints(
            bodyA=robot.robot_id
        )

        for contact in contact_points:

            body_a = contact[1]
            body_b = contact[2]

            if (
                body_a in obstacles
                or body_b in obstacles
            ):

                collision = True
                break

        if collision:
            break

        # CHECK GOAL

        position = robot.get_position()

        if position[0] >= GOAL_X:

            success = True
            break

    steps = step + 1

    p.disconnect()

    return {
        "success": success,
        "collision": collision,
        "steps": steps,
        "turns": turns,
        "minimum_distance": minimum_distance
    }


# RUN BENCHMARK

def run_benchmark(controller, model=None):

    results = []

    print()
    print("=" * 60)
    print(f"{controller} CONTROLLER")
    print("=" * 60)

    for episode in range(N_EPISODES):

        result = run_episode(
            controller,
            model
        )

        results.append(result)

        print(
            f"Episode {episode + 1:02d} | "
            f"Success: {result['success']} | "
            f"Collision: {result['collision']} | "
            f"Steps: {result['steps']} | "
            f"Turns: {result['turns']} | "
            f"Min Distance: "
            f"{result['minimum_distance']:.2f} m"
        )

    return results


# SUMMARY

def summarize(results):

    return {
        "Success Rate (%)":
            np.mean(
                [r["success"] for r in results]
            ) * 100,

        "Collision Rate (%)":
            np.mean(
                [r["collision"] for r in results]
            ) * 100,

        "Average Steps":
            np.mean(
                [r["steps"] for r in results]
            ),

        "Average Turns":
            np.mean(
                [r["turns"] for r in results]
            ),

        "Average Minimum Distance":
            np.mean(
                [r["minimum_distance"] for r in results]
            )
    }


# MAIN

print("=" * 60)
print("ROBOT CONTROLLER BENCHMARK")
print("=" * 60)

print(
    f"Episodes per controller: {N_EPISODES}"
)

print()
print("Loading Random Forest model...")

model = joblib.load(
    MODEL_PATH
)


# RULE-BASED BENCHMARK

random.seed(42)

rule_results = run_benchmark(
    "RULE"
)


# AI BENCHMARK

random.seed(42)

ai_results = run_benchmark(
    "AI",
    model
)


# FINAL COMPARISON

rule_summary = summarize(
    rule_results
)

ai_summary = summarize(
    ai_results
)

comparison = pd.DataFrame(
    [
        rule_summary,
        ai_summary
    ],
    index=[
        "Rule-Based",
        "Random Forest AI"
    ]
)


print()
print("=" * 60)
print("FINAL COMPARISON")
print("=" * 60)

print(
    comparison.round(2)
)


# SAVE RESULTS

os.makedirs(
    "results",
    exist_ok=True
)

comparison.to_csv(
    "results/controller_benchmark.csv"
)

print()
print("Saved:")
print(
    "results/controller_benchmark.csv"
)