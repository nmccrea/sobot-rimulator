#!/usr/bin/python
# -*- Encoding: utf-8 -*
# Python implementation of the Week 2 exercise.

from math import *
from pose import *

class DifferentialDriveDynamics:
  
  def __init__( self, wheel_radius, wheel_base_length):
    self.wheel_radius = wheel_radius
    self.wheel_base_length = wheel_base_length
    
  def uni_to_diff( self, v, w ):
    # v = translational velocity (m/s)
    # w = angular velocity (rad/s)
    
    R = self.wheel_radius
    L = self.wheel_base_length
    
    v_l = ( (2.0 * v) - (w*L) ) / (2.0 * R)
    v_r = ( (2.0 * v) + (w*L) ) / (2.0 * R)
    
    return v_l, v_r
    
  def diff_to_uni( self, v_l, v_r ):
    # v_l = left-wheel angular velocity (rad/s)
    # v_r = right-wheel angular velocity (rad/s)
    
    R = self.wheel_radius
    L = self.wheel_base_length
    
    v = ( R / 2.0 ) * ( v_r + v_l )
    w = ( R / L ) * ( v_r - v_l )
    
    return v, w
  
  def apply_dynamics( self, old_pose, v_l, v_r, d_t ):
    wheel_meters_per_rad = self.wheel_radius
    
    # calculate the distance traveled
    d_left_wheel = d_t * v_l * wheel_meters_per_rad
    d_right_wheel = d_t * v_r * wheel_meters_per_rad
    d_center = ( d_left_wheel + d_right_wheel ) / 2.0
    
    # calculate the new pose
    old_x, old_y, old_theta = old_pose.unpack()
    
    new_x = old_x + ( d_center * cos( old_theta ) )
    new_y = old_y + ( d_center * sin( old_theta ) )
    new_theta = old_theta + ( ( d_right_wheel - d_left_wheel ) / self.wheel_base_length )
    
    # package and return the new pose
    new_pose = Pose( new_x, new_y, new_theta )
    return new_pose
