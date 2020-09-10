from utils import linalg2_util as linalg
from models.geometry import Geometry


class Polygon(Geometry):
    def __init__(self, vertices):
        self.vertices = vertices  # a list of 2-dimensional vectors

        # define the centerpoint and radius of a circle containing this polygon
        # value is a tuple of the form ( [ cx, cy ], r )
        # NOTE: this may not be the "minimum bounding circle"
        self.bounding_circle = self._bounding_circle()

    # return a copy of this polygon transformed to the given pose
    def get_transformation_to_pose(self, pose):
        p_pos, p_theta = pose.vunpack()
        return Polygon(
            linalg.rotate_and_translate_vectors(self.vertices, p_theta, p_pos)
        )

    # get a list of of this polygon's edges as vertex pairs
    def edges(self):
        vertices = self.vertices

        edges = []
        n = len(vertices)
        for i in range(n):
            edges.append([vertices[i], vertices[(i + 1) % n]])

        return edges

    # get the number of edges of this polygon
    def numedges(self):
        return len(self.vertices)

    # get the centerpoint and radius for a circle that completely contains this polygon
    def _bounding_circle(self):
        # NOTE: this method is meant to give a quick bounding circle
        #   the circle calculated may not be the "minimum bounding circle"

        c = self._centroidish()
        r = 0.0
        for v in self.vertices:
            d = linalg.distance(c, v)
            if d > r:
                r = d

        return c, r

    # approximate the centroid of this polygon
    def _centroidish(self):
        # NOTE: this method is meant to give a quick and dirty approximation of center
        # of the polygon
        #   it returns the average of the vertices
        #   the actual centroid may not be equivalent

        n = len(self.vertices)
        x = 0.0
        y = 0.0
        for v in self.vertices:
            x += v[0]
            y += v[1]
        x /= n
        y /= n

        return [x, y]
