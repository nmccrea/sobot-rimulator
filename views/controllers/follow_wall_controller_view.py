#!/usr/bin/python
# -*- Encoding: utf-8 -*

import utils.linalg2_util as linalg

class FollowWallControllerView:

  def __init__( self, viewer, supervisor ):
    self.viewer = viewer
    self.supervisor = supervisor
    self.follow_wall_controller = supervisor.follow_wall_controller

  # draw a representation of the avoid-obstacles controller's internal state to the frame
  def draw_follow_wall_controller_to_frame( self, frame ):
    robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()

    # draw the estimated wall surface
    surface_line = self.follow_wall_controller.wall_surface
    surface_line = linalg.rotate_and_translate_vectors( surface_line, robot_theta, robot_pos )
    frame.add_lines(  [ surface_line ],
                      linewidth = 0.005,
                      color = "black",
                      alpha = 1.0 )

    # draw the measuring line from the robot to the wall
    range_line = [ [ 0.0, 0.0 ], self.follow_wall_controller.distance_vector ]
    range_line = linalg.rotate_and_translate_vectors( range_line, robot_theta, robot_pos )
    frame.add_lines(  [ range_line ],
                      linewidth = 0.005,
                      color = "black",
                      alpha = 1.0 )

    # draw the perpendicular component vector
    perpendicular_component_line = [ [ 0.0, 0.0 ], self.follow_wall_controller.perpendicular_component ]
    perpendicular_component_line = linalg.rotate_and_translate_vectors( perpendicular_component_line, robot_theta, robot_pos )
    frame.add_lines(  [ perpendicular_component_line ],
                      linewidth = 0.01,
                      color = "blue",
                      alpha = 0.8 )

    # draw the parallel component vector
    parallel_component_line = [ [ 0.0, 0.0 ], self.follow_wall_controller.parallel_component ]
    parallel_component_line = linalg.rotate_and_translate_vectors( parallel_component_line, robot_theta, robot_pos )
    frame.add_lines(  [ parallel_component_line ],
                      linewidth = 0.01,
                      color = "red",
                      alpha = 0.8 )

    # draw the computed follow-wall vector
    vector_line = [ [ 0.0, 0.0 ], self.follow_wall_controller.fw_heading_vector ]
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    frame.add_lines( [ vector_line ],
                     linewidth = 0.015,
                     color = "orange",
                     alpha = 1.0 )
