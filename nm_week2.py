#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

from models.world import *
from models.rectangle_obstacle import *
from models.robot import *
from views.world_view import *

from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0 # hertz

class Week2Simulator:

  def __init__( self ):
    # timing control
    self.period = 1.0 / REFRESH_RATE  # seconds

    # create the simulation world
    self.world = World( self.period )
    self.world_view = WorldView()

    # create some obstacles
    obstacle = RectangleObstacle( 0.3, 0.1,
                                  Pose( 0.15, 0.12, -pi/6 ) )
    self._add_obstacle( obstacle )
    obstacle = RectangleObstacle( 0.1, 0.2,
                                  Pose( 0.3, -0.6, pi/4 ) )
    self._add_obstacle( obstacle )
    
    # create the robot
    robot = Robot()
    self._add_robot( robot )

    # program the robot supervisor
    supervisor = robot.supervisor
    supervisor.goal = [ -1.0, -1.3 ]
    
    # run the simulation
    self.run_sim()

  def run_sim( self ):
    # initialize timing control
    next_refresh_time = time.time() + self.period

    # loop the simulation
    while self.world.world_time < 100:
      # render the current state
      self.world_view.render_frame()
      
      # increment the simulation
      try:
        self.world.step()
      except CollisionException:
        print "\n\nCOLLISION!\n\n"
        break
      except GoalReachedException:
        print "\n\nGOAL REACHED!\n\n"
        break

      # pause the simulation until the next refresh time
      while time.time() < next_refresh_time: time.sleep( 0 )  # loop sleep until time to refresh
      next_refresh_time = time.time() + self.period           # update next refresh time
    
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
