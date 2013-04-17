#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

from models.world import *
from models.rectangle_obstacle import *
from models.robot import *
from views.world_view import *

from sim_exceptions.collision_exception import *

class Week2Simulator:

  def __init__( self ):
    # create the simulation world
    self.world = World()
    self.world_view = WorldView()
    
    # create the robot
    robot = Robot()
    robot.set_wheel_rotations( 9.0, 12.5 )
    self._add_robot( robot )
    # self._add_robot( Robot() )

    # create some obstacles
    obstacle = RectangleObstacle( 0.1,
                                  0.2,
                                  Pose( 0.2, 0.4, pi/4 ) )
    self._add_obstacle( obstacle )
    
    # run the simulation
    self.run_sim()

  def run_sim( self ):
    # loop the simulation
    # TODO make the loop condition smart
    while self.world.world_time < 5:
      # render the current state
      self.world_view.render_frame()
      
      # increment the simulation
      try:
        self.world.step()
      except CollisionException:
        print "\n\nCOLLISION!!\n\n"
        break
    
    # pause the GUI thread ( app crashes otherwise ) 
    self.world_view.wait()

  def _add_robot( self, robot ):
    self.world.add_robot( robot )
    self.world_view.add_robot( robot )

  def _add_obstacle( self, obstacle ):
    self.world.add_obstacle( obstacle )
    self.world_view.add_obstacle( obstacle )




# RUN THE SIM:
Week2Simulator()
