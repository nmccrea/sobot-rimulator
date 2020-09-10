# AN ABSTRACT GEOMETRY CLASS


class Geometry:
    def __init__(self, vertices):
        self.vertices = vertices
        self.bounding_circle = None

    def get_transformation_to_pose(self, pose):
        raise NotImplementedError()
