from utils import linalg2_util as linalg
from models.geometry import Geometry


class LineSegment(Geometry):
    def __init__(self, vertexes):
        self.vertexes = vertexes  # the beginning and ending points of this line segment

        # define the centerpoint and radius of a circle containing this line segment
        # value is a tuple of the form ( [ cx, cy ], r )
        self.bounding_circle = self._bounding_circle()

    # return a copy of this line segment transformed to the given pose
    def get_transformation_to_pose(self, pose):
        p_pos, p_theta = pose.vunpack()
        return LineSegment(
            linalg.rotate_and_translate_vectors(self.vertexes, p_theta, p_pos)
        )

    # get the centerpoint and radius of a circle that contains this line segment
    def _bounding_circle(self):
        v = self._as_vector()
        vhalf = linalg.scale(v, 0.5)

        c = linalg.add(self.vertexes[0], vhalf)
        r = linalg.mag(v) * 0.5

        return c, r

    # get the vector from the beginning point to the end point of this line segment
    def _as_vector(self):
        return linalg.sub(self.vertexes[1], self.vertexes[0])
