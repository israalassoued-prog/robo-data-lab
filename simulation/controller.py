class ObstacleAvoidanceController:

    def __init__(self, safe_distance=1.0):
        self.safe_distance = safe_distance

    def choose_action(self, sensors):

        front = sensors["front"]
        left = sensors["left"]
        right = sensors["right"]

        # Obstacle directly ahead
        if front < self.safe_distance:

            # Choose the side with more free space
            if left > right:
                return "LEFT"
            else:
                return "RIGHT"

        # No immediate obstacle
        return "FORWARD"