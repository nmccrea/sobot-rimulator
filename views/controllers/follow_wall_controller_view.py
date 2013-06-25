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
    v1_point = surface_line[0]
    frame.add_circle( pos = v1_point,
                      radius = 0.01,
                      color = "blue",
                      alpha = 1.0 )

    # draw the vector from the robot to the wall
    robot_to_wall = [ [ 0.0, 0.0 ], self.follow_wall_controller.robot_to_wall_vector ]
    robot_to_wall = linalg.rotate_and_translate_vectors( robot_to_wall, robot_theta, robot_pos )
    frame.add_lines(  [ robot_to_wall ],
                      linewidth = 0.005,
                      color = "black",
                      alpha = 1.0 )


    # # draw the wall surface vector
    # wall_surface_vector = [ [ 0.0, 0.0 ], self.follow_wall_controller.wall_surface_vector ]
    # frame.add_lines(  [ wall_surface_vector ],
    #                   linewidth = 0.005,
    #                   color = "black",
    #                   alpha = 1.0 )

    # # draw the computed avoid-obstacles vector
    # vector_line = [ [ 0.0, 0.0 ], self.avoid_obstacles_controller.ao_heading_vector ]
    # vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    # frame.add_lines( [ vector_line ],
    #                  linewidth = 0.015,
    #                  color = "red",
    #                  alpha = 1.0 )
