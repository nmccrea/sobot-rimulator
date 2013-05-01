#!/usr/bin/python
# -*- Encoding: utf-8 -*

import utils.linalg2_util as linalg
from line_segment import *
from pose import *

class ProximitySensor:

  def __init__( self, robot,          # robot this sensor is attached to
                      relative_pose,  # pose of this sensor relative to robot (NOTE: normalized on robot located at origin and with theta 0, i.e. facing east )
                      min_range,      # min sensor range (meters)
                      max_range,      # max sensor range (meters)
                      phi_view ):     # view angle of this sensor (rad from front of robot)
    
    
    # bind the robot
    self.robot = robot

    # pose attributes
    self.relative_pose = relative_pose
    self.pose = Pose( 0.0, 0.0, 0.0 ) # initialize pose object
    
    # detector line
    self.detector_line_source = LineSegment( [ [0.0, 0.0], [max_range, 0.0] ] )
    self.detector_line = LineSegment( [ [0.0, 0.0], [max_range, 0.0] ] )  

    # pose and detector_line are incorrect until:
    # set initial state
    self.update_state()
    
    # sensitivity attributes
    self.min_range = min_range
    self.max_range = max_range
    self.phi_view = phi_view

  def update_state( self ):
    # update global pose
    self.update_pose()

    # update detector line
    self.detector_line = self.detector_line_source.get_transformation_to_pose( self.pose )

  def update_pose( self ):
    # get the elements of the robot's pose
    robot_vect, robot_theta = self.robot.pose.vunpack()

    # get the elements of this sensor's relative pose
    rel_vect, rel_theta = self.relative_pose.vunpack()
    
    # construct this sensor's global pose
    global_vect_d = linalg.rotate_vector( rel_vect, robot_theta )
    global_vect = linalg.add( robot_vect, global_vect_d ) 
    global_theta = robot_theta + rel_theta

    self.pose.vupdate( global_vect, global_theta )

  def set_proximity( self, distance ):
    # TODO: set the sensor value for the given distance
    False

  def read( self ):
    # TODO: return this sensor's sensor value
    False
