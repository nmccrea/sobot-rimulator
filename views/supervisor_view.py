#!/usr/bin/python
# -*- Encoding: utf-8 -*

import utils.linalg2_util as linalg

class SupervisorView:

  def __init__( self, viewer, supervisor, robot_geometry ):
    self.viewer = viewer
    self.supervisor = supervisor

    # information for rendering
    self.robot_geometry = robot_geometry      # robot geometry
    self.robot_estimated_traverse_path = []   # path taken by robot's internal image

  # draw a representation of the supervisor's internal state to the frame
  def draw_supervisor_to_frame( self, frame ):
    self._draw_goal_to_frame( frame )
    self._draw_robot_state_estimate_to_frame( frame )
    # draw controller state
    # TODO: determine current controller to draw
    self._draw_avoid_obstacles_controller_to_frame( frame )

  def _draw_goal_to_frame( self, frame ):
    goal = self.supervisor.goal
    frame.add_circle( pos = goal,
                      radius = 0.05,
                      color = "dark green",
                      alpha = 0.25 )
    frame.add_circle( pos = goal,
                      radius = 0.01,
                      color = "black",
                      alpha = 0.5 )

  def _draw_robot_state_estimate_to_frame( self, frame ):
    estimated_pose = self.supervisor.estimated_pose

    # draw the supposed position of the robot
    vertexes = self.robot_geometry.get_transformation_to_pose( estimated_pose ).vertexes[:]
    vertexes.append( vertexes[0] )    # close the drawn polygon
    frame.add_lines(  [ vertexes ],
                      color = "black",
                      linewidth = 0.0075,
                      alpha = 0.5 )

    # draw the supposed traverse path of the robot
    position = estimated_pose.vposition()
    self.robot_estimated_traverse_path.append( position )
    frame.add_lines(  [ self.robot_estimated_traverse_path ],
                      linewidth = 0.005,
                      color = "red",
                      alpha = 0.5 )
  
  # avoid obstacles controller state
  def _draw_avoid_obstacles_controller_to_frame( self, frame ):
    robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()
    
    # draw the detected environment boundary (i.e. sensor readings)
    obstacle_vertexes = self.supervisor.avoid_obstacles_controller.obstacle_vectors[:]
    obstacle_vertexes.append( obstacle_vertexes[0] )  # close the drawn polygon
    obstacle_vertexes = linalg.rotate_and_translate_vectors( obstacle_vertexes, robot_theta, robot_pos )
    frame.add_lines(  [ obstacle_vertexes ],
                      linewidth = 0.005,
                      color = "black",
                      alpha = 1.0 )

    # draw the computed obstacle-avoidance vector
    vector_line = [ [ 0.0, 0.0 ], self.supervisor.avoid_obstacles_controller.heading_vector ]
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    frame.add_lines( [ vector_line ],
                     linewidth = 0.005,
                     color = "blue",
                     alpha = 1.0 )
