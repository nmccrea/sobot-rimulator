#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

from models.map_generator import *
from models.robot import *
from models.world import *
from views.world_view import *

from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0 # hertz

class Week2Simulator:

  def __init__( self ):
    # timing control
    self.period = 1.0 / REFRESH_RATE  # seconds

    # create the simulation world
    self.world = World( self.period )

    # create the robot
    robot = Robot()
    self.world.add_robot( robot )

    # generate a random environment
    obstacles, goal = MapGenerator().random_init( robot.global_geometry )
    # override random initialization here

    # add the generated obstacles
    for o in obstacles:
      width, height, x, y, theta = o
      self.world.add_obstacle( RectangleObstacle( width, height, Pose( x, y, theta ) ) )

    # program the robot supervisor
    supervisor = robot.supervisor
    supervisor.goal = goal

    # create the world view
    self.world_view = WorldView( self.world )
    
    # run the simulation
    self.run_sim()

  def run_sim( self ):
    # initialize timing control
    next_refresh_time = time.time() + self.period

    # loop the simulation
    while self.world.world_time < 500:
      # increment the simulation
      try:
        self.world.step()
      except CollisionException:
        print "\n\nCOLLISION!\n\n"
        break
      except GoalReachedException:
        print "\n\nGOAL REACHED!\n\n"
        break

      # render the current state
      self.world_view.render_frame()

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
