#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import math_utils
from pose import *

class ProximitySensor:

  def __init__( self, robot,          # robot this sensor is attached to
                      relative_pose,  # pose of this sensor relative to robot
                      min_range,      # min sensor range (meters)
                      max_range,      # max sensor range (meters)
                      phi_view ):     # view angle of this sensor (rad from front of robot)
    
    # pose attributes
    self.robot = robot
    self.relative_pose = relative_pose
    self.update_pose()                # determine global pose
    
    # sensitivity attributes
    self.min_range = min_range
    self.max_range = max_range
    self.phi_view = phi_view

  def update_pose( self ):
    # get the elements of the robot's pose
    robot_x, robot_y, robot_theta = self.robot.pose.unpack()

    # get the elements of this sensor's relative pose
    rel_x, rel_y, rel_theta = self.relative_pose.unpack()
    
    # construct this sensor's global pose
    global_x_d, global_y_d = math_utils.rotate_vector( rel_x, rel_y, robot_theta )
    global_x = robot_x + global_x_d
    global_y = robot_y + global_y_d
    global_theta = robot_theta + rel_theta

    self.pose = Pose( global_x, global_y, global_theta )
