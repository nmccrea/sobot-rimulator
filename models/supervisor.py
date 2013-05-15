#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
from go_to_angle_controller import *
from pose import *

class Supervisor:

  def __init__( self, proximity_sensors,
                      wheel_encoders,
                      wheel_radius,
                      wheel_base_length,
                      initial_pose = Pose( 0.0, 0.0, 0.0) ):
    # robot representation
    # NOTE: the supervisor does NOT have access to the robot, only the robot's sensor output
    self.robot_wheel_radius = wheel_radius
    self.robot_wheel_base_length = wheel_base_length
    self.robot_wheel_encoders = wheel_encoders
    self.robot_proximity_sensors = proximity_sensors

    # odometry information
    self.wheel_encoder_ticks_per_revolution = wheel_encoders[0].ticks_per_rev
    self.prev_ticks_left = 0
    self.prev_ticks_right = 0

    # controllers
    self.controllers = [ GoToAngleController() ]
    self.current_controller = self.controllers[0]

    # goal
    self.goal = [ -1.0, 1.3 ]

    # state estimate
    self.estimated_pose = initial_pose

  # execute one control loop
  def execute( self ):
    # run odometry calculations to get updated pose estimate
    self.update_odometry()

    # execute the current controller's control loop
    self.current_controller.execute( self.estimated_pose )
  
  # read the proximity sensors
  def read_proximity_sensors( self ):
    return [ s.read() for s in self.robot_proximity_sensors ]

  # read the wheel encoders
  def read_wheel_encoders( self ):
    return [ e.read() for e in self.robot_wheel_encoders ]

  # update the estimated position of the robot using it's wheel encoder readings
  def update_odometry( self ):
    R = self.robot_wheel_radius
    N = float( self.wheel_encoder_ticks_per_revolution )

    # read the wheel encoder values
    ticks_left, ticks_right = self.read_wheel_encoders()

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
