#!/usr/bin/python
# -*- Encoding: utf-8 -*

import Euv.EuvGtk as Euv
import Euv.Frame as Frame
import Euv.Shapes as Shapes
import Euv.Color as Color
from obstacle_view import *
from robot_view import *

VIEW_PORT_PIX_H = 950
VIEW_PORT_PIX_W = 950
CONTROLS_PIX_H = 50

WORLD_WIDTH = 8 # meters

MAJOR_GRIDLINE_INTERVAL = 1.0 # meters
MAJOR_GRIDLINE_SUBDIVISIONS = 5  # minor gridlines for every major gridline

class WorldView:

  def __init__( self, world ):
    # create viewer
    self.viewer = Euv.Viewer( size = (VIEW_PORT_PIX_W, VIEW_PORT_PIX_H+CONTROLS_PIX_H),
                          view_port_center = (0, 0),
                          view_port_width = WORLD_WIDTH,
                          recording = False,
                          flip_y = True )

    # initialize the current frame object
    self.current_frame = Frame.Frame()

    # initialize views for world objects
    self.robot_views = []
    for robot in world.robots: self.add_robot( robot )

    self.obstacle_views = []
    for obstacle in world.obstacles: self.add_obstacle( obstacle )

  def add_robot( self, robot ):
    robot_view = RobotView( self.viewer, robot )
    self.robot_views.append( robot_view )

  def add_obstacle( self, obstacle ):
    obstacle_view = ObstacleView( self.viewer, obstacle )
    self.obstacle_views.append( obstacle_view )

  def render_frame( self ):
    # draw the grid
    self._draw_grid_to_frame()

    # draw all the robots
    for robot_view in self.robot_views:
      robot_view.draw_robot_to_frame( self.current_frame )
    # draw all the obstacles
    for obstacle_view in self.obstacle_views:
      obstacle_view.draw_obstacle_to_frame( self.current_frame )

    # cycle the frame
    self.viewer.add_frame( self.current_frame )   # push the current frame
    self.current_frame = Frame.Frame()            # prepare the next frame
  
  def wait( self ):
    self.viewer.wait()

  def _draw_grid_to_frame( self ):
    # NOTE: THIS FORMULA ASSUMES THE FOLLOWING:
    # - Window size never changes
    # - Window is always centered at (0, 0)

    # calculate minor gridline interval
    minor_gridline_interval = MAJOR_GRIDLINE_INTERVAL / MAJOR_GRIDLINE_SUBDIVISIONS
    
    # determine world space to draw grid upon
    width = self._meters_per_pixel() * VIEW_PORT_PIX_W
    height = self._meters_per_pixel() * VIEW_PORT_PIX_H
    x_halfwidth = width * 0.5
    y_halfwidth = height * 0.5
    
    x_max = int( x_halfwidth / minor_gridline_interval )
    y_max = int( y_halfwidth / minor_gridline_interval )

    # build the gridlines
    major_lines_accum = []                  # accumulator for major gridlines
    minor_lines_accum = []                  # accumulator for minor gridlines

    for i in range( x_max + 1 ):            # build the vertical gridlines
      x = i * minor_gridline_interval

      if x % MAJOR_GRIDLINE_INTERVAL == 0:                        # sort major from minor
        accum = major_lines_accum
      else:
        accum = minor_lines_accum

      accum.append( [ [ x, -y_halfwidth ], [ x, y_halfwidth ] ] )   # positive-side gridline
      accum.append( [ [ -x, -y_halfwidth ], [ -x, y_halfwidth ] ] ) # negative-side gridline

    for j in range( y_max + 1 ):            # build the horizontal gridlines
      y = j * minor_gridline_interval

      if y % MAJOR_GRIDLINE_INTERVAL == 0:                        # sort major from minor
        accum = major_lines_accum
      else:
        accum = minor_lines_accum

      accum.append( [ [ -x_halfwidth, y ], [ x_halfwidth, y ] ] )     # positive-side gridline
      accum.append( [ [ -x_halfwidth, -y ], [ x_halfwidth, -y ] ] )   # negative-side gridline

    # draw the gridlines
    self.current_frame.add_lines( major_lines_accum,          # draw major gridlines
                      linewidth = self._meters_per_pixel(),
                      color = "black",
                      alpha = 0.2 )
    self.current_frame.add_lines( minor_lines_accum,          # draw minor gridlines
                      linewidth = self._meters_per_pixel(),
                      colro = "black",
                      alpha = 0.1 )


  def _meters_per_pixel( self ):
    return float( WORLD_WIDTH ) / float( VIEW_PORT_PIX_W )
