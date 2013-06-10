#!/usr/bin/python
# -*- Encoding: utf-8 -*

import utils.linalg2_util as linalg

class GoToGoalControllerView:

  def __init__( self, viewer, go_to_goal_controller, supervisor ):
    self.viewer = viewer
    self.go_to_goal_controller = go_to_goal_controller
    self.supervisor = supervisor

  # draw a representation of the go-to-goal controller's internal state to the frame
  def draw_go_to_goal_controller_to_frame( self, frame ):
    robot_pos, robot_theta = self.supervisor.estimated_pose.vunpack()
    
    # draw the computed go-to-goal vector
    vector_line = [ [ 0.0, 0.0 ], self.go_to_goal_controller.gtg_heading_vector ]
    vector_line = linalg.rotate_and_translate_vectors( vector_line, robot_theta, robot_pos )
    frame.add_lines( [ vector_line ],
                     linewidth = 0.005,
                     color = "green",
                     alpha = 1.0 )
