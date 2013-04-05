#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

from utils import math_utils
import Euv.EuvGtk as Euv
import Euv.Frame as Frame
import Euv.Shapes as Shapes
import Euv.Color as Color
from robot_view import *

VIEW_PORT_PIX_H = 800
VIEW_PORT_PIX_W = 800
CONTROLS_PIX_H = 50

WORLD_WIDTH = 4 # meters

MAJOR_GRIDLINE_INTERVAL = 1.0 # meters
MINOR_GRIDLINE_INTERVAL = 0.2 # meters

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
    
    # determine world space to draw grid upon
    w = self._meters_per_pixel() * VIEW_PORT_PIX_W
    h = self._meters_per_pixel() * VIEW_PORT_PIX_H
    half_w = w / 2.0
    half_h = h / 2.0

    w_start = -half_w
    w_end = half_w
    h_start = -half_h
    h_end = half_h

    # build the gridlines
    major_gridlines = [] # accumulator for major gridlines
    minor_gridlines = [] # accumulator for minor gridlines
    for x in math_utils.frange( w_start, w_end+1, MINOR_GRIDLINE_INTERVAL ):
      for y in math_utils.frange( h_start, h_end+1, MINOR_GRIDLINE_INTERVAL ):
        # clear up floating point errors
        x = round( x, 2 )
        y = round( y, 2 )

        h_gridline = [ [ -half_w, y ], [ half_w, y ] ] # horizontal gridline
        v_gridline = [ [ x, -half_h ], [ x, half_h ] ] # vertical gridline

        if x % MAJOR_GRIDLINE_INTERVAL== 0:     # sort majors from minors vertical
          major_gridlines.append( v_gridline )
        else:
          minor_gridlines.append( v_gridline )

        if y % MAJOR_GRIDLINE_INTERVAL  == 0:   # sort majors from minors horizontal
          major_gridlines.append( h_gridline )
        else:
          minor_gridlines.append( h_gridline )
    
    # draw the gridlines
    self.current_frame.add_lines( major_gridlines,          # draw major gridlines
                      linewidth = self._meters_per_pixel(),
                      color = "black",
                      alpha = 0.2 )
    self.current_frame.add_lines( minor_gridlines,          # draw minor gridlines
                      linewidth = self._meters_per_pixel(),
                      colro = "black",
                      alpha = 0.1 )


  def _meters_per_pixel( self ):
    return float( WORLD_WIDTH ) / float( VIEW_PORT_PIX_W )
