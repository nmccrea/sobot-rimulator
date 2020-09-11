from math import e, ceil
from models.line_segment import LineSegment
from models.pose import Pose
from models.sensor import Sensor

MIN_READ_VALUE = 18
MAX_READ_VALUE = 3960


class ProximitySensor(Sensor):
    def __init__(
        self,
        robot,  # robot this sensor is attached to
        placement_pose,  # pose of this sensor relative to the robot (NOTE: normalized on robot located at origin and with theta 0, i.e. facing east )
        min_range,  # min sensor range (meters)
        max_range,  # max sensor range (meters)
        phi_view,
    ):  # view angle of this sensor (rad from front of robot)

        # bind the robot
        self.robot = robot

        # pose attributes
        self.placement_pose = (
            placement_pose  # pose of this sensor relative to the robot
        )
        self.pose = Pose(0.0, 0.0, 0.0)  # global pose of this sensor

        # detector line
        self.detector_line_source = LineSegment([[0.0, 0.0], [max_range, 0.0]])
        self.detector_line = LineSegment([[0.0, 0.0], [max_range, 0.0]])

        # pose and detector_line are incorrect until:
        # set initial position
        self.update_position()

        # sensitivity attributes
        self.min_range = min_range
        self.max_range = max_range
        self.phi_view = phi_view

        # physical distance detected to target as a proportion of max_range ( must be
        # in range [0, 1] or None )
        self.target_delta = None

        # sensor output
        self.read_value = MIN_READ_VALUE

    # set this proximity sensor to detect an object at distance ( delta * max_range )
    def detect(self, delta):
        if delta is not None and (delta < 0.0 or delta > 1.0):
            raise Exception("delta out of bounds - must be in range [0.0, 1.0]")

        if delta is None:
            self.target_delta = None
            self.read_value = MIN_READ_VALUE
        else:
            max_range = self.max_range
            min_range = self.min_range

            d = max_range * delta  # d is the real distance in meters
            if d <= min_range:  # d in [0.00, 0.02]
                self.target_delta = min_range / max_range
                self.read_value = MAX_READ_VALUE
            else:  # d in (0.02, 0.20]
                self.target_delta = delta
                self.read_value = max(
                    MIN_READ_VALUE, int(ceil(MAX_READ_VALUE * e ** (-30 * (d - 0.02))))
                )

    # get this sensor's output
    def read(self):
        return self.read_value

    # update the global position of this sensor
    def update_position(self):
        # update global pose
        self._update_pose()

        # update detector line
        self.detector_line = self.detector_line_source.get_transformation_to_pose(
            self.pose
        )

    # update this sensor's pose
    def _update_pose(self):
        self.pose = self.placement_pose.transform_to(self.robot.pose)
