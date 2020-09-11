import utils.linalg2_util as linalg
from robot_control.control_state import ControlState

VECTOR_LEN = 0.75  # length of heading vector

FWDIR_LEFT = 0
FWDIR_RIGHT = 1


class FollowWallControllerView:
    def __init__(self, viewer, supervisor):
        self.viewer = viewer
        self.supervisor = supervisor
        self.follow_wall_controller = supervisor.follow_wall_controller

    # draw a representation of the currently-active side of the follow-wall controller
    # state to the frame
    def draw_active_follow_wall_controller_to_frame(self):
        # determine which side to renderi
        current_state = self.supervisor.state_machine.current_state
        if current_state == ControlState.SLIDE_LEFT:
            self._draw_follow_wall_controller_to_frame_by_side(FWDIR_LEFT)
        elif current_state == ControlState.SLIDE_RIGHT:
            self._draw_follow_wall_controller_to_frame_by_side(FWDIR_RIGHT)
        else:
            raise Exception(
                "applying follow-wall controller when not in a sliding state currently "
                "not supported"
            )

    # draw a representation of both sides of the follow-wall controller to the frame
    def draw_complete_follow_wall_controller_to_frame(self):
        self._draw_follow_wall_controller_to_frame_by_side(FWDIR_LEFT)
        self._draw_follow_wall_controller_to_frame_by_side(FWDIR_RIGHT)

    # draw the controller to the frame for the indicated side only
    def _draw_follow_wall_controller_to_frame_by_side(self, side):
        if side == FWDIR_LEFT:
            surface_line = self.follow_wall_controller.l_wall_surface
            distance_vector = self.follow_wall_controller.l_distance_vector
            fw_heading_vector = self.follow_wall_controller.l_fw_heading_vector
        elif side == FWDIR_RIGHT:
            surface_line = self.follow_wall_controller.r_wall_surface
            distance_vector = self.follow_wall_controller.r_distance_vector
            fw_heading_vector = self.follow_wall_controller.r_fw_heading_vector
        else:
            raise Exception("unrecognized argument: follow-wall direction indicator")

        robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()

        # draw the estimated wall surface
        surface_line = linalg.rotate_and_translate_vectors(
            surface_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [surface_line], linewidth=0.01, color="black", alpha=1.0
        )

        # draw the measuring line from the robot to the wall
        range_line = [[0.0, 0.0], distance_vector]
        range_line = linalg.rotate_and_translate_vectors(
            range_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [range_line], linewidth=0.005, color="black", alpha=1.0
        )

        # draw the computed follow-wall vector
        fw_heading_vector = linalg.scale(linalg.unit(fw_heading_vector), VECTOR_LEN)
        vector_line = [[0.0, 0.0], fw_heading_vector]
        vector_line = linalg.rotate_and_translate_vectors(
            vector_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [vector_line], linewidth=0.02, color="orange", alpha=1.0
        )
