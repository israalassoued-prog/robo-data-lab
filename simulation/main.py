import pybullet as p
import pybullet_data
import time

from robot import MobileRobot
from controller import ObstacleAvoidanceController


# -----------------------------
# Start simulation
# -----------------------------

physics_client = p.connect(p.GUI)

p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0, 0, -9.81)

p.loadURDF("plane.urdf")


# -----------------------------
# Create obstacle
# -----------------------------

obstacle_collision = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[0.5, 0.5, 0.5]
)

obstacle_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[0.5, 0.5, 0.5]
)

p.createMultiBody(
    baseMass=0,
    baseCollisionShapeIndex=obstacle_collision,
    baseVisualShapeIndex=obstacle_visual,
    basePosition=[3, 0, 0.5]
)


# -----------------------------
# Create robot and controller
# -----------------------------

robot = MobileRobot(position=[0, 0, 0.15])

controller = ObstacleAvoidanceController(
    safe_distance=1.0
)


# -----------------------------
# Simulation loop
# -----------------------------

for step in range(3000):

    # Read sensors
    sensors = robot.get_distance_sensors()

    # Choose action
    action = controller.choose_action(sensors)

    # Execute action
    if action == "FORWARD":

        robot.move_forward()

    elif action == "LEFT":

        robot.turn_left()

    elif action == "RIGHT":

        robot.turn_right()

    elif action == "STOP":

        robot.stop()

    # Print information
    if step % 100 == 0:

        print(
            f"Step: {step} | "
            f"Front: {sensors['front']:.2f} m | "
            f"Left: {sensors['left']:.2f} m | "
            f"Right: {sensors['right']:.2f} m | "
            f"Action: {action}"
        )

    # Advance simulation
    p.stepSimulation()

    time.sleep(1 / 240)


p.disconnect()