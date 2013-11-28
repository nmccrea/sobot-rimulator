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
    
    # initialize the drawing_area
    self.drawing_area = gtk.DrawingArea()
    self.drawing_area.set_size_request( self.view_width_pixels, self.view_height_pixels )
    self.drawing_area.connect( 'expose_event', self.on_expose )
    
    # initialize the painter
    self.painter = Painter( self.drawing_area, self.pixels_per_meter )
    
    # initialize the buttons
    # build the play button
    self.button_play = gtk.Button( 'Play' )
    play_image = gtk.Image()
    play_image.set_from_stock( gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_BUTTON )
    self.button_play.set_image( play_image )
    self.button_play.set_image_position( gtk.POS_LEFT )
    self.button_play.connect( 'clicked', self.on_play )
    
    # build the stop button
    self.button_stop = gtk.Button( 'Stop' )
    stop_image = gtk.Image()
    stop_image.set_from_stock( gtk.STOCK_MEDIA_STOP, gtk.ICON_SIZE_BUTTON )
    self.button_stop.set_image( stop_image )
    self.button_stop.set_image_position( gtk.POS_LEFT )
    self.button_stop.connect( 'clicked', self.on_stop )
    
    # build the step button
    self.button_step = gtk.Button( 'Step' )
    step_image = gtk.Image()
    step_image.set_from_stock( gtk.STOCK_MEDIA_NEXT, gtk.ICON_SIZE_BUTTON )
    self.button_step.set_image( step_image )
    self.button_step.set_image_position( gtk.POS_LEFT )
    self.button_step.connect( 'clicked', self.on_step )
    
    # build the reset button
    self.button_reset = gtk.Button( 'Reset' )
    reset_image = gtk.Image()
    reset_image.set_from_stock( gtk.STOCK_MEDIA_REWIND, gtk.ICON_SIZE_BUTTON )
    self.button_reset.set_image( reset_image )
    self.button_reset.set_image_position( gtk.POS_LEFT )
    self.button_reset.connect( 'clicked', self.on_reset )
    
    # build the save map button
    self.button_save_map = gtk.Button( 'Save Map' )
    save_map_image = gtk.Image()
    save_map_image.set_from_stock( gtk.STOCK_SAVE, gtk.ICON_SIZE_BUTTON )
    self.button_save_map.set_image( save_map_image )
    self.button_save_map.set_image_position( gtk.POS_LEFT )
    self.button_save_map.connect( 'clicked', self.on_save_map )
    
    # build the load map button
    self.button_load_map = gtk.Button( 'Load Map' )
    load_map_image = gtk.Image()
    load_map_image.set_from_stock( gtk.STOCK_OPEN, gtk.ICON_SIZE_BUTTON )
    self.button_load_map.set_image( load_map_image )
    self.button_load_map.set_image_position( gtk.POS_LEFT )
    self.button_load_map.connect( 'clicked', self.on_load_map )
    
    # build the random map buttons
    self.button_random_map = gtk.Button( 'Random Map' )
    random_map_image = gtk.Image()
    random_map_image.set_from_stock( gtk.STOCK_REFRESH, gtk.ICON_SIZE_BUTTON )
    self.button_random_map.set_image( random_map_image )
    self.button_random_map.set_image_position( gtk.POS_LEFT )
    self.button_random_map.connect( 'clicked', self.on_random_map )
    
    # pack the simulation control buttons
    sim_controls_box = gtk.HBox( spacing = 5 )
    sim_controls_box.pack_start( self.button_play, False, False )
    sim_controls_box.pack_start( self.button_stop, False, False )
    sim_controls_box.pack_start( self.button_step, False, False )
    sim_controls_box.pack_start( self.button_reset, False, False )
    
    # pack the map control buttons
    map_controls_box = gtk.HBox( spacing = 5 )
    map_controls_box.pack_start( self.button_save_map, False, False )
    map_controls_box.pack_start( self.button_load_map, False, False )
    map_controls_box.pack_start( self.button_random_map, False, False )
    
    # align the controls
    sim_controls_alignment = gtk.Alignment( 0.5, 0.0, 0.0, 1.0 )
    map_controls_alignment = gtk.Alignment( 0.5, 0.0, 0.0, 1.0 )
    sim_controls_alignment.add( sim_controls_box )
    map_controls_alignment.add( map_controls_box )
    
    # create the alert box
    self.alert_box = gtk.Label()
    
    # lay out the simulation view and all of the controls
    layout_box = gtk.VBox()
    layout_box.pack_start( self.drawing_area )
    layout_box.pack_start( self.alert_box, False, False, 5 )
    layout_box.pack_start( sim_controls_alignment, False, False, 5 )
    layout_box.pack_start( map_controls_alignment, False, False, 5 )
    
    # apply the layout
    self.window.add( layout_box )
    
    # show the simulator window
    self.window.show_all()
    
    
  def new_frame( self ):
    self.current_frame = Frame()
    
    
  def draw_frame( self ):
    self.drawing_area.queue_draw_area( 0, 0, self.view_width_pixels, self.view_height_pixels )
    
    
  def restrict( self, alert_text ):
    self.alert_box.set_text( alert_text )
    self.button_play.set_sensitive( False )
    self.button_stop.set_sensitive( False )
    self.button_step.set_sensitive( False )
    
    
  def reset( self ):
    self.alert_box.set_text( '' )
    self.button_play.set_sensitive( True )
    self.button_stop.set_sensitive( True )
    self.button_step.set_sensitive( True )
    self.button_reset.set_sensitive( False )
    
    
  # EVENT HANDLERS:
  def on_play( self, widget ):
    self.button_reset.set_sensitive( True )
    self.simulator.run_sim()
    
    
  def on_stop( self, widget ):
    self.simulator.stop_sim()
    
    
  def on_step( self, widget ):
    self.button_reset.set_sensitive( True )
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