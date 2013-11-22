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

# user response codes for file chooser dialog buttons
LS_DIALOG_RESPONSE_CANCEL = 1
LS_DIALOG_RESPONSE_ACCEPT = 2

class Viewer:
  
  def __init__( self, simulator ):
    # bind the simulator
    self.simulator = simulator
    
    # initialize frame
    self.current_frame = Frame()
    
    # initialize camera parameters
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
    
    
    
    # initialize buttons
    self.button_play = gtk.Button( 'Play' )
    self.button_play.connect( 'clicked', self.on_play )
    self.button_play.set_size_request( 120, 30 )
    self.layout_box.pack_start( self.button_play, True, False, 0 )
    
    
    self.button_stop = gtk.Button( 'Stop' )
    self.button_stop.connect( 'clicked', self.on_stop )
    self.layout_box.pack_start( self.button_stop, True, False, 0 )
    
    
    self.button_step = gtk.Button( 'Step' )
    self.button_step.connect( 'clicked', self.on_step )
    self.layout_box.pack_start( self.button_step, True, False, 0 )
    
    
    self.button_reset = gtk.Button( 'Reset' )
    self.button_reset.connect( 'clicked', self.on_reset )
    self.layout_box.pack_start( self.button_reset, True, False, 0 )
    
    
    self.button_save_map = gtk.Button( 'Save Map' )
    self.button_save_map.connect( 'clicked', self.on_save_map )
    self.layout_box.pack_start( self.button_save_map, True, False, 0 )
    
    
    self.button_load_map = gtk.Button( 'Load Map' )
    self.button_load_map.connect( 'clicked', self.on_load_map )
    self.layout_box.pack_start( self.button_load_map, True, False, 0 )
    
    
    self.button_random_map = gtk.Button( 'Random Map' )
    self.button_random_map.connect( 'clicked', self.on_random_map )
    self.layout_box.pack_start( self.button_random_map, True, False, 0 )
    
    
    
    
    
    self.window.show_all()
    
    
  def new_frame( self ):
    self.current_frame = Frame()
    
    
  def draw_frame( self ):
    self.drawing_area.queue_draw_area( 0, 0, self.view_width_pixels, self.view_height_pixels )
    
    
  # EVENT HANDLERS:
  def on_play( self, widget ):
    self.simulator.run_sim()
    
    
  def on_stop( self, widget ):
    self.simulator.stop_sim()
    
    
  def on_step( self, widget ):
    self.simulator.step_sim_once()
    
    
  def on_reset( self, widget ):
    self.simulator.reset_sim()
    
    
  def on_save_map( self, widget ):
    # create the file chooser
    file_chooser = gtk.FileChooserDialog( title = 'Save Map',
                                          parent = self.window,
                                          action = gtk.FILE_CHOOSER_ACTION_SAVE,
                                          buttons = ( gtk.STOCK_CANCEL, LS_DIALOG_RESPONSE_CANCEL,
                                                      gtk.STOCK_SAVE, LS_DIALOG_RESPONSE_ACCEPT ) )
    file_chooser.set_do_overwrite_confirmation( True )
    file_chooser.set_current_folder( 'maps' )
    
    # run the file chooser dialog
    response_id = file_chooser.run()
    
    # handle the user's response
    if response_id == LS_DIALOG_RESPONSE_CANCEL:
      file_chooser.destroy()
    elif response_id == LS_DIALOG_RESPONSE_ACCEPT:
      self.simulator.save_map( file_chooser.get_filename() )
      file_chooser.destroy()
    
    
  def on_load_map( self, widget ):
    # create the file chooser
    file_chooser = gtk.FileChooserDialog( title = 'Load Map',
                                          parent = self.window,
                                          action = gtk.FILE_CHOOSER_ACTION_OPEN,
                                          buttons = ( gtk.STOCK_CANCEL, LS_DIALOG_RESPONSE_CANCEL,
                                                      gtk.STOCK_OPEN, LS_DIALOG_RESPONSE_ACCEPT ) )
    file_chooser.set_current_folder( 'maps' )
    
    # run the file chooser dialog
    response_id = file_chooser.run()
    
    # handle the user's response
    if response_id == LS_DIALOG_RESPONSE_CANCEL:
      file_chooser.destroy()
    elif response_id == LS_DIALOG_RESPONSE_ACCEPT:
      self.simulator.load_map( file_chooser.get_filename() )
      file_chooser.destroy()
      
      
  def on_random_map( self, widget ):
    self.simulator.random_map()
    
    
  def on_expose( self, widget, event ):
    self.painter.draw_frame( self.current_frame )
    
    
  def on_delete( self, widget, event ):
    gtk.main_quit()
    return False