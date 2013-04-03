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
    robot_body = Shapes.arrow_head_polygon( (robot_x, robot_y),
                                            robot_theta,
                                            scale = 0.02 )
    robot_wheels = Shapes.rectangle_pair( (robot_x, robot_y),
                                          5.0, 2.0, 7.0,
                                          angle = robot_theta,
                                          scale = 0.02 )

    # add the robot to the frame
    frame.add_polygons( [ robot_body ],
                        color = "red",
                        alpha = 0.5 )
    frame.add_polygons( robot_wheels,
                        color = "black",
                        alpha = 0.5 )
