#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

from utils import linalg2_util as linalg
from utils import math_util

class AvoidObstaclesController:

  def __init__( self, supervisor ):
    # bind the supervisor
    self.supervisor = supervisor

    # sensor placements
    self.proximity_sensor_placements = supervisor.proximity_sensor_placements()

    # sensor gains (weights)
    self.sensor_gains = [   1.0-( (0.9*abs(p.theta)) / pi )   for p in supervisor.proximity_sensor_placements() ]

    # control gains
    self.kP = 5.0
    self.kI = 0.5
    self.kD = 0.1
    
    # stored values - for computing next results
    self.prev_time = 0.0
    self.prev_eP = 0.0
    self.prev_eI = 0.0

  def execute( self ):
    # determine the global pose of each sensor
    robot_pose = self.supervisor.estimated_pose()
    global_sensor_poses = []
    for p in self.proximity_sensor_placements:
      global_sensor_poses.append( p.transform_to( robot_pose ).vunpack() )

    # calculate the position of detected obstacles in the robot's reference frame
    sensor_distances = self.supervisor.proximity_sensor_real_distances()
    target_vectors = []
    for i in range( len( sensor_distances ) ):
      if sensor_distances[i] != None:
        # calculate the position of the obstacle in the robot's reference frame
        sensor_pos, sensor_theta = global_sensor_poses[i]
        vector = [ 1.0, 0.0 ] # the neutral unit vector
        vector = linalg.scale( vector, sensor_distances[i] )
        vector = linalg.rotate_and_translate_vector( vector, sensor_theta, sensor_pos )
        target_vectors.append( vector )
      else:
        target_vectors.append( [ 0.0, 0.0 ] )
