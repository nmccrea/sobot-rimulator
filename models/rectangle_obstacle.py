from models.polygon import Polygon


class RectangleObstacle:
    def __init__(self, width, height, pose):
        self.pose = pose
        self.width = width
        self.height = height

        # define the geometry
        halfwidth_x = width * 0.5
        halfwidth_y = height * 0.5
        vertexes = [
            [halfwidth_x, halfwidth_y],
            [halfwidth_x, -halfwidth_y],
            [-halfwidth_x, -halfwidth_y],
            [-halfwidth_x, halfwidth_y],
        ]
        self.geometry = Polygon(vertexes)
        self.global_geometry = Polygon(vertexes).get_transformation_to_pose(self.pose)
