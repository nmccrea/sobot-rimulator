#!/usr/bin/python
# -*- Encoding: utf-8 -*

import pygtk
pygtk.require( '2.0' )
import gtk
import gobject

import gui.frame
import gui.viewer

from models.map_manager import *
from models.robot import *
from models.world import *

from views.world_view import *

from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0 # hertz

class Simulator:

  def __init__( self ):
    # create the GUI
    self.viewer = gui.viewer.Viewer( self )
    
    # create the map manager
    self.map_manager = MapManager()
    
    # timing control
    self.period = 1.0 / REFRESH_RATE  # seconds
    
    # gtk simulation event source
    self.sim_event_source = gobject.idle_add( self.stop_sim )
    
    # initialize the simulation
    self.initialize_sim()
    
    # start gtk
    gtk.main()
    
    
  def initialize_sim( self ):
    # create the simulation world
    self.world = World( self.period )
    
    # create the robot
    robot = Robot()
    self.world.add_robot( robot )
    
    # generate a random environment
    obstacles, goal = self.map_manager.random_map( robot.global_geometry )
    # override random initialization here
    
    # add the generated obstacles
    for o in obstacles:
      width, height, x, y, theta = o
      self.world.add_obstacle( RectangleObstacle( width, height, Pose( x, y, theta ) ) )
      
    # program the robot supervisor
    robot.supervisor.goal = goal
    
    # create the world view
    self.world_view = WorldView( self.world, self.viewer )
    
    # render the initial world
    self._draw_world()
    
    
  def run_sim( self ):
    self.sim_event_source = gobject.timeout_add( int( self.period * 1000 ), self.run_sim )
    self._step_sim()
    
    
  def stop_sim( self ):
    gobject.source_remove( self.sim_event_source )
    
    
  def step_sim_once( self ):
    self.stop_sim()
    self._step_sim()
    
    
  def reset_sim( self ):
    self.stop_sim()
    self.initialize_sim()
    
    
  def save_map( self, filename ):
    self.map_manager.save_map( filename )
    
    
  def load_map( self, filename ):
    self.map_manager.load_map( filename )
    self.reset_sim()
    
    
  def _draw_world( self ):  
    self.viewer.new_frame()                 # start a fresh frame
    self.world_view.draw_world_to_frame()   # draw the world onto the frame
    self.viewer.draw_frame()                # render the frame
    
    
  def _step_sim( self ):
    # increment the simulation
    try:
      self.world.step()
    except CollisionException:
      self.stop_sim()
      print "\n\nCOLLISION!\n\n"
    except GoalReachedException:
      self.stop_sim()
      print "\n\nGOAL REACHED!\n\n"
      
    # draw the resulting world
    self._draw_world()


# RUN THE SIM:
Simulator()
