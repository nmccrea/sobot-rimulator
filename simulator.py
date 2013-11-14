#!/usr/bin/python
# -*- Encoding: utf-8 -*

import pygtk
pygtk.require( '2.0' )
import gtk
import gobject

import gui.frame
import gui.viewer

from models.map_generator import *
from models.robot import *
from models.world import *

from views.world_view import *

from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0 # hertz

class Simulator:

  def __init__( self ):
    # create the GUI
    self.viewer = gui.viewer.Viewer( self )
    
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
    self.draw_world()
    
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
    self.draw_world()
    
    
  def draw_world( self ):
    frame = gui.frame.Frame()
    self.world_view.draw_world_to_frame( frame )  # draw the world onto the frame
    self.viewer.draw_frame( frame )               # render the frame


# RUN THE SIM:
Simulator()
