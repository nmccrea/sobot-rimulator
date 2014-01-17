#!/usr/bin/env python

# Sobot Rimulator - A Robot Programming Tool
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Email mccrea.engineering@gmail.com for questions, comments, or to report bugs.





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
    
    # gtk simulation event source - for simulation control
    self.sim_event_source = gobject.idle_add( self.initialize_sim, True ) # we use this opportunity to initialize the sim
    
    # start gtk
    gtk.main()
    
    
  def initialize_sim( self, random=False ):
    # reset the viewer
    self.viewer.control_panel_state_init()
    
    # create the simulation world
    self.world = World( self.period )
    
    # create the robot
    robot = Robot()
    self.world.add_robot( robot )
    
    # generate a random environment
    if random:
      self.map_manager.random_map( self.world )
    else:
      self.map_manager.apply_to_world( self.world )
    
    # create the world view
    self.world_view = WorldView( self.world, self.viewer )
    
    # render the initial world
    self.draw_world()
    
    
  def play_sim( self ):
    gobject.source_remove( self.sim_event_source )  # this ensures multiple calls to play_sim do not speed up the simulator
    self._run_sim()
    self.viewer.control_panel_state_playing()
    
    
  def pause_sim( self ):
    gobject.source_remove( self.sim_event_source )
    self.viewer.control_panel_state_paused()
    
    
  def step_sim_once( self ):
    self.pause_sim()
    self._step_sim()
    
    
  def end_sim( self, alert_text='' ):
    gobject.source_remove( self.sim_event_source )
    self.viewer.control_panel_state_finished( alert_text )
    
    
  def reset_sim( self ):
    self.pause_sim()
    self.initialize_sim()
    
    
  def save_map( self, filename ):
    self.map_manager.save_map( filename )
    
    
  def load_map( self, filename ):
    self.map_manager.load_map( filename )
    self.reset_sim()
    
    
  def random_map( self ):
    self.pause_sim()
    self.initialize_sim( random = True )
    
    
  def draw_world( self ):
    self.viewer.new_frame()                 # start a fresh frame
    self.world_view.draw_world_to_frame()   # draw the world onto the frame
    self.viewer.draw_frame()                # render the frame
    
    
  def _run_sim( self ):
    self.sim_event_source = gobject.timeout_add( int( self.period * 1000 ), self._run_sim )
    self._step_sim()
    
    
  def _step_sim( self ):
    # increment the simulation
    try:
      self.world.step()
    except CollisionException:
      self.end_sim( 'Collision!' )
    except GoalReachedException:
      self.end_sim( 'Goal Reached!' )
      
    # draw the resulting world
    self.draw_world()


# RUN THE SIM:
Simulator()
