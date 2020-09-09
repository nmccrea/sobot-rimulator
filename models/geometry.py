# AN ABSTRACT GEOMETRY CLASS


class Geometry:
    def __init__(self, vertexes):
        self.vertexes = vertexes
        self.bounding_circle = None

    def get_transformation_to_pose(self, pose):
        raise NotImplementedError()
