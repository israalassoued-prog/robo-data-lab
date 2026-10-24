import pybullet as p
import math


class MobileRobot:

    def __init__(self, position=[0, 0, 0.15]):

        # Robot dimensions
        self.length = 0.6
        self.width = 0.4
        self.height = 0.2

        # Create collision shape
        collision_shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=[
                self.length / 2,
                self.width / 2,
                self.height / 2
            ]
        )

        # Create visual shape
        visual_shape = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=[
                self.length / 2,
                self.width / 2,
                self.height / 2
            ]
        )

        # Create robot
        self.robot_id = p.createMultiBody(
            baseMass=1,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=position
        )

        # Movement speed
        self.speed = 2.0

    # -----------------------------
    # Move forward
    # -----------------------------

    def move_forward(self):

        position, orientation = p.getBasePositionAndOrientation(
            self.robot_id
        )

        # Convert orientation to Euler angles
        _, _, yaw = p.getEulerFromQuaternion(orientation)

        # Calculate movement direction
        dx = math.cos(yaw) * self.speed
        dy = math.sin(yaw) * self.speed

        # Apply velocity
        p.resetBaseVelocity(
            self.robot_id,
            linearVelocity=[dx, dy, 0]
        )

    # -----------------------------
    # Stop
    # -----------------------------

    def stop(self):

        p.resetBaseVelocity(
            self.robot_id,
            linearVelocity=[0, 0, 0],
            angularVelocity=[0, 0, 0]
        )

    
        # -----------------------------
    # Turn left while moving
    # -----------------------------

    def turn_left(self):

        position, orientation = p.getBasePositionAndOrientation(
            self.robot_id
        )

        _, _, yaw = p.getEulerFromQuaternion(orientation)

        dx = math.cos(yaw) * self.speed
        dy = math.sin(yaw) * self.speed

        p.resetBaseVelocity(
            self.robot_id,
            linearVelocity=[dx, dy, 0],
            angularVelocity=[0, 0, 2]
        )


    # -----------------------------
    # Turn right while moving
    # -----------------------------

    def turn_right(self):

        position, orientation = p.getBasePositionAndOrientation(
            self.robot_id
        )

        _, _, yaw = p.getEulerFromQuaternion(orientation)

        dx = math.cos(yaw) * self.speed
        dy = math.sin(yaw) * self.speed

        p.resetBaseVelocity(
            self.robot_id,
            linearVelocity=[dx, dy, 0],
            angularVelocity=[0, 0, -2]
        )
    # -----------------------------
    # Distance sensors
    # -----------------------------

    def get_distance_sensors(self):

        position, orientation = p.getBasePositionAndOrientation(
            self.robot_id
        )

        _, _, yaw = p.getEulerFromQuaternion(orientation)

        # Sensor directions relative to the robot
        sensor_angles = {
            "front": 0,
            "left": math.radians(45),
            "right": math.radians(-45)
        }

        sensor_data = {}

        # Distance the sensor can see
        max_distance = 5.0

        for name, angle in sensor_angles.items():

            # Absolute angle in the world
            sensor_yaw = yaw + angle

            # Start point of the ray
            start = [
                position[0],
                position[1],
                position[2]
            ]

            # End point of the ray
            end = [
                position[0] + max_distance * math.cos(sensor_yaw),
                position[1] + max_distance * math.sin(sensor_yaw),
                position[2]
            ]

            # Cast the ray
            result = p.rayTest(start, end)[0]

            hit_object = result[0]
            hit_fraction = result[2]

            # If the ray hits something
            if hit_object != -1:

                distance = hit_fraction * max_distance

            else:

                distance = max_distance

            sensor_data[name] = distance

        return sensor_data

    # -----------------------------
    # Get position
    # -----------------------------

    def get_position(self):

        position, orientation = p.getBasePositionAndOrientation(
            self.robot_id
        )

        return position

    # -----------------------------
    # Get velocity
    # -----------------------------

    def get_velocity(self):

        linear_velocity, angular_velocity = p.getBaseVelocity(
            self.robot_id
        )

        return linear_velocity, angular_velocity