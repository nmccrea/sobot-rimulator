#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
from utils import linalg2_util as linalg
from go_to_angle_controller import *
from pose import *
from sim_exceptions.goal_reached_exception import *

class Supervisor:

  def __init__( self, robot_interface,
                      wheel_radius,
                      wheel_base_length,
                      wheel_encoder_ticks_per_rev,
                      goal = [ 0.0, 0.0 ],
                      d_stop = 0.05,
                      initial_pose = Pose( 0.0, 0.0, 0.0) ):

    # robot representation
    # NOTE: the supervisor does NOT have access to the physical robot, only the robot's interface
    self.robot = robot_interface

    # odometry information
    self.robot_wheel_radius = wheel_radius
    self.robot_wheel_base_length = wheel_base_length
    self.wheel_encoder_ticks_per_revolution = wheel_encoder_ticks_per_rev
    self.prev_ticks_left = 0
    self.prev_ticks_right = 0

    # controllers
    self.controllers = [ GoToAngleController() ]
    self.current_controller = self.controllers[0]

    # goal
    self.goal = goal
    self.d_stop = d_stop

    # state estimate
    self.estimated_pose = initial_pose

  # execute one control loop
  def execute( self ):
    if linalg.distance( self.estimated_pose.vposition(), self.goal ) < self.d_stop:
      raise GoalReachedException()

    # run odometry calculations to get updated pose estimate
    self.update_odometry()

    # execute the current controller's control loop

    # TODO: establish controller-agnostic algorithm here
    vect_to_goal = linalg.sub( self.goal, self.estimated_pose.vunpack()[0] )
    theta_d = atan2( vect_to_goal[1], vect_to_goal[0] )
    omega = self.current_controller.execute( self.estimated_pose, theta_d )
    v = 0.5
    self.robot.set_unicycle_motion( v, omega )

  # update the estimated position of the robot using it's wheel encoder readings
  def update_odometry( self ):
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
