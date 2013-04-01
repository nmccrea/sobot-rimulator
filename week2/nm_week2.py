#!/usr/bin/python
# -*- Encoding: utf-8 -*
# Python implementation of the Week 2 exercise.

from math import *



# Khepera3 Properties (copied from Sim.I.Am)
K3_WHEEL_RADIUS = 0.021         # meters
K3_WHEEL_BASE_LENGTH = 0.0885   # meters
K3_SPEED_FACTOR = 6.2953e-6     
K3_TRANS_VEL_LIMIT = 0.3148     # m/s
K3_ANG_VEL_LIMIT = 2.2763       # rad/s



class Pose:

  def __init__( self, x, y, phi ):
    self.x = x
    self.y = y
    self.phi = phi




class DifferentialDriveDynamics:
  
  def __init__( self, wheel_radius, wheel_base_length):
    self.wheel_radius = wheel_radius
    self.wheel_base_length = wheel_base_length
    
  def uni_to_diff( self, v, w ):
    # v = translational velocity (m/s)
    # w = angular velocity (rad/s)
    
    R = self.wheel_radius
    L = self.wheel_base_length
    
    v_l = ( (2.0 * v) - (w*L) ) / (2.0 * R)
    v_r = ( (2.0 * v) + (w*L) ) / (2.0 * R)
    
    return v_l, v_r
    
  def diff_to_uni( self, v_l, v_r ):
    # v_l = left-wheel angular velocity (rad/s)
    # v_r = right-wheel angular velocity (rad/s)
    
    R = self.wheel_radius
    L = self.wheel_base_length
    
    v = ( R / 2.0 ) * ( v_r + v_l )
    w = ( R / L ) * ( v_r - v_l )
    
    return v, w
  
  def apply_dynamics( self, old_pose, v_l, v_r, d_t ):
    wheel_meters_per_rad = self.wheel_radius
    
    # calculate the distance traveled
    d_left_wheel = d_t * v_l * wheel_meters_per_rad
    d_right_wheel = d_t * v_r * wheel_meters_per_rad
    d_center = ( d_left_wheel + d_right_wheel ) / 2.0
    
    # calculate the new pose
    old_x = old_pose.x
    old_y = old_pose.y
    old_phi = old_pose.phi
    
    new_x = old_x + ( d_center * cos( old_phi ) )
    new_y = old_y + ( d_center * sin( old_phi ) )
    new_phi = old_phi + ( ( d_right_wheel - d_left_wheel ) / self.wheel_base_length )
    # normalize phi:
    if new_phi > pi:
      new_phi -= 2*pi
    elif new_phi < -pi:
      new_phi += 2*pi
    
    # package and return the new pose
    new_pose = Pose( new_x, new_y, new_phi )
    return new_pose




class Robot: # Khepera3 robot 
  
  def __init__( self ):
    # wheel arrangement:
    self.wheel_radius = K3_WHEEL_RADIUS             # meters
    self.wheel_base_length = K3_WHEEL_BASE_LENGTH   # meters
    
    # wheel speed factor
    self.speed_factor = K3_SPEED_FACTOR
    
    # dynamics
    self.dynamics = DifferentialDriveDynamics( self.wheel_radius, self.wheel_base_length )
    
    ## initialize state
    # set wheel rotations (rad/sec)
    self.left_wheel_rotation = 0.0
    self.right_wheel_rotation = 0.0
    
    # set pose
    self.pose = Pose( 0.0, 0.0, 0.0 )
    
  def update_state( self, dt ):
    pose = self.pose
    v_l = self.left_wheel_rotation
    v_r = self.right_wheel_rotation
    
    self.pose = self.dynamics.apply_dynamics( pose, v_l, v_r, dt )
    
  
  def set_wheel_rotations( self, v_l, v_r ):
    # limit the speeds:
    v, w = self.dynamics.diff_to_uni( v_l, v_r )
    v = max( min( v, K3_TRANS_VEL_LIMIT ), -K3_TRANS_VEL_LIMIT )
    w = max( min( w, K3_ANG_VEL_LIMIT ), -K3_ANG_VEL_LIMIT )
    v_l, v_r = self.dynamics.uni_to_diff( v, w )
    
    # set rotations
    self.left_wheel_rotation = v_l
    self.right_wheel_rotation = v_r
  
  def wheel_rotations( self ):
    return self.left_wheel_rotation, self.right_wheel_rotation
  
  
  

import Euv.EuvGtk as Euv
import Euv.Frame as Frame
import Euv.Shapes as Shapes
import Euv.Color as Color
class WorldView:

  def __init__( self ):
    # create viewer
    self.viewer = Euv.Viewer( size = (300, 300),
                          view_port_center = (0, 0),
                          view_port_width = 3,
                          flip_y = True )

    # initialize the current frame object
    self.current_frame = Frame.Frame()

    # initialize list of robots views
    self.robot_views = []

  def add_robot( self, robot ):
    robot_view = RobotView( self.viewer, robot )
    self.robot_views.append( robot_view )

  def render_frame( self ):
    # draw all the robots
    for robot_view in self.robot_views:
      robot_view.draw_robot_to_frame( self.current_frame )

    # cycle the frame
    self.viewer.add_frame( self.current_frame )   # push the current frame
    self.current_frame = Frame.Frame()            # prepare the next frame

  def wait( self ):
    self.viewer.wait()




class RobotView:
  
  def __init__( self, viewer, robot ):
    self.viewer = viewer
    self.robot = robot

  def draw_robot_to_frame( self, frame ):
    # grab robot pose values
    robot_pose = self.robot.pose
    robot_x = robot_pose.x
    robot_y = robot_pose.y
    robot_phi = robot_pose.phi
    
    # build the robot
    robot_body = Shapes.arrow_head_polygon( (robot_x, robot_y),
                                            robot_phi,
                                            scale = 0.02 )
    robot_wheels = Shapes.rectangle_pair( (robot_x, robot_y),
                                          5.0, 2.0, 7.0,
                                          angle = robot_phi,
                                          scale = 0.02 )

    # add the robot to the frame
    frame.add_polygons( [ robot_body ],
                        color = "red",
                        alpha = 0.5 )
    frame.add_polygons( robot_wheels,
                        color = "black",
                        alpha = 0.5 )




import time
class World:

  def __init__( self ):
    # initialize world time
    self.world_time = 0.0 # seconds
    self.dt = 0.1         # seconds
    
    # initialize robots
    self.robots = []

  def add_robot( self, robot ):
    self.robots.append( robot )

  def tick( self ):
    dt = self.dt
    
    # update all the robots
    for robot in self.robots:
      robot.update_state( dt )
    
    # increment world time
    self.world_time += dt
    # pause the simulation for a moment
    time.sleep( dt )




class Week2Simulator:

  def __init__( self ):
    # create the simulation world
    self.world = World()
    self.world_view = WorldView()
    
    # create the robot
    self._add_robot( Robot() )
    
    # run the simulation
    self.run_sim()

  def run_sim( self ):
    # loop the simulation
    # TODO make the loop condition smart
    while self.world.world_time < 5:
      # render the current state
      self.world_view.render_frame()
      
      # increment the simulation
      self.world.tick()
    
    self.world_view.wait()

  def _add_robot( self, robot ):
    self.world.add_robot( robot )
    self.world_view.add_robot( robot )
