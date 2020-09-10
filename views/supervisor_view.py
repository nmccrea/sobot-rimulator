from views.controllers.avoid_obstacles_controller_view import AvoidObstaclesControllerView
from views.controllers.follow_wall_controller_view import FollowWallControllerView
from views.controllers.go_to_goal_controller_view import GoToGoalControllerView
from views.controllers.gtg_and_ao_controller_view import GTGAndAOControllerView
from robot_control.control_state import ControlState


class SupervisorView:
    def __init__(self, viewer, supervisor, robot_geometry):
        self.viewer = viewer
        self.supervisor = supervisor
        self.supervisor_state_machine = supervisor.state_machine

        # controller views
        self.go_to_goal_controller_view = GoToGoalControllerView(viewer, supervisor)
        self.avoid_obstacles_controller_view = AvoidObstaclesControllerView(
            viewer, supervisor
        )
        self.gtg_and_ao_controller_view = GTGAndAOControllerView(viewer, supervisor)
        self.follow_wall_controller_view = FollowWallControllerView(viewer, supervisor)

        # additional information for rendering
        self.robot_geometry = robot_geometry  # robot geometry
        self.robot_estimated_traverse_path = []  # path taken by robot's internal image

    # draw a representation of the supervisor's internal state to the frame
    def draw_supervisor_to_frame(self):
        # update the estimated robot traverse path
        self.robot_estimated_traverse_path.append(
            self.supervisor.estimated_pose.vposition()
        )

        # draw the goal to frame
        self._draw_goal_to_frame()

        # draw the supervisor-generated data to frame if indicated
        if self.viewer.show_invisibles:
            self._draw_robot_state_estimate_to_frame()
            self._draw_current_controller_to_frame()

        # === FOR DEBUGGING ===
        # self._draw_all_controllers_to_frame()

    def _draw_goal_to_frame(self):
        goal = self.supervisor.goal
        self.viewer.current_frame.add_circle(
            pos=goal, radius=0.05, color="dark green", alpha=0.65
        )
        self.viewer.current_frame.add_circle(
            pos=goal, radius=0.01, color="black", alpha=0.5
        )

    def _draw_robot_state_estimate_to_frame(self):
        # draw the estimated position of the robot
        vertices = self.robot_geometry.get_transformation_to_pose(
            self.supervisor.estimated_pose
        ).vertices[:]
        vertices.append(vertices[0])  # close the drawn polygon
        self.viewer.current_frame.add_lines(
            [vertices], color="black", linewidth=0.0075, alpha=0.5
        )

        # draw the estimated traverse path of the robot
        self.viewer.current_frame.add_lines(
            [self.robot_estimated_traverse_path],
            linewidth=0.005,
            color="red",
            alpha=0.5,
        )

    # draw the current controller's state to the frame
    def _draw_current_controller_to_frame(self):
        current_state = self.supervisor_state_machine.current_state
        if current_state == ControlState.GO_TO_GOAL:
            self.go_to_goal_controller_view.draw_go_to_goal_controller_to_frame()
        elif current_state == ControlState.AVOID_OBSTACLES:
            self.avoid_obstacles_controller_view.draw_avoid_obstacles_controller_to_frame()
        elif current_state == ControlState.GTG_AND_AO:
            self.gtg_and_ao_controller_view.draw_gtg_and_ao_controller_to_frame()
        elif current_state in [ControlState.SLIDE_LEFT, ControlState.SLIDE_RIGHT]:
            self.follow_wall_controller_view.draw_active_follow_wall_controller_to_frame()

    # draw all of the controllers's to the frame
    def _draw_all_controllers_to_frame(self):
        self.go_to_goal_controller_view.draw_go_to_goal_controller_to_frame()
        self.avoid_obstacles_controller_view.draw_avoid_obstacles_controller_to_frame()
        # self.gtg_and_ao_controller_view.draw_gtg_and_ao_controller_to_frame()
        self.follow_wall_controller_view.draw_complete_follow_wall_controller_to_frame()
