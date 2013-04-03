#!/usr/bin/python
# -*- Encoding: utf-8 -*

import Euv.Shapes as Shapes
from proximity_sensor_view import *

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
    robot_x, robot_y, robot_theta = self.robot.pose.unpack()

    # build the robot
    robot_bottom = [  [ -0.024, 0.064 ],
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
    robot_top = [ [ -0.031, 0.043 ],
                  [ -0.031, -0.043 ],
                  [ 0.033, -0.043 ],
                  [ 0.052, -0.021 ],
                  [ 0.057, 0.0 ],
                  [ 0.052, 0.021 ],
                  [ 0.033, 0.043 ] ]
    robot_bottom = Shapes.rotate_and_move_poly( robot_bottom,
                                                robot_theta,
                                                [ robot_x, robot_y ] )
    robot_top = Shapes.rotate_and_move_poly(  robot_top,
                                              robot_theta,
                                              [ robot_x, robot_y ] )

    
    frame.add_polygons( [ robot_bottom ],
                        color = "blue",
                        alpha = 0.5 ) 
    frame.add_polygons( [ robot_top ],
                        color = "black",
                        alpha = 1.0 ) 
