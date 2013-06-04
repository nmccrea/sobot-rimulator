#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

# an interfacing allowing a controller to interact with its supervisor 
class SupervisorControllerInterface:

  def __init__( self, supervisor ):
    self.supervisor = supervisor

  # get the supervisor's internal pose estimation
  def estimated_pose( self ):
    return self.supervisor.estimated_pose

  # get the placement poses of the robot's sensors
  def proximity_sensor_placements( self ):
    return self.supervisor.proximity_sensor_placements

  # get the robot's proximity sensor read values converted to real distances in meters
  def proximity_sensor_real_distances( self ):
    return [   0.02-( log(readval/3960.0) )/30.0   for readval in self.supervisor.robot.read_proximity_sensors() ]

  # get the supervisor's goal
  def goal( self ):
    return self.supervisor.goal

  # get the supervisor's internal clock time
  def time( self ):
    return self.supervisor.time

  # set the outputs of the supervisor
  def set_outputs( self, v, omega ):
    self.supervisor.v_output = v
    self.supervisor.omega_output = omega
