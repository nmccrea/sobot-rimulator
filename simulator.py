#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

import pygtk
pygtk.require( '2.0' )
import gtk
import gobject

from models.map_generator import *
from models.robot import *
from models.world import *

import gui.viewer as viewer
import gui.frame as frame

from views.world_view import *

from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0 # hertz

class Simulator:

  def __init__( self ):
    # create the GUI
    self.viewer = viewer.Viewer( self )
    
    # initialize the current frame
    self.current_frame = frame.Frame()
    
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
    self.world_view = WorldView( self.world, self.viewer )
    
    # render the first frame
    self.render_frame()
    
    # start gtk
    gtk.main()
    
  def run_sim( self ):
    s = gobject.timeout_add( int( self.period * 1000 ), self.run_sim )
    
    # increment the simulation
    try:
      self.world.step()
    except CollisionException:
      gobject.source_remove( s )
      print "\n\nCOLLISION!\n\n"
    except GoalReachedException:
      gobject.source_remove( s )
      print "\n\nGOAL REACHED!\n\n"
  
    # render the current state
    self.render_frame()
    
  def render_frame( self ):
    self.world_view.draw_world_to_frame( self.current_frame )
    
    # cycle the frame
    self.viewer.draw_frame( self.current_frame )   # push the current frame
    self.current_frame = frame.Frame()            # prepare the next frame


# RUN THE SIM:
Simulator()
