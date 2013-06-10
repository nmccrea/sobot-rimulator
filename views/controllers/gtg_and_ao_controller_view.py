#!/usr/bin/python
# -*- Encoding: utf-8 -*

import utils.linalg2_util as linalg

class GTGAndAOControllerView:

  def __init__( self, viewer, gtg_and_ao_controller, supervisor ):
    self.viewer = viewer
    self.gtg_and_ao_controller = gtg_and_ao_controller
    self.supervisor = supervisor

  # draw a representation of the blended controller's internal state to the frame
  def draw_gtg_and_ao_controller_to_frame( self, frame ):
    robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()
    
    # draw the detected environment boundary (i.e. sensor readings)
    obstacle_vertexes = self.supervisor.gtg_and_ao_controller.obstacle_vectors[:]
    obstacle_vertexes.append( obstacle_vertexes[0] )  # close the drawn polygon
    obstacle_vertexes = linalg.rotate_and_translate_vectors( obstacle_vertexes, robot_theta, robot_pos )
    frame.add_lines(  [ obstacle_vertexes ],
                      linewidth = 0.005,
                      color = "black",
                      alpha = 1.0 )

    # draw the computed avoid-obstacles vector
    vector_line = [ [ 0.0, 0.0 ], self.gtg_and_ao_controller.ao_heading_vector ]
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    frame.add_lines( [ vector_line ],
                     linewidth = 0.005,
                     color = "red",
                     alpha = 1.0 )

    # draw the computed go-to-goal vector
    vector_line = [ [ 0.0, 0.0 ], self.gtg_and_ao_controller.gtg_heading_vector ]
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    frame.add_lines( [ vector_line ],
                     linewidth = 0.005,
                     color = "dark green",
                     alpha = 1.0 )

    # draw the computed blended vector
    vector_line = [ [ 0.0, 0.0 ], self.gtg_and_ao_controller.blended_heading_vector ]
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    frame.add_lines( [ vector_line ],
                     linewidth = 0.015,
                     color = "blue",
                     alpha = 1.0 )
