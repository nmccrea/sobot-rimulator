import utils.linalg2_util as linalg

VECTOR_LEN = 0.75  # length of heading vector


class AvoidObstaclesControllerView:
    def __init__(self, viewer, supervisor):
        self.viewer = viewer
        self.supervisor = supervisor
        self.avoid_obstacles_controller = supervisor.avoid_obstacles_controller

    # draw a representation of the avoid-obstacles controller's internal state to the
    # frame
    def draw_avoid_obstacles_controller_to_frame(self):
        robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()

        # draw the detected environment boundary (i.e. sensor readings)
        obstacle_vertices = self.avoid_obstacles_controller.obstacle_vectors[:]
        obstacle_vertices.append(obstacle_vertices[0])  # close the drawn polygon
        obstacle_vertices = linalg.rotate_and_translate_vectors(
            obstacle_vertices, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [obstacle_vertices], linewidth=0.005, color="black", alpha=1.0
        )

        # draw the computed avoid-obstacles vector
        ao_heading_vector = linalg.scale(
            linalg.unit(self.avoid_obstacles_controller.ao_heading_vector), VECTOR_LEN
        )
        vector_line = [[0.0, 0.0], ao_heading_vector]
        vector_line = linalg.rotate_and_translate_vectors(
            vector_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [vector_line], linewidth=0.02, color="red", alpha=1.0
        )
