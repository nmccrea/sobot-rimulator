#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
from pose import *

class Supervisor:

  def __init__( self, robot,
                      initial_pose = Pose( 0.0, 0.0, 0.0) ):
    # robot
    self.robot = robot
    self.robot_wheel_radius = robot.wheel_radius
    self.robot_wheel_base_length = robot.wheel_base_length

    # odometry information
    self.wheel_encoder_ticks_per_revolution = robot.left_wheel_encoder.ticks_per_rev
    self.prev_ticks_left = 0
    self.prev_ticks_right = 0

    # state estimate
    self.estimated_pose = initial_pose

  # execute one control loop
  def execute( self ):
    # run odometry calculations to get updated pose estimate
    self.update_odometry()

  # update the estimated position of the robot using it's wheel encoder readings
  def update_odometry( self ):
    R = self.robot_wheel_radius
    N = float( self.wheel_encoder_ticks_per_revolution )

    # read the wheel encoder values
    wheel_encoder_readings = self.robot.read_wheel_encoders()
    ticks_left, ticks_right = wheel_encoder_readings[0], wheel_encoder_readings[1]

    # get the difference in ticks since the last iterationi
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
