#!/usr/bin/python
# -*- Encoding: utf-8 -*

import utils.linalg2_util as linalg
from controllers.avoid_obstacles_controller_view import *
from controllers.follow_wall_controller_view import *
from controllers.go_to_goal_controller_view import *
from controllers.gtg_and_ao_controller_view import *
from models.control_state import *

class SupervisorView:

  def __init__( self, viewer, supervisor, robot_geometry ):
    self.viewer = viewer
    self.supervisor = supervisor
    self.supervisor_state_machine = supervisor.state_machine

    # controller views
    self.go_to_goal_controller_view = GoToGoalControllerView( viewer,
                                                              supervisor )
    self.avoid_obstacles_controller_view = AvoidObstaclesControllerView( viewer,
                                                                         supervisor )
    self.gtg_and_ao_controller_view = GTGAndAOControllerView( viewer,
                                                              supervisor )
    self.follow_wall_controller_view = FollowWallControllerView(  viewer,
                                                                  supervisor )

    # additional information for rendering
    self.robot_geometry = robot_geometry      # robot geometry
    self.robot_estimated_traverse_path = []   # path taken by robot's internal image

  # draw a representation of the supervisor's internal state to the frame
  def draw_supervisor_to_frame( self ):
    self._draw_goal_to_frame()
    self._draw_robot_state_estimate_to_frame()
    self._draw_current_controller_to_frame()

    # === FOR DEBUGGING ===
    # self._draw_all_controllers_to_frame()

  def _draw_goal_to_frame( self ):
    goal = self.supervisor.goal
    self.viewer.current_frame.add_circle( pos = goal,
                                          radius = 0.05,
                                          color = "dark green",
                                          alpha = 0.25 )
    self.viewer.current_frame.add_circle( pos = goal,
                                          radius = 0.01,
                                          color = "black",
                                          alpha = 0.5 )

  def _draw_robot_state_estimate_to_frame( self ):
    estimated_pose = self.supervisor.estimated_pose

    # draw the supposed position of the robot
    vertexes = self.robot_geometry.get_transformation_to_pose( estimated_pose ).vertexes[:]
    vertexes.append( vertexes[0] )    # close the drawn polygon
    self.viewer.current_frame.add_lines(  [ vertexes ],
                                          color = "black",
                                          linewidth = 0.0075,
                                          alpha = 0.5 )

    # draw the supposed traverse path of the robot
    position = estimated_pose.vposition()
    self.robot_estimated_traverse_path.append( position )
    self.viewer.current_frame.add_lines(  [ self.robot_estimated_traverse_path ],
                                          linewidth = 0.005,
                                          color = "red",
                                          alpha = 0.5 )
  
  # draw the current controller's state to the frame
  def _draw_current_controller_to_frame( self ):
    current_state = self.supervisor_state_machine.current_state
    if current_state == ControlState.GO_TO_GOAL:
      self.go_to_goal_controller_view.draw_go_to_goal_controller_to_frame()
    elif current_state == ControlState.AVOID_OBSTACLES:
      self.avoid_obstacles_controller_view.draw_avoid_obstacles_controller_to_frame()
    elif current_state == ControlState.GTG_AND_AO:
      self.gtg_and_ao_controller_view.draw_gtg_and_ao_controller_to_frame()
    elif current_state in [ ControlState.SLIDE_LEFT, ControlState.SLIDE_RIGHT ]:
      self.follow_wall_controller_view.draw_active_follow_wall_controller_to_frame()

  # draw all of the controllers's to the frame
  def _draw_all_controllers_to_frame( self ):
    self.go_to_goal_controller_view.draw_go_to_goal_controller_to_frame()
    self.avoid_obstacles_controller_view.draw_avoid_obstacles_controller_to_frame()
    # self.gtg_and_ao_controller_view.draw_gtg_and_ao_controller_to_frame()
    self.follow_wall_controller_view.draw_complete_follow_wall_controller_to_frame()
