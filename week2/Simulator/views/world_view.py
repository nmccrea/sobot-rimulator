#!/usr/bin/python
# -*- Encoding: utf-8 -*
# Python implementation of the Week 2 exercise.

import Euv.EuvGtk as Euv
import Euv.Frame as Frame
import Euv.Shapes as Shapes
import Euv.Color as Color
from robot_view import *

class WorldView:

  def __init__( self ):
    # create viewer
    self.viewer = Euv.Viewer( size = (300, 300),
                          view_port_center = (0, 0),
                          view_port_width = 3,
                          flip_y = True )

    # initialize the current frame object
    self.current_frame = Frame.Frame()

    # initialize list of robots views
    self.robot_views = []

  def add_robot( self, robot ):
    robot_view = RobotView( self.viewer, robot )
    self.robot_views.append( robot_view )

  def render_frame( self ):
    # draw all the robots
    for robot_view in self.robot_views:
      robot_view.draw_robot_to_frame( self.current_frame )

    # cycle the frame
    self.viewer.add_frame( self.current_frame )   # push the current frame
    self.current_frame = Frame.Frame()            # prepare the next frame

  def wait( self ):
    self.viewer.wait()
