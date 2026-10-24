import pybullet as p


class Environment:

    def __init__(self):

        self.obstacles = []

        self.create_test_environment()


    def create_test_environment(self):

        # ==========================================
        # OBSTACLE 1 — DIRECTLY IN FRONT
        # ==========================================

        self.create_obstacle(
            position=[2.0, 0.0, 0.5],
            size=[0.5, 1.0, 0.5]
        )


        # ==========================================
        # OBSTACLE 2 — ON THE LEFT
        # ==========================================

        self.create_obstacle(
            position=[4.0, 1.8, 0.5],
            size=[0.5, 0.8, 0.5]
        )


        # ==========================================
        # OBSTACLE 3 — ON THE RIGHT
        # ==========================================

        self.create_obstacle(
            position=[6.0, -1.8, 0.5],
            size=[0.5, 0.8, 0.5]
        )


        print("Test environment created.")
        print("Obstacle 1: directly ahead")
        print("Obstacle 2: left side")
        print("Obstacle 3: right side")


    def create_obstacle(self, position, size):

        # Collision shape

        collision_shape = p.createCollisionShape(
            p.GEOM_BOX,
            halfExtents=size
        )


        # Visual shape

        visual_shape = p.createVisualShape(
            p.GEOM_BOX,
            halfExtents=size
        )


        # Static obstacle

        obstacle_id = p.createMultiBody(
            baseMass=0,
            baseCollisionShapeIndex=collision_shape,
            baseVisualShapeIndex=visual_shape,
            basePosition=position
        )


        self.obstacles.append(obstacle_id)