#!/usr/bin/python
# -*- Encoding: utf-8 -*

# wall-following directions
FWDIR_LEFT = 0
FWDIR_RIGHT = 1

from math import *

from utils import linalg2_util as linalg
from sim_exceptions.goal_reached_exception import *

class FollowWallController:

  def __init__( self, supervisor ):
    # bind the supervisor
    self.supervisor = supervisor

    # sensor placements
    self.proximity_sensor_placements = supervisor.proximity_sensor_placements()

    # follow direction
    self.follow_direction = FWDIR_LEFT

    # control gains
    self.kP = 10.0
    self.kI = 0.0
    self.kD = 0.0
    
    # stored values - for computing next results
    self.prev_time = 0.0
    self.prev_eP = 0.0
    self.prev_eI = 0.0

    # additional calculated values
    self.fw_heading_vector = [ 0.0, 0.0 ]

  def execute( self ):
    # generate and store new heading vector
    self.fw_heading_vector = self.calculate_fw_heading_vector()

    # calculate the time that has passed since the last control iteration
    current_time = self.supervisor.time()
    dt = current_time - self.prev_time

    # calculate the error terms
    theta_d = atan2( self.fw_heading_vector[1], self.fw_heading_vector[0] )
    eP = theta_d
    eI = self.prev_eI + eP*dt
    eD = ( eP - self.prev_eP ) / dt

    # calculate angular velocity
    omega = self.kP * eP + self.kI * eI + self.kD * eD
    
    # calculate translational velocity
    # velocity is v_max when omega is 0,
    # drops rapidly to zero as |omega| rises
    v = self.supervisor.v_max() / ( abs( omega ) + 1 )**1.5

    # store values for next control iteration
    self.prev_time = current_time
    self.prev_eP = eP
    self.prev_eI = eI

    self.supervisor.set_outputs( v, omega )

    # === FOR DEBUGGING ===
    # self._print_vars( eP, eI, eD, v, omega )

  # return a wall-following vector in the robot's reference frame
  def calculate_fw_heading_vector( self ):
    # NOTE: preexisting knowledge of the how the sensors are stored and indexed used extensively here

    # estimate wall surface:

    # get the working set of sensor information for the side we are bearing on
    # the working set is the sensors on the bearing side, indexed from front to back on the robot
    if self.follow_direction == FWDIR_LEFT:
      sensor_placements = self.proximity_sensor_placements[4:8]
      sensor_distances = self.supervisor.proximity_sensor_distances()[4:8]
    elif self.follow_direction == FWDIR_RIGHT:
      sensor_placments = self.proximity_sensor_placments[3::-1]
      sensor_distances = self.supervisor.proximity_sensor_distances()[3::-1]
    else:
      raise Exception( "unknown wall-following direction" )


    # get the smallest sensor distances
    d1, d2 = sorted( sensor_distances )[0:2]

    # identify the sensors giving these values
    i1 = sensor_distances.index( d1 )
    i2 = sensor_distances.index( d2 )
    
    # calculate the vectors to the obstacle in the robot's reference frame
    sensor1_pos, sensor1_theta = sensor_placements[i1].vunpack()
    sensor2_pos, sensor2_theta = sensor_placements[i2].vunpack()
    v1, v2 = [ d1, 0.0 ], [ d2, 0.0 ]
    v1 = linalg.rotate_and_translate_vector( v1, sensor1_theta, sensor1_pos )
    v2 = linalg.rotate_and_translate_vector( v2, sensor2_theta, sensor2_pos )

    # ensure correct orientation by determining which is the forwardmost sensor reading
    if i2 < i1: v1, v2 = v2, v1 # swap the vectors

    wall_surface_vector = linalg.sub( v1, v2 )

    return [ 0.0, 0.0 ]  # TODO: fix this


  def _print_vars( self, eP, eI, eD, v, omega ):
    print "\n\n"
    print "=============="
    print "ERRORS:"
    print "eP: " + str( eP )
    print "eI: " + str( eI )
    print "eD: " + str( eD )
    print ""
    print "CONTROL COMPONENTS:"
    print "kP * eP = " + str( self.kP ) + " * " + str( eP )
    print "= " + str( self.kP * eP )
    print "kI * eI = " + str( self.kI ) + " * " + str( eI )
    print "= " + str( self.kI * eI )
    print "kD * eD = " + str( self.kD ) + " * " + str( eD )
    print "= " + str( self.kD * eD )
    print ""
    print "OUTPUTS:"
    print "omega: " + str( omega )
    print "v    : " + str( v )
