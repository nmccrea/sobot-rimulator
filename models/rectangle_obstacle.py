from models.polygon import Polygon


class RectangleObstacle:
    def __init__(self, width, height, pose):
        self.pose = pose
        self.width = width
        self.height = height

        # define the geometry
        halfwidth_x = width * 0.5
        halfwidth_y = height * 0.5
        vertices = [
            [halfwidth_x, halfwidth_y],
            [halfwidth_x, -halfwidth_y],
            [-halfwidth_x, -halfwidth_y],
            [-halfwidth_x, halfwidth_y],
        ]
        self.geometry = Polygon(vertices)
        self.global_geometry = Polygon(vertices).get_transformation_to_pose(self.pose)
