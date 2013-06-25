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

    # follow distance
    self.follow_distance = 0.15 # meters

    # control gains
    self.kP = 10.0
    self.kI = 0.0
    self.kD = 0.0
    
    # stored values - for computing next results
    self.prev_time = 0.0
    self.prev_eP = 0.0
    self.prev_eI = 0.0

    # additional calculated values
    self.wall_surface = [ [ 0.0, 0.0 ], [ 0.0, 0.0 ] ]
    self.robot_to_wall_vector = [ 0.0, 0.0 ]
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

    # ESTIMATE WALL SURFACE:

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
    p1, p2 = [ d1, 0.0 ], [ d2, 0.0 ]
    p1 = linalg.rotate_and_translate_vector( p1, sensor1_theta, sensor1_pos )
    p2 = linalg.rotate_and_translate_vector( p2, sensor2_theta, sensor2_pos )

    # ensure correct orientation by determining which is the forwardmost sensor reading
    if i2 < i1: p1, p2 = p2, p1 # swap the vectors

    self.wall_surface = [ p1, p2 ]  # TODO: fix this

    wall_surface_vector = linalg.sub( p1, p2 )

    if linalg.mag( wall_surface_vector ) == 0.0:  # TODO: fix this
      p1 = [ 1.0, 0.0 ]
      p2 = [ 0.0, 0.0 ]
      wall_surface_vector = [ 1.0, 0.0 ]
      

    # ESTIMATE ROBOT-TO-WALL VECTOR
    
    # compute the vector from the robot center to the nearest point on the wall surface
    robot_to_wall_vector = linalg.sub(  p1,
                                        linalg.proj(  p1,
                                                      linalg.sub( p1, p2 ) ) )
    # # this alternative formula is closer to that given in the Coursera course manual, but the result is the same
    # wall_surface_vector_unit = linalg.unit( wall_surface_vector )
    # robot_to_wall_vector = linalg.sub(  p1,
    #                                     linalg.scale( wall_surface_vector_unit,
    #                                                   linalg.dot( p1, wall_surface_vector_unit ) ) )
    
    self.robot_to_wall_vector = robot_to_wall_vector

    # COMBINE THE TWO COMPONENT VECTORS INTO A HEADING VECTOR

    if linalg.mag( robot_to_wall_vector ) == 0.0:
      fw_heading_vector = [ 1.0, 0.0 ]
    else:
      fw_heading_vector = linalg.add( linalg.unit(  wall_surface_vector ),
                                                   linalg.sub( robot_to_wall_vector,
                                                               linalg.scale( linalg.unit( robot_to_wall_vector ), self.follow_distance ) ) )

    return linalg.unit( fw_heading_vector )  # TODO: fix this


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
