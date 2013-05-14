#!/usr/bin/python
# -*- Encoding: utf-8 -*

import time
from physics import *

class World:

  def __init__( self ):
    # initialize physics engine
    self.physics = Physics( self )

    # initialize world time
    self.world_time = 0.0 # seconds
    self.dt = 0.05        # seconds
    
    # initialize lists of world objects
    self.computers = []
    self.robots = []
    self.obstacles = []

  # step the simulation through one time interval
  def step( self ):
    dt = self.dt
    
    # step all the robots
    for robot in self.robots:
      # step robot motion
      robot.step_motion( dt )

    # apply physics interactions
    self.physics.apply_physics()

    # NOTE: the computers must run last to ensure they are observing the "current" world
    # step all of the computers
    for computer in self.computers:
      computer.execute()

    # increment world time
    self.world_time += dt
    # pause the simulation for a moment
    time.sleep( dt )

  def add_robot( self, robot ):
    self.robots.append( robot )
    self.computers.append( robot.supervisor )

  def add_obstacle( self, obstacle ):
    self.obstacles.append( obstacle )

  # return all objects in the world that might collide with other objects in the world during simulation
  def colliders( self ):
    # moving objects only
    return self.robots  # as obstacles are static we should not test them against each other

  # return all solids in the world
  def solids( self ):
    return self.robots + self.obstacles
