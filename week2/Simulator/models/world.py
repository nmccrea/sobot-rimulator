#!/usr/bin/python
# -*- Encoding: utf-8 -*

import time

class World:

  def __init__( self ):
    # initialize world time
    self.world_time = 0.0 # seconds
    self.dt = 0.1         # seconds
    
    # initialize lists of world objects
    self.robots = []
    self.obstacles = []

  def add_robot( self, robot ):
    self.robots.append( robot )

  def add_obstacle( self, obstacle ):
    self.obstacles.append( obstacle )

  def tick( self ):
    dt = self.dt
    
    # update all the robots
    for robot in self.robots:
      robot.update_state( dt )
    
    # increment world time
    self.world_time += dt
    # pause the simulation for a moment
    time.sleep( dt )
