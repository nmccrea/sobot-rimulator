#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import gobject

from frame import *
from painter import *

DEFAULT_VIEW_PIX_W = 800    # pixels
DEFAULT_VIEW_PIX_H = 800    # pixels
DEFAULT_ZOOM = 100          # pixels per meter

class Viewer:
  
  def __init__( self, simulator ):
    # bind the simulator
    self.simulator = simulator
    
    # initialize frame
    self.current_frame = None
    
    # initialize geometric parameters
    self.view_width_pixels = DEFAULT_VIEW_PIX_W
    self.view_height_pixels = DEFAULT_VIEW_PIX_H
    self.pixels_per_meter = DEFAULT_ZOOM
    
    # initialize the window
    self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
    self.window.set_title( 'Robot Simulator' )
    self.window.connect( 'delete_event', self.on_delete )
    
    # initialize the layout container
    self.layout_box = gtk.VBox()
    self.window.add( self.layout_box )
    
    # initialize the drawing_area
    self.drawing_area = gtk.DrawingArea()
    self.drawing_area.set_size_request( self.view_width_pixels, self.view_height_pixels )
    self.drawing_area.connect( 'expose_event', self.on_expose )
    self.layout_box.pack_start( self.drawing_area )
    
    # initialize the painter
    self.painter = Painter( self.drawing_area, self.pixels_per_meter )
    
    
    
    self.button_play = gtk.Button( 'Play' )
    self.button_play.connect( 'clicked', self.on_play )
    self.button_play.set_size_request( 120, 30 )
    self.layout_box.pack_start( self.button_play, True, False, 5 )
    
    
    self.button_stop = gtk.Button( 'Stop' )
    self.button_stop.connect( 'clicked', self.on_stop )
    self.layout_box.pack_start( self.button_stop, True, False, 5 )
    
    
    self.button_step = gtk.Button( 'Step' )
    self.button_step.connect( 'clicked', self.on_step )
    self.layout_box.pack_start( self.button_step, True, False, 5 )
    
    
    self.button_reset = gtk.Button( 'Reset' )
    self.button_reset.connect( 'clicked', self.on_reset )
    self.layout_box.pack_start( self.button_reset, True, False, 5 )
    
    
    
    
    
    self.window.show_all()
    
    
  def draw_frame( self, frame ):
    self.current_frame = frame
    self.drawing_area.queue_draw_area( 0, 0, self.view_width_pixels, self.view_height_pixels )
    
    
  # EVENT HANDLERS:
  def on_play( self, widget ):
    self.simulator.run_sim()
    
    
  def on_stop( self, widget ):
    self.simulator.stop_sim()
    
    
  def on_step( self, widget ):
    self.simulator.stop_sim()
    self.simulator.step_sim()
    
    
  def on_reset( self, widget ):
    self.simulator.reset_sim()
    
    
  def on_expose( self, widget, event ):
    if self.current_frame: self.painter.draw_frame( self.current_frame )
    
    
  def on_delete( self, widget, event ):
    gtk.main_quit()
    return False