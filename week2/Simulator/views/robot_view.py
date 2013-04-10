#!/usr/bin/python
# -*- Encoding: utf-8 -*

import Euv.Shapes as Shapes
import utils.linalg2_util as linalg
from proximity_sensor_view import *

# Khepera3 Dimensions (copied from Sim.I.Am by J.P. de la Croix)
K3_BOTTOM_PLATE = [ [ -0.024, 0.064 ],
                    [ 0.033, 0.064 ],
                    [ 0.057, 0.043 ],
                    [ 0.074, 0.010 ],
                    [ 0.074, -0.010 ],
                    [ 0.057, -0.043 ],
                    [ 0.033, -0.064 ],
                    [ -0.025, -0.064 ],
                    [ -0.042, -0.043 ],
                    [ -0.048, -0.010 ],
                    [ -0.048, 0.010 ],
                    [ -0.042, 0.043 ] ]
K3_TOP_PLATE = [  [ -0.031, 0.043 ],
                  [ -0.031, -0.043 ],
                  [ 0.033, -0.043 ],
                  [ 0.052, -0.021 ],
                  [ 0.057, 0.0 ],
                  [ 0.052, 0.021 ],
                  [ 0.033, 0.043 ] ]

class RobotView:
  
  def __init__( self, viewer, robot ):
    self.viewer = viewer
    self.robot = robot
    
    # add the IR sensor views for this robot
    self.ir_sensor_views = []
    for ir_sensor in robot.ir_sensors:
      self.ir_sensor_views.append( ProximitySensorView( viewer, ir_sensor ) )

  def draw_robot_to_frame( self, frame ):
    # draw the IR sensors to the frame
    for ir_sensor_view in self.ir_sensor_views:
      ir_sensor_view.draw_proximity_sensor_to_frame( frame )


    # grab robot pose values
    robot_pos, robot_theta = self.robot.pose.split()

    # build the robot
    robot_bottom = linalg.rotate_and_translate_vectors( K3_BOTTOM_PLATE,
                                                        robot_theta,
                                                        robot_pos )
    robot_top = linalg.rotate_and_translate_vectors(  K3_TOP_PLATE,
                                                      robot_theta,
                                                      robot_pos )

    
    frame.add_polygons( [ robot_bottom ],
                        color = "blue",
                        alpha = 0.5 ) 
    frame.add_polygons( [ robot_top ],
                        color = "black",
                        alpha = 1.0 ) 
