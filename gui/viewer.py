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





import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk as gtk
from gi.repository import GObject
from gi.repository import GdkPixbuf

from gui.frame import Frame
from gui.painter import Painter

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
    self.window = gtk.Window()
    self.window.set_title( 'Sobot Rimulator' )
    self.window.set_resizable( False )
    self.window.connect( 'delete_event', self.on_delete )
    
    # initialize the drawing_area
    self.drawing_area = gtk.DrawingArea()
    self.drawing_area.set_size_request( self.view_width_pixels, self.view_height_pixels )
    self.drawing_area.connect( 'draw', self.on_expose )
    
    # initialize the painter
    self.painter = Painter( self.pixels_per_meter )
    
    # == initialize the buttons
    
    # build the play button
    self.button_play = gtk.Button( 'Play' )
    play_image = gtk.Image()
    play_image.set_from_stock( gtk.STOCK_MEDIA_PLAY, gtk.IconSize.BUTTON )
    self.button_play.set_image( play_image )
    self.button_play.set_image_position( gtk.PositionType.LEFT )
    self.button_play.connect( 'clicked', self.on_play )
    
    # build the stop button
    self.button_stop = gtk.Button( 'Stop' )
    stop_image = gtk.Image()
    stop_image.set_from_stock( gtk.STOCK_MEDIA_STOP, gtk.IconSize.BUTTON )
    self.button_stop.set_image( stop_image )
    self.button_stop.set_image_position( gtk.PositionType.LEFT )
    self.button_stop.connect( 'clicked', self.on_stop )
    
    # build the step button
    self.button_step = gtk.Button( 'Step' )
    step_image = gtk.Image()
    step_image.set_from_stock( gtk.STOCK_MEDIA_NEXT, gtk.IconSize.BUTTON )
    self.button_step.set_image( step_image )
    self.button_step.set_image_position( gtk.PositionType.LEFT )
    self.button_step.connect( 'clicked', self.on_step )
    
    # build the reset button
    self.button_reset = gtk.Button( 'Reset' )
    reset_image = gtk.Image()
    reset_image.set_from_stock( gtk.STOCK_MEDIA_REWIND, gtk.IconSize.BUTTON )
    self.button_reset.set_image( reset_image )
    self.button_reset.set_image_position( gtk.PositionType.LEFT )
    self.button_reset.connect( 'clicked', self.on_reset )
    
    # build the save map button
    self.button_save_map = gtk.Button( 'Save Map' )
    save_map_image = gtk.Image()
    save_map_image.set_from_stock( gtk.STOCK_SAVE, gtk.IconSize.BUTTON )
    self.button_save_map.set_image( save_map_image )
    self.button_save_map.set_image_position( gtk.PositionType.LEFT )
    self.button_save_map.connect( 'clicked', self.on_save_map )
    
    # build the load map button
    self.button_load_map = gtk.Button( 'Load Map' )
    load_map_image = gtk.Image()
    load_map_image.set_from_stock( gtk.STOCK_OPEN, gtk.IconSize.BUTTON )
    self.button_load_map.set_image( load_map_image )
    self.button_load_map.set_image_position( gtk.PositionType.LEFT )
    self.button_load_map.connect( 'clicked', self.on_load_map )
    
    # build the random map buttons
    self.button_random_map = gtk.Button( 'Random Map' )
    random_map_image = gtk.Image()
    random_map_image.set_from_stock( gtk.STOCK_REFRESH, gtk.IconSize.BUTTON )
    self.button_random_map.set_image( random_map_image )
    self.button_random_map.set_image_position( gtk.PositionType.LEFT )
    self.button_random_map.connect( 'clicked', self.on_random_map )
    
    # build the draw-invisibles toggle button
    self.draw_invisibles = False                  # controls whether invisible world elements are displayed
    self.button_draw_invisibles = gtk.Button()
    self._decorate_draw_invisibles_button_inactive()
    self.button_draw_invisibles.set_image_position( gtk.PositionType.LEFT )
    self.button_draw_invisibles.connect( 'clicked', self.on_draw_invisibles )
    
    # == lay out the window
    
    # pack the simulation control buttons
    sim_controls_box = gtk.HBox( spacing = 5 )
    sim_controls_box.pack_start( self.button_play, False, False, 0 )
    sim_controls_box.pack_start( self.button_stop, False, False, 0 )
    sim_controls_box.pack_start( self.button_step, False, False, 0 )
    sim_controls_box.pack_start( self.button_reset, False, False, 0 )
    
    # pack the map control buttons
    map_controls_box = gtk.HBox( spacing = 5 )
    map_controls_box.pack_start( self.button_save_map, False, False, 0 )
    map_controls_box.pack_start( self.button_load_map, False, False, 0 )
    map_controls_box.pack_start( self.button_random_map, False, False, 0 )
    
    # pack the invisibles button
    invisibles_button_box = gtk.HBox()
    invisibles_button_box.pack_start( self.button_draw_invisibles, False, False, 0 )
    
    # align the controls
    sim_controls_alignment = gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
    map_controls_alignment = gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
    invisibles_button_alignment = gtk.Alignment(xalign=0.5, yalign=0.5, xscale=0, yscale=0)
    sim_controls_alignment.add( sim_controls_box )
    map_controls_alignment.add( map_controls_box )
    invisibles_button_alignment.add( invisibles_button_box )
    
    # create the alert box
    self.alert_box = gtk.Label()
    
    # lay out the simulation view and all of the controls
    layout_box = gtk.VBox()
    layout_box.pack_start( self.drawing_area, False, False, 0 )
    layout_box.pack_start( self.alert_box, False, False, 5 )
    layout_box.pack_start( sim_controls_alignment, False, False, 5 )
    layout_box.pack_start( map_controls_alignment, False, False, 5 )
    layout_box.pack_start( invisibles_button_alignment, False, False, 5 )
    
    # apply the layout
    self.window.add( layout_box )
    
    # show the simulator window
    self.window.show_all()
    
    
  def new_frame( self ):
    self.current_frame = Frame()
    
    
  def draw_frame( self ):
    self.drawing_area.queue_draw_area( 0, 0, self.view_width_pixels, self.view_height_pixels )
    
    
  def control_panel_state_init( self ):
    self.alert_box.set_text( '' )
    self.button_play.set_sensitive( True )
    self.button_stop.set_sensitive( False )
    self.button_step.set_sensitive( True )
    self.button_reset.set_sensitive( False )
    
    
  def control_panel_state_playing( self ):
    self.button_play.set_sensitive( False )
    self.button_stop.set_sensitive( True )
    self.button_reset.set_sensitive( True )
    
    
  def control_panel_state_paused( self ):
    self.button_play.set_sensitive( True )
    self.button_stop.set_sensitive( False )
    self.button_reset.set_sensitive( True )
    
    
  def control_panel_state_finished( self, alert_text ):
    self.alert_box.set_text( alert_text )
    self.button_play.set_sensitive( False )
    self.button_stop.set_sensitive( False )
    self.button_step.set_sensitive( False )
    
    
  # EVENT HANDLERS:
  def on_play( self, widget ):
    self.simulator.play_sim()
    
    
  def on_stop( self, widget ):
    self.simulator.pause_sim()
    
    
  def on_step( self, widget ):
    self.simulator.step_sim_once()
    
    
  def on_reset( self, widget ):
    self.simulator.reset_sim()
    
    
  def on_save_map( self, widget ):
    # create the file chooser
    file_chooser = gtk.FileChooserDialog( title = 'Save Map',
                                          parent = self.window,
                                          action = gtk.FileChooserAction.SAVE,
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
                                          action = gtk.FileChooserAction.OPEN,
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
    
    
  def on_draw_invisibles( self, widget ):    
    # toggle the draw_invisibles state
    self.draw_invisibles = not self.draw_invisibles
    if self.draw_invisibles:
      self._decorate_draw_invisibles_button_active()
    else:
      self._decorate_draw_invisibles_button_inactive()
    self.simulator.draw_world()
    
    
  def on_expose( self, widget, context):
    self.painter.draw_frame( self.current_frame, widget, context )
    
    
  def on_delete( self, widget, event ):
    gtk.main_quit()
    return False
    
    
  def _decorate_draw_invisibles_button_active( self ):
    draw_invisibles_image = gtk.Image()
    draw_invisibles_image.set_from_stock( gtk.STOCK_REMOVE, gtk.IconSize.BUTTON )
    self.button_draw_invisibles.set_image( draw_invisibles_image )
    self.button_draw_invisibles.set_label( 'Hide Invisibles' )
    
    
  def _decorate_draw_invisibles_button_inactive( self ):
    draw_invisibles_image = gtk.Image()
    draw_invisibles_image.set_from_stock( gtk.STOCK_ADD, gtk.IconSize.BUTTON )
    self.button_draw_invisibles.set_image( draw_invisibles_image )
    self.button_draw_invisibles.set_label( 'Show Invisibles' )
