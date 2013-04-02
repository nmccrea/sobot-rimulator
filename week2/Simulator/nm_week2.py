#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

from models.world import *
from models.robot import *
from views.world_view import *
from views.robot_view import *

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
