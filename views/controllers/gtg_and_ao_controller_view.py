import utils.linalg2_util as linalg

VECTOR_LEN = 0.75  # length of heading vector


class GTGAndAOControllerView:
    def __init__(self, viewer, supervisor):
        self.viewer = viewer
        self.supervisor = supervisor
        self.gtg_and_ao_controller = supervisor.gtg_and_ao_controller

    # draw a representation of the blended controller's internal state to the frame
    def draw_gtg_and_ao_controller_to_frame(self):
        robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()

        # draw the detected environment boundary (i.e. sensor readings)
        obstacle_vertices = self.gtg_and_ao_controller.obstacle_vectors[:]
        obstacle_vertices.append(obstacle_vertices[0])  # close the drawn polygon
        obstacle_vertices = linalg.rotate_and_translate_vectors(
            obstacle_vertices, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [obstacle_vertices], linewidth=0.005, color="black", alpha=1.0
        )

        # draw the computed avoid-obstacles vector
        ao_heading_vector = linalg.scale(
            linalg.unit(self.gtg_and_ao_controller.ao_heading_vector), VECTOR_LEN
        )
        vector_line = [[0.0, 0.0], ao_heading_vector]
        vector_line = linalg.rotate_and_translate_vectors(
            vector_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [vector_line], linewidth=0.005, color="red", alpha=1.0
        )

        # draw the computed go-to-goal vector
        gtg_heading_vector = linalg.scale(
            linalg.unit(self.gtg_and_ao_controller.gtg_heading_vector), VECTOR_LEN
        )
        vector_line = [[0.0, 0.0], gtg_heading_vector]
        vector_line = linalg.rotate_and_translate_vectors(
            vector_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [vector_line], linewidth=0.005, color="dark green", alpha=1.0
        )

        # draw the computed blended vector
        blended_heading_vector = linalg.scale(
            linalg.unit(self.gtg_and_ao_controller.blended_heading_vector), VECTOR_LEN
        )
        vector_line = [[0.0, 0.0], blended_heading_vector]
        vector_line = linalg.rotate_and_translate_vectors(
            vector_line, robot_theta, robot_pos
        )
        self.viewer.current_frame.add_lines(
            [vector_line], linewidth=0.02, color="blue", alpha=1.0
        )
