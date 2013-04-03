#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

import Euv.EuvGtk as Euv
import Euv.Frame as Frame
import Euv.Shapes as Shapes
import Euv.Color as Color
from robot_view import *

VIEW_PORT_PIX_H = 800
VIEW_PORT_PIX_W = 800
CONTROLS_PIX_H = 50

WORLD_WIDTH = 10 # meters

class WorldView:

  def __init__( self ):
    # create viewer
    self.viewer = Euv.Viewer( size = (VIEW_PORT_PIX_W, VIEW_PORT_PIX_H+CONTROLS_PIX_H),
                          view_port_center = (0, 0),
                          view_port_width = WORLD_WIDTH,
                          flip_y = True )

    # initialize the current frame object
    self.current_frame = Frame.Frame()

    # initialize list of robots views
    self.robot_views = []

  def add_robot( self, robot ):
    robot_view = RobotView( self.viewer, robot )
    self.robot_views.append( robot_view )

  def render_frame( self ):
    # draw the grid
    self._draw_grid_to_frame()

    # draw all the robots
    for robot_view in self.robot_views:
      robot_view.draw_robot_to_frame( self.current_frame )

    # cycle the frame
    self.viewer.add_frame( self.current_frame )   # push the current frame
    self.current_frame = Frame.Frame()            # prepare the next frame
  
  def wait( self ):
    self.viewer.wait()

  def _draw_grid_to_frame( self ):
    # NOTE: THIS FORMULA ASSUMES THE FOLLOWING:
    # - Window size never changes
    # - Window is always centered at (0, 0)

    w = self._meters_per_pixel() * VIEW_PORT_PIX_W
    h = self._meters_per_pixel() * VIEW_PORT_PIX_H
    half_w = w / 2.0
    half_h = h / 2.0

    w_start = -int( half_w )
    w_end = int( half_w )
    h_start = -int( half_h )
    h_end = int( half_h )
    
    # draw a gridline at every meter
    lines = []
    for x in range( w_start, w_end+1 ):
      for y in range( h_start, h_end+1 ):
        h_gridline = [ [ -half_w, y ], [ half_w, y ] ]
        v_gridline = [ [ x, -half_h ], [ x, half_h ] ]
        lines.append( h_gridline )
        lines.append( v_gridline )

    self.current_frame.add_lines( lines,
                     linewidth = self._meters_per_pixel(),
                     color = "black",
                     alpha = 0.2 )

  def _meters_per_pixel( self ):
    return float( WORLD_WIDTH ) / float( VIEW_PORT_PIX_W )
