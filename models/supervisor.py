#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

from utils import linalg2_util as linalg
from pose import *
from sim_exceptions.goal_reached_exception import *
from supervisor_controller_interface import *
from supervisor_state_machine import *

from controllers.avoid_obstacles_controller import *
from controllers.go_to_angle_controller import *
from controllers.go_to_goal_controller import *
from controllers.gtg_and_ao_controller import *

# control parameters
K3_TRANS_VEL_LIMIT = 0.3148     # m/s
K3_ANG_VEL_LIMIT = 2.2763       # rad/s
D_STOP = 0.05                   # meters from goal

class Supervisor:

  def __init__( self, robot_interface,                        # the interface through which this supervisor will interact with the robot
                      wheel_radius,                           # the radius of a drive wheel on the robot
                      wheel_base_length,                      # the robot's wheel base
                      wheel_encoder_ticks_per_rev,            # the number of wheel encoder ticks per revolution of a drive wheel
                      sensor_placements,                      # placement pose of the sensors on the robot body
                      goal = [ 0.0, 0.0 ],                    # the goal to which this supervisor will guide the robot
                      initial_pose = Pose( 0.0, 0.0, 0.0) ):  # the pose the robot will have when control begins
    
    # internal clock time in seconds
    self.time = 0.0

    # robot representation
    # NOTE: the supervisor does NOT have access to the physical robot, only the robot's interface
    self.robot = robot_interface

    # proximity sensor placement poses
    self.proximity_sensor_placements = [ Pose( rawpose[0], rawpose[1], radians( rawpose[2] ) ) for rawpose in sensor_placements ]

    # odometry information
    self.robot_wheel_radius = wheel_radius
    self.robot_wheel_base_length = wheel_base_length
    self.wheel_encoder_ticks_per_revolution = wheel_encoder_ticks_per_rev
    self.prev_ticks_left = 0
    self.prev_ticks_right = 0

    # controllers
    controller_interface = SupervisorControllerInterface( self )
    self.go_to_angle_controller = GoToAngleController( controller_interface )
    self.go_to_goal_controller = GoToGoalController( controller_interface )
    self.avoid_obstacles_controller = AvoidObstaclesController( controller_interface )
    self.gtg_and_ao_controller = GTGAndAOController( controller_interface )

    # state machine
    self.state_machine = SupervisorStateMachine( self )

    # state
    self.proximity_sensor_distances = [ 0.0, 0.0 ] * len( sensor_placements ) # sensor distances
    self.estimated_pose = initial_pose                                        # estimated pose
    self.current_controller = self.gtg_and_ao_controller                      # current controller

    # goal
    self.goal = goal

    # control bounds
    self.v_max = K3_TRANS_VEL_LIMIT
    self.omega_max = K3_ANG_VEL_LIMIT

    # CONTROL OUTPUTS - UNICYCLE
    self.v_output = 0.0
    self.omega_output = 0.0
  
  # simulate this supervisor running for one time increment
  def step( self, dt ):
    # increment the internal clock time
    self.time += dt

    # NOTE: for simplicity, we assume that the onboard computer executes exactly one control loop for every simulation time increment
    # although technically this is not likely to be realistic, it is a good simplificiation

    # execute one full control loop
    self.execute()

  # execute one control loop
  def execute( self ):
    if linalg.distance( self.estimated_pose.vposition(), self.goal ) < D_STOP:
      raise GoalReachedException()

    self._update_state()              # update state
    self.current_controller.execute() # execute the controller's control loop
    self._send_robot_commands()       # output the generated control signals to the robot

  # current controller indicator methods
  def currently_gtg( self ): return self.current_controller == self.go_to_goal_controller
  def currently_ao( self ): return self.current_controller == self.avoid_obstacles_controller
  def currently_blended( self ): return self.current_controller == self.gtg_and_ao_controller

  # update the estimated robot state and the control state
  def _update_state( self ):
    # update estimated robot state from sensor readings
    self._update_proximity_sensor_distances()
    self._update_odometry()

    # update the control state
    self.state_machine.update_state()
  
  # update the distances indicated by the proximity sensors
  def _update_proximity_sensor_distances( self ):
    self.proximity_sensor_distances = [ 0.02-( log(readval/3960.0) )/30.0
                                        for readval in self.robot.read_proximity_sensors() ]

  # update the estimated position of the robot using it's wheel encoder readings
  def _update_odometry( self ):
    R = self.robot_wheel_radius
    N = float( self.wheel_encoder_ticks_per_revolution )

    # read the wheel encoder values
    ticks_left, ticks_right = self.robot.read_wheel_encoders()

    # get the difference in ticks since the last iteration
    d_ticks_left = ticks_left - self.prev_ticks_left
    d_ticks_right = ticks_right - self.prev_ticks_right
    
    # estimate the wheel movements
    d_left_wheel = 2*pi*R*( d_ticks_left / N )
    d_right_wheel = 2*pi*R*( d_ticks_right / N )
    d_center = 0.5 * ( d_left_wheel + d_right_wheel )

    # calculate the new pose
    prev_x, prev_y, prev_theta = self.estimated_pose.sunpack()
    new_x = prev_x + ( d_center * cos( prev_theta ) )
    new_y = prev_y + ( d_center * sin( prev_theta ) )
    new_theta = prev_theta + ( ( d_right_wheel - d_left_wheel ) / self.robot_wheel_base_length )

    # update the pose estimate with the new values
    self.estimated_pose.supdate( new_x, new_y, new_theta )

    # save the current tick count for the next iteration
    self.prev_ticks_left = ticks_left
    self.prev_ticks_right = ticks_right

  # generate and send the correct commands to the robot
  def _send_robot_commands( self ):
    # limit the speeds:
    v = max( min( self.v_output, self.v_max ), -self.v_max )
    omega = max( min( self.omega_output, self.omega_max ), -self.omega_max )

    # send the drive commands to the robot
    v_l, v_r = self._uni_to_diff( v, omega )
    self.robot.set_wheel_drive_rates( v_l, v_r )

  def _uni_to_diff( self, v, omega ):
    # v = translational velocity (m/s)
    # omega = angular velocity (rad/s)
    
    R = self.robot_wheel_radius
    L = self.robot_wheel_base_length
    
    v_l = ( (2.0 * v) - (omega*L) ) / (2.0 * R)
    v_r = ( (2.0 * v) + (omega*L) ) / (2.0 * R)
    
    return v_l, v_r
    
  def _diff_to_uni( self, v_l, v_r ):
    # v_l = left-wheel angular velocity (rad/s)
    # v_r = right-wheel angular velocity (rad/s)
    
    R = self.robot_wheel_radius
    L = self.robot_wheel_base_length
    
    v = ( R / 2.0 ) * ( v_r + v_l )
    omega = ( R / L ) * ( v_r - v_l )
    
    return v, omega
