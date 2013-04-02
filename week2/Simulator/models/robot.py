#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
from differential_drive_dynamics import *
from pose import *

# Khepera3 Properties (copied from Sim.I.Am)
K3_WHEEL_RADIUS = 0.021         # meters
K3_WHEEL_BASE_LENGTH = 0.0885   # meters
K3_SPEED_FACTOR = 6.2953e-6     
K3_TRANS_VEL_LIMIT = 0.3148     # m/s
K3_ANG_VEL_LIMIT = 2.2763       # rad/s

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
    # set wheel rotations (rad/s)
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
