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

    # follow parameters
    self.follow_direction = FWDIR_LEFT
    self.follow_distance = 0.1 # meters

    # control gains
    self.kP = 10.0
    self.kI = 0.0
    self.kD = 0.0
    
    # stored values - for computing next results
    self.prev_time = 0.0
    self.prev_eP = 0.0
    self.prev_eI = 0.0

    # additional calculated values
    self.wall_surface =             [ [ 0.0, 0.0 ], [ 0.0, 0.0 ] ]  # the followed surface, in robot space
    self.parallel_component =       [ 0.0, 0.0 ]
    self.perpendicular_component =  [ 0.0, 0.0 ]
    self.fw_heading_vector =        [ 0.0, 0.0 ]

  def execute( self ):
    # generate and store new heading vector and critical points
    self.fw_heading_vector, self.parallel_component, self.perpendicular_component, self.wall_surface = self.calculate_fw_heading_vector()

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
    v = self.supervisor.v_max() / ( abs( omega ) + 1 )**0.7

    # store values for next control iteration
    self.prev_time = current_time
    self.prev_eP = eP
    self.prev_eI = eI

    self.supervisor.set_outputs( v, omega )

    # === FOR DEBUGGING ===
    # self._print_vars( eP, eI, eD, v, omega )

  # return a wall-following vector in the robot's reference frame
  # also returns the component vectors used to calculate the heading
  # and the vectors representing the followed surface in robot-space
  def calculate_fw_heading_vector( self ):

    # get the necessary variables for the working set of sensors
    #   the working set is the sensors on the side we are bearing on, indexed from rearmost to foremost on the robot
    #   NOTE: uses preexisting knowledge of the how the sensors are stored and indexed
    if self.follow_direction == FWDIR_LEFT:

      # if we are following to the left, we bear on the righthand sensors
      sensor_placements = self.proximity_sensor_placements[7:3:-1]
      sensor_distances = self.supervisor.proximity_sensor_distances()[7:3:-1]
    elif self.follow_direction == FWDIR_RIGHT:

      # if we are following to the right, we bear on the lefthand sensors
      sensor_placements = self.proximity_sensor_placements[:4]
      sensor_distances = self.supervisor.proximity_sensor_distances()[:4]
    else:
      raise Exception( "unknown wall-following direction" )

    # sort the sensor distances along with their corresponding indices
    sensor_distances, indices = zip( *sorted( zip( # this method ensures two different sensors are always used
                                    sensor_distances, # sensor distances
                                    [0, 1, 2, 3]      # corresponding indices
                                  ) ) )
    # get the smallest sensor distances and their corresponding indices
    d1, d2 = sensor_distances[0:2]
    i1, i2 = indices[0:2]
    
    # calculate the vectors to the obstacle in the robot's reference frame
    sensor1_pos, sensor1_theta = sensor_placements[i1].vunpack()  # the indices are used here to get the correct placements
    sensor2_pos, sensor2_theta = sensor_placements[i2].vunpack()                
    p1, p2 = [ d1, 0.0 ], [ d2, 0.0 ]
    p1 = linalg.rotate_and_translate_vector( p1, sensor1_theta, sensor1_pos )   # p1 is the nearest point measured
    p2 = linalg.rotate_and_translate_vector( p2, sensor2_theta, sensor2_pos )   # p2 is the second nearest point measured

    
    if i2 < i1: p1, p2 = p2, p1 # ensure correct orientation by determining which is the forwardmost sensor reading
    
    # compute the parallel and perpendicular component vectors
    parallel_component = linalg.sub( p2, p1 ) 
    perpendicular_component = linalg.sub( p1, linalg.proj( p1, parallel_component ) )

    perp_vector = linalg.sub( perpendicular_component,
                              linalg.scale( linalg.unit( perpendicular_component ), self.follow_distance ) )
    perp_vector = linalg.scale( perp_vector, 250*linalg.mag(perp_vector)**2 )

    fw_heading_vector = linalg.add( parallel_component,
                                    perp_vector )

    return fw_heading_vector, parallel_component, perp_vector, [ p2, p1 ]


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
