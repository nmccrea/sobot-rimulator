import utils.linalg2_util as linalg

VECTOR_LEN = 0.75  # length of heading vector


class GoToGoalControllerView:
    def __init__(self, viewer, supervisor):
        self.viewer = viewer
        self.supervisor = supervisor
        self.go_to_goal_controller = supervisor.go_to_goal_controller

    # draw a representation of the go-to-goal controller's internal state to the frame
    def draw_go_to_goal_controller_to_frame(self):
        robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()

        # draw the computed go-to-goal vector
        gtg_heading_vector = linalg.scale(
            linalg.unit(self.go_to_goal_controller.gtg_heading_vector), VECTOR_LEN
        )
        vector_line = [[0.0, 0.0], gtg_heading_vector]
        vector_line = linalg.rotate_and_translate_vectors(
            vector_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [vector_line], linewidth=0.02, color="dark green", alpha=1.0
        )
