#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

import pygtk
pygtk.require( '2.0' )
import gtk
import glib

from models.map_generator import *
from models.robot import *
from models.world import *
from views.world_view import *

from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0 # hertz

class Simulator:

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
    supervisor = robot.supervisor.goal = goal
    
    # create the world view
    self.world_view = WorldView( self.world )
    
    # start the simulation
    glib.idle_add( self.run_sim )
    gtk.main()
    
  def run_sim( self ):
    s = glib.timeout_add( int( self.period * 1000 ), self.run_sim )
    
    # increment the simulation
    try:
      self.world.step()
    except CollisionException:
      glib.source_remove( s )
      print "\n\nCOLLISION!\n\n"
    except GoalReachedException:
      glib.source_remove( s )
      print "\n\nGOAL REACHED!\n\n"
  
    # render the current state
    self.world_view.render_frame()
    
  def _add_robot( self, robot ):
    self.world.add_robot( robot )
    self.world_view.add_robot( robot )

  def _add_obstacle( self, obstacle ):
    self.world.add_obstacle( obstacle )
    self.world_view.add_obstacle( obstacle )


# RUN THE SIM:
Simulator()
