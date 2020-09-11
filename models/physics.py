import utils.geometrics_util as geometrics
from sim_exceptions.collision_exception import CollisionException


class Physics:
    def __init__(self, world):
        # the world this physics engine acts on
        self.world = world

    def apply_physics(self):
        self._detect_collisions()
        self._update_proximity_sensors()

    # test the world for existing collisions with solids
    # raises a CollisionException if one occurs
    def _detect_collisions(self):
        colliders = self.world.colliders()
        solids = self.world.solids()

        for collider in colliders:
            polygon1 = collider.global_geometry  # polygon1

            for solid in solids:
                if solid is not collider:  # don't test an object against itself
                    polygon2 = solid.global_geometry  # polygon2

                    if geometrics.check_nearness(
                        polygon1, polygon2
                    ):  # don't bother testing objects that are not near each other
                        if geometrics.convex_polygon_intersect_test(polygon1, polygon2):
                            raise CollisionException()

    # update any proximity sensors that are in range of solid objects
    def _update_proximity_sensors(self):
        robots = self.world.robots
        solids = self.world.solids()

        for robot in robots:
            sensors = robot.ir_sensors

            for sensor in sensors:
                dmin = float("inf")
                detector_line = sensor.detector_line

                for solid in solids:

                    if (
                        solid is not robot
                    ):  # assume that the sensor does not detect it's own robot
                        solid_polygon = solid.global_geometry

                        if geometrics.check_nearness(
                            detector_line, solid_polygon
                        ):  # don't bother testing objects that are not near each other
                            (
                                intersection_exists,
                                intersection,
                                d,
                            ) = geometrics.directed_line_segment_polygon_intersection(
                                detector_line, solid_polygon
                            )

                            if intersection_exists and d < dmin:
                                dmin = d

                # if there is an intersection, update the sensor with the new delta
                # value
                if dmin != float("inf"):
                    sensor.detect(dmin)
                else:
                    sensor.detect(None)
