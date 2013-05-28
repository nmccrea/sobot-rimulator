#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
import utils.linalg2_util as linalg
from line_segment import *
from pose import *
from sensor import *

class ProximitySensor( Sensor ):

  def __init__( self, robot,          # robot this sensor is attached to
                      placement_pose, # pose of this sensor relative to the robot (NOTE: normalized on robot located at origin and with theta 0, i.e. facing east )
                      min_range,      # min sensor range (meters)
                      max_range,      # max sensor range (meters)
                      phi_view ):     # view angle of this sensor (rad from front of robot)
    
    
    # bind the robot
    self.robot = robot

    # pose attributes
    self.placement_pose = placement_pose  # pose of this sensor relative to the robot
    self.pose = Pose( 0.0, 0.0, 0.0 )     # global pose of this sensor
    
    # detector line
    self.detector_line_source = LineSegment( [ [0.0, 0.0], [max_range, 0.0] ] )
    self.detector_line = LineSegment( [ [0.0, 0.0], [max_range, 0.0] ] )  

    # pose and detector_line are incorrect until:
    # set initial position
    self.update_position()
    
    # sensitivity attributes
    self.min_range = min_range
    self.max_range = max_range
    self.phi_view = phi_view

    # physical distance detected to target as a proportion of max_range ( must be in range [0, 1] or None )
    self.target_delta = None

    # sensor output
    self.read_value = 0

  # set this proximity sensor to detect an object at distance ( delta * max_range )
  def detect( self, delta ):
    if delta != None and ( delta < 0.0 or delta > 1.0 ):
      raise Exception("delta out of bounds - must be in range [0.0, 1.0]")

    if delta == None:
      self.target_delta = None
      self.read_value = 0
    else:
      max_range = self.max_range
      min_range = self.min_range

      d = max_range * delta
      if d <= min_range:        # d in [0.00, 0.02]
        self.target_delta = min_range / max_range
        self.read_value = 3960
      else:                     # d in (0.02, 0.20]
        self.target_delta = delta
        self.read_value = int( ceil( 3960 * e**( -30 * (d-0.02) ) ) )

  # get this sensor's output
  def read( self ):
    return self.read_value

  # update the global position of this sensor
  def update_position( self ):
    # update global pose
    self._update_pose()

    # update detector line
    self.detector_line = self.detector_line_source.get_transformation_to_pose( self.pose )

  # update this sensor's pose
  def _update_pose( self ):
    # get the elements of the robot's pose
    robot_vect, robot_theta = self.robot.pose.vunpack()

    # get the elements of this sensor's relative pose
    rel_vect, rel_theta = self.placement_pose.vunpack()
    
    # construct this sensor's global pose
    global_vect_d = linalg.rotate_vector( rel_vect, robot_theta )
    global_vect = linalg.add( robot_vect, global_vect_d ) 
    global_theta = robot_theta + rel_theta

    self.pose.vupdate( global_vect, global_theta )
