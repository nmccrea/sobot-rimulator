#!/usr/bin/python
# -*- Encoding: utf-8 -*

import Euv.Shapes as Shapes
import utils.linalg2_util as linalg
from proximity_sensor_view import *
from supervisor_view import *

# Khepera3 Dimensions (from Sim.I.Am by J.P. de la Croix)
K3_TOP_PLATE = [[ -0.031,  0.043 ],
                [ -0.031, -0.043 ],
                [  0.033, -0.043 ],
                [  0.052, -0.021 ],
                [  0.057,  0.000 ],
                [  0.052,  0.021 ],
                [  0.033,  0.043 ]]

class RobotView:
  
  def __init__( self, viewer, robot ):
    self.viewer = viewer
    self.robot = robot

    # add the supervisor views for this robot
    self.supervisor_view = SupervisorView( viewer, robot.supervisor, robot.geometry )
    
    # add the IR sensor views for this robot
    self.ir_sensor_views = []
    for ir_sensor in robot.ir_sensors:
      self.ir_sensor_views.append( ProximitySensorView( viewer, ir_sensor ) )

    self.traverse_path = []  # this robot's traverse path

  def draw_robot_to_frame( self, frame ):
    robot = self.robot

    # draw the internal state ( supervisor ) to the frame
    self.supervisor_view.draw_supervisor_to_frame( frame )

    # draw the IR sensors to the frame
    for ir_sensor_view in self.ir_sensor_views:
      ir_sensor_view.draw_proximity_sensor_to_frame( frame )

    # draw the robot
    robot_bottom = robot.global_geometry.vertexes
    frame.add_polygons( [ robot_bottom ],
                        color = "blue",
                        alpha = 0.5 ) 
    # add decoration
    robot_pos, robot_theta = robot.pose.vunpack()
    robot_top = linalg.rotate_and_translate_vectors( K3_TOP_PLATE, robot_theta, robot_pos )
    frame.add_polygons( [ robot_top ],
                        color = "black",
                        alpha = 0.5 )
    
    # draw the robot's traverse path
    self._draw_traverse_path_to_frame( frame )

  def _draw_traverse_path_to_frame( self, frame ):
    position = self.robot.pose.vposition()
    self.traverse_path.append( position )
    frame.add_lines(  [ self.traverse_path ],
                      color = "black",
                      linewidth = 0.01 )

  # draws the traverse path as dots weighted according to robot speed
  def _draw_rich_traverse_path_to_frame( self, frame ):
    position = self.robot.pose.vposition()
    self.traverse_path.append( position )

    # when robot is moving fast, draw small, opaque dots
    # when robot is moving slow, draw large, transparent dots
    d_min,  d_max = 0.0, 0.01574  # possible distances between dots
    r_min,  r_max = 0.007, 0.02   # dot radius
    a_min,  a_max = 0.3, 0.55     # dot alpha value
    m_r = ( r_max - r_min ) / ( d_min - d_max )
    b_r = r_max - m_r*d_min
    m_a = ( a_max - a_min ) / ( r_min - r_max )
    b_a = a_max - m_a*r_min
    
    prev_posn = self.traverse_path[0]
    for posn in self.traverse_path[1::1]:
      d = linalg.distance( posn, prev_posn )
      r = ( m_r*d ) + b_r
      a = ( m_a*r ) + b_a
      frame.add_circle( pos = posn,
                        radius = r,
                        color = "black",
                        alpha = a)

      prev_posn = posn
