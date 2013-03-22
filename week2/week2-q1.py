#!/usr/bin/python
# -*- Encoding: utf-8 -*
# Python implementation of the Week 2 exercise.
#
# Dov Grobgeld <dov.grobgeld@gmail.com>
# 2013-02-05 Tue

from math import *
import Euv.Frame as Frame
import Euv.EuvGtk as Euv
import Euv.Color as Color
import Euv.Shapes as Shapes
import time

# Constants for encoder arrays
LEFT = 0
RIGHT = 1

def len2(x,y):
  return x**2+y**2

def normalize_angle(theta):
  return atan2(sin(theta),cos(theta))

class State:
  """The state (pose) of the robot"""
  def __init__(self,x,y,phi):
    self.x = x
    self.y = y
    self.phi = phi

  def get_pose(self):
    return self.x,self.y,self.phi

  def set_pose(self,x,y,phi):
    self.x,self.y,self.phi = x,y,phi

class WheelEncoder:
  """An wheel encoder with descrete ticks"""
  def __init__(self,
               radius,
               length,
               ticks_per_rev=1000):
    self.radius = radius
    self.length = length
    self.ticks_per_rev = ticks_per_rev
    self.ticks = 0

  def update_ticks(self,
                   angular_velocity,
                   dt):
    self.ticks += self.distance_to_ticks(angular_velocity * dt)

  def reset_ticks(self):
    self.ticks = 0

  def distance_to_ticks(self, distance):
    return ceil((distance*self.ticks_per_rev)/(2*pi))

  def ticks_to_distance(self, ticks):
    return (ticks*2*pi)/self.ticks_per_rev

  def get_ticks(self):
    return self.ticks

  def get_ticks_per_rev(self):
    return self.ticks_per_rev

class Robot:
  """The robot model contains two differential wheels"""
  def __init__(self,
               axis_length,
               wheel_radius,
               viewer=None,
               init=None,
               goal=None,
               ticks_per_rev = 50,
               initial_state = State(0,0,0)   # Estimated state of robot
               ):
    self.axis_length = axis_length  # L
    self.wheel_radius = wheel_radius  # R
    self.viewer = viewer
    self.path = []
    self.time = 0
    self.init = init
    self.goal = goal
    self.state = initial_state
    self.left_encoder = WheelEncoder(wheel_radius,axis_length,ticks_per_rev)
    self.right_encoder = WheelEncoder(wheel_radius,axis_length,ticks_per_rev)
    
  def uni_to_diff(self,
                  velocity,
                  rotation_speed):
    """Translate from unicycle dynamicls to differential
    drive dynamics"""
    L = self.axis_length
    R = self.wheel_radius
    w = rotation_speed
    v = velocity
    v_l = 1.0*(2*v-w*L)/(2*R)
    v_r = 1.0*(2*v+w*L)/(2*R)
    return v_l,v_r
    
  def diff_to_uni(self,
                  velocity_left,
                  velocity_right):
    """Translate from differential drive angular velocities to
    unicycle velocity and direction."""
    L = self.axis_length
    R = self.wheel_radius
    v_l = velocity_left                 
    v_r = velocity_right
    v = 1.0*R/2*(v_r + v_l)
    w = 1.0*R/L*(v_r - v_l)
    return v,w

  def set_pose(self,x,y,phi):
    self.state.set_pose(x,y,phi)
    self.path = [(x,y)]  # Reset the path

  def set_wheel_speeds(self, velocity_left, velocity_right):
    self.velocity_left = velocity_left
    self.velocity_right = velocity_right

  def draw_robot(self, draw_path=True, text_info=''):
    """Create a new frame and draw a representation of the robot in it"""
    x,y,phi = self.state.get_pose()
    phi_d = self.get_dir_to_goal()
    if self.viewer:
      f = Frame.Frame()
      if draw_path:
        f.add_lines(color=Color.Color("black"),
                    lines=[self.path[:]],
                    linewidth=0.01)
      
      # Draw start and goal
      for p,color in ( (self.init, "green"),
                       (self.goal, "blue") ):
        if p:
          f.add_circle(p,
                       color=color,
                       alpha=0.5,
                       radius=0.05)

      # Our robot representation is built of an arrow head
      # with two wheels.
      poly = Shapes.arrow_head_polygon((x, y),
                                       phi,
                                       scale=0.02)
      f.add_polygons([poly],
                     color="red",
                     alpha=0.5)
      wheels = Shapes.rectangle_pair((x,y),
                                     5.,2.,7.,
                                     angle=phi,
                                     scale=0.02)
      f.add_polygons(wheels,
                     color="black",
                     alpha=0.5)

      # Add some anotation
      f.add_text(pos=(-0.5,-0.5), size=0.1, text="Time=%.2fs"%self.time,color="darkgreen")
      dy = -0.6
      for i,s in enumerate(text_info.split('\n')):
        f.add_text(pos=(-0.5,dy-0.1*i), size=0.07,
                   text=s,color="darkgreen")

      self.viewer.add_frame(f)
      time.sleep(0.01)
    
  def step(self,
           dt):
    """Take a timestep and draw the new pose"""
    prev_left_ticks = self.left_encoder.get_ticks()
    prev_right_ticks = self.right_encoder.get_ticks()

    self.left_encoder.update_ticks(self.velocity_left,dt)
    self.right_encoder.update_ticks(self.velocity_right,dt)

    left_ticks = self.left_encoder.get_ticks()
    right_ticks = self.right_encoder.get_ticks()

    rad_per_tick = 2*pi/self.left_encoder.get_ticks_per_rev()
    m_per_rad = rad_per_tick * self.wheel_radius

    # Distances traveled by left and right wheels
    drad_left = (left_ticks - prev_left_ticks)*rad_per_tick
    drad_right = (right_ticks - prev_right_ticks)*rad_per_tick
    dm_left = drad_left * m_per_rad
    dm_right = drad_right * m_per_rad

    # Convert to uni cycle model
    dm_center = 0.5*(dm_left+dm_right)
    dphi = (dm_right - dm_left)/self.axis_length

    # Get previous pose
    x,y,phi = self.state.get_pose()

    # Do linear integration. simiam uses ode45, which seems to
    # be an overkill!
    phi += dphi
    dx = dm_center * cos(phi)
    x+= dx
    dy = dm_center * sin(phi)
    y += dy

    self.state.set_pose(x,y,phi)
    self.path += [(x,y)]
    self.time+=dt

  def get_pose(self):
    """Return the current robot direction based on the position
    and direction of the differential wheels"""    
    return self.state.get_pose()

  def get_v_and_w(self):
    return self.diff_to_uni(self.velocity_left,
                            self.velocity_right)

  def reached_goal(self):
    """Returns true if we have reached the goal"""
    x,y,phi = self.state.get_pose()
    epsilon = 0.02**2
    return len2(x-self.goal[0],y-self.goal[1]) < epsilon

  def get_dir_to_goal(self):
    x,y,phi = self.get_pose()
    return atan2(self.goal[1]-y,self.goal[0]-x)
    
# Create the viewer window
viewer = Euv.Viewer(size=(600,600),
                    view_port_center = (0,0),
                    view_port_width = 3,
                    flip_y = True
                    )

# Create the robot
wheel_radius = 0.1
wheel_apart = 0.2
init = (0,0)
goal = (0,1)
robot = Robot(wheel_apart,
              wheel_radius,
              viewer=viewer,
              init=init,
              goal=goal) 

# Set the initial position of the robot
robot.set_pose(0.,0.,0)
velocity = 1
vel_l, vel_r = robot.uni_to_diff(velocity, 0)
robot.set_wheel_speeds(vel_l,vel_r)

# Do PID loop
dt = 0.1

steps_num = 0
epsilon = 1e-3

# Loop until we reach the goal or we reach 400 steps.
while steps_num < 400:
  x,y,phi = robot.get_pose()
  v,w = robot.get_v_and_w()

  # The direction to the goal
  phi_d = robot.get_dir_to_goal()

  # Our current error in direction
  e_k = normalize_angle(phi_d - phi)

  # Correction strength
  Kp = 5
  new_w = Kp*e_k

  # Update the angular speed but not the velocity
  vel_l, vel_r = robot.uni_to_diff(velocity, new_w)

  # Set the new direction
  robot.set_wheel_speeds(vel_l,vel_r)
  steps_num+=1
  robot.draw_robot(text_info= (
                   u"φ=%.2f\n"
                   u"φ_d=%.2f\n"
                   'e_k=%.3f\n'
                   u'ω =%.3f\n'
                   'vel_l=%.3f\n'
                   'vel_r=%.3f'
                   %(phi,phi_d,e_k,new_w,vel_l,vel_r)))

  if robot.reached_goal():
    break
  robot.step(dt)


viewer.wait()
