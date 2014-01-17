# Sobot Rimulator - A Robot Programming Tool
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Email mccrea.engineering@gmail.com for questions, comments, or to report bugs.





# wall-following directions
FWDIR_LEFT = 0
FWDIR_RIGHT = 1

from math import *

from models.control_state import *
from utils import linalg2_util as linalg
from sim_exceptions.goal_reached_exception import *

class FollowWallController:

  def __init__( self, supervisor ):
    # bind the supervisor
    self.supervisor = supervisor

    # sensor placements
    self.proximity_sensor_placements = supervisor.proximity_sensor_placements()

    # wall-follow parameters
    self.follow_distance = 0.15 # meters from the center of the robot to the wall

    # control gains
    self.kP = 10.0
    self.kI = 0.0
    self.kD = 0.0
    
    # stored values - for computing next results
    self.prev_time = 0.0
    self.prev_eP = 0.0
    self.prev_eI = 0.0

    # key vectors and data (initialize to any non-zero vector)
    self.l_wall_surface =             [ [ 1.0, 0.0 ], [ 1.0, 0.0 ] ]  # the followed surface, in robot space
    self.l_parallel_component =       [ 1.0, 0.0 ]
    self.l_perpendicular_component =  [ 1.0, 0.0 ]
    self.l_distance_vector =          [ 1.0, 0.0 ]
    self.l_fw_heading_vector =        [ 1.0, 0.0 ]

    self.r_wall_surface =             [ [ 1.0, 0.0 ], [ 1.0, 0.0 ] ]  # the followed surface, in robot space
    self.r_parallel_component =       [ 1.0, 0.0 ]
    self.r_perpendicular_component =  [ 1.0, 0.0 ]
    self.r_distance_vector =          [ 1.0, 0.0 ]
    self.r_fw_heading_vector =        [ 1.0, 0.0 ]

  def update_heading( self ):
    # generate and store new heading vector and critical points for following to the left
    [
      self.l_fw_heading_vector,
      self.l_parallel_component,
      self.l_perpendicular_component,
      self.l_distance_vector,
      self.l_wall_surface
                        ] = self.calculate_fw_heading_vector( FWDIR_LEFT )
    # generate and store new heading vector and critical points for following to the right
    [
      self.r_fw_heading_vector,
      self.r_parallel_component,
      self.r_perpendicular_component,
      self.r_distance_vector,
      self.r_wall_surface
                        ] = self.calculate_fw_heading_vector( FWDIR_RIGHT )

  def execute( self ):
    # determine which direction to slide in
    current_state = self.supervisor.current_state()
    if current_state == ControlState.SLIDE_LEFT:      heading_vector = self.l_fw_heading_vector
    elif current_state == ControlState.SLIDE_RIGHT:   heading_vector = self.r_fw_heading_vector
    else: raise Exception( "applying follow-wall controller when not in a sliding state currently not supported" )

    # calculate the time that has passed since the last control iteration
    current_time = self.supervisor.time()
    dt = current_time - self.prev_time

    # calculate the error terms
    theta_d = atan2( heading_vector[1], heading_vector[0] )
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
  def calculate_fw_heading_vector( self, follow_direction ):

    # get the necessary variables for the working set of sensors
    #   the working set is the sensors on the side we are bearing on, indexed from rearmost to foremost on the robot
    #   NOTE: uses preexisting knowledge of the how the sensors are stored and indexed
    if follow_direction == FWDIR_LEFT:
      # if we are following to the left, we bear on the righthand sensors
      sensor_placements = self.proximity_sensor_placements[7:3:-1]
      sensor_distances = self.supervisor.proximity_sensor_distances()[7:3:-1]
      sensor_detections = self.supervisor.proximity_sensor_positive_detections()[7:3:-1]
    elif follow_direction == FWDIR_RIGHT:
      # if we are following to the right, we bear on the lefthand sensors
      sensor_placements = self.proximity_sensor_placements[:4]
      sensor_distances = self.supervisor.proximity_sensor_distances()[:4]
      sensor_detections = self.supervisor.proximity_sensor_positive_detections()[:4]
    else:
      raise Exception( "unknown wall-following direction" )

    if True not in sensor_detections:
      # if there is no wall to track detected, we default to predefined reference points
      # NOTE: these points are designed to turn the robot towards the bearing side, which aids with cornering behavior
      #       the resulting heading vector is also meant to point close to directly aft of the robot
      #       this helps when determining switching conditions in the supervisor state machine
      p1 = [ -0.2, 0.0 ]
      if follow_direction == FWDIR_LEFT: p2 = [ -0.2, -0.0001 ]
      if follow_direction == FWDIR_RIGHT: p2 = [ -0.2, 0.0001 ]
    else:
      # sort the sensor distances along with their corresponding indices
      sensor_distances, indices = zip( *sorted( zip( # this method ensures two different sensors are always used
                                      sensor_distances, # sensor distances
                                      [0, 1, 2, 3]      # corresponding indices
                                    ) ) )
      # get the smallest sensor distances and their corresponding indices
      d1, d2 = sensor_distances[0:2]
      i1, i2 = indices[0:2]
      
      # calculate the vectors to the obstacle in the robot's reference frame
      sensor1_pos, sensor1_theta = sensor_placements[i1].vunpack()
      sensor2_pos, sensor2_theta = sensor_placements[i2].vunpack()                
      p1, p2 = [ d1, 0.0 ], [ d2, 0.0 ]
      p1 = linalg.rotate_and_translate_vector( p1, sensor1_theta, sensor1_pos )
      p2 = linalg.rotate_and_translate_vector( p2, sensor2_theta, sensor2_pos )

      # ensure p2 is forward of p1
      if i2 < i1: p1, p2 = p2, p1
    
    # compute the key vectors and auxiliary data
    l_wall_surface = [ p2, p1 ]
    l_parallel_component = linalg.sub( p2, p1 ) 
    l_distance_vector = linalg.sub( p1, linalg.proj( p1, l_parallel_component ) )
    unit_perp = linalg.unit( l_distance_vector )
    distance_desired = linalg.scale( unit_perp, self.follow_distance )
    l_perpendicular_component = linalg.sub( l_distance_vector, distance_desired )
    l_fw_heading_vector = linalg.add( l_parallel_component, l_perpendicular_component )

    return l_fw_heading_vector, l_parallel_component, l_perpendicular_component, l_distance_vector, l_wall_surface

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
