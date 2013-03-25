#!/usr/bin/python
# -*- Encoding: utf-8 -*
# Python implementation of the Week 2 exercise.

from math import *



# Khepera3 Properties (copied from Sim.I.Am)
K3_WHEEL_RADIUS = 0.021         # meters
K3_WHEEL_BASE_LENGTH = 0.0885   # meters
K3_SPEED_FACTOR = 6.2953e-6     
K3_TRANS_VEL_LIMIT = 0.3148     # m/s
K3_ANG_VEL_LIMIT = 2.2763       # rad/s



class Pose:

  def __init__( self, x, y, phi ):
    self.x = x
    self.y = y
    self.phi = phi




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
    old_x = old_pose.x
    old_y = old_pose.y
    old_phi = old_pose.phi
    
    new_x = old_x + ( d_center * cos( old_phi ) )
    new_y = old_y + ( d_center * sin( old_phi ) )
    new_phi = old_phi + ( ( d_right_wheel - d_left_wheel ) / self.wheel_base_length )
    # normalize phi:
    if new_phi > pi:
      new_phi -= 2*pi
    elif new_phi < -pi:
      new_phi += 2*pi
    
    # package and return the new pose
    new_pose = Pose( new_x, new_y, new_phi )
    return new_pose




class Robot: # Khepera3 robot 
  
  def __init__( self ):
    # wheel arrangement:
    self.wheel_radius = K3_WHEEL_RADIUS             # meters
    self.wheel_base_length = K3_WHEEL_BASE_LENGTH   # meters
    
    # wheel speed factor
    self.speed_factor = K3_SPEED_FACTOR
    
    # dynamics
    self.dynamics = DifferentialDriveDynamics( self.wheel_radius, self.wheel_base_length )
    
    ## initialize state
    # set wheel rotations (rad/sec)
    self.left_wheel_rotation = 0.0
    self.right_wheel_rotation = 0.0
    
    # set pose
    self.pose = Pose( 0.0, 0.0, 0.0 )
    
  def update_state( self, dt ):
    pose = self.pose
    v_l = self.left_wheel_rotation
    v_r = self.right_wheel_rotation
    
    self.pose = self.dynamics.apply_dynamics( pose, v_l, v_r, dt )
    
  
  def set_wheel_rotations( self, v_l, v_r ):
    # limit the speeds:
    v, w = self.dynamics.diff_to_uni( v_l, v_r )
    v = max( min( v, K3_TRANS_VEL_LIMIT ), -K3_TRANS_VEL_LIMIT )
    w = max( min( w, K3_ANG_VEL_LIMIT ), -K3_ANG_VEL_LIMIT )
    v_l, v_r = self.dynamics.uni_to_diff( v, w )
    
    # set rotations
    self.left_wheel_rotation = v_l
    self.right_wheel_rotation = v_r
  
  def wheel_rotations( self ):
    return self.left_wheel_rotation, self.right_wheel_rotation
  
