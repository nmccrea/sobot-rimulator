#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk

from frame import *
from painter import *

DEFAULT_VIEW_PIX_W = 800    # pixels
DEFAULT_VIEW_PIX_H = 800    # pixels
DEFAULT_ZOOM = 100          # pixels per meter

class Viewer:
  
  def __init__( self ):
    self.frames = []
    self.current_frame = None
    
    # geometric parameters
    self.view_width_pixels = DEFAULT_VIEW_PIX_W
    self.view_height_pixels = DEFAULT_VIEW_PIX_H
    self.pixels_per_meter = DEFAULT_ZOOM
    
    # initialize the window
    self.window = gtk.Window( gtk.WINDOW_TOPLEVEL )
    self.window.set_title( "Application" )
    self.window.connect( "delete_event", self.delete_event )
    
    # initialize the layout container
    self.layout_box = gtk.VBox()
    self.window.add( self.layout_box )
    
    # initialize the drawing_area
    self.drawing_area = gtk.DrawingArea()
    self.drawing_area.set_size_request( self.view_width_pixels, self.view_height_pixels )
    self.drawing_area.connect( "expose_event", self.expose_event )
    self.layout_box.pack_start( self.drawing_area )
    
    # initialize the painter
    self.painter = Painter( self.drawing_area, self.pixels_per_meter )
    
    
    
    self.button = gtk.Button( 'Click' )
    self.button.set_size_request( 120, 30 )
    self.layout_box.pack_start( self.button, True, False, 5 )
    
    
    
    
    
    self.window.show_all()
    
    
  def add_frame( self, frame ):
    self.frames.append( frame )
    self.current_frame = frame
    
    self.drawing_area.queue_draw_area( 0, 0, self.view_width_pixels, self.view_height_pixels )
    
    
  def expose_event( self, widget, event ):
    if self.current_frame:
      self.painter.draw_frame( self.current_frame )
    
    
  def delete_event( self, widget, event ):
    gtk.main_quit()
    return False