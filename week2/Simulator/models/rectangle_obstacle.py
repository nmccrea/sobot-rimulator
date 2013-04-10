#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
from polygon import *
from pose import *

class RectangleObstacle:

  def __init__( self, width, height, pose ):
    self.pose = pose
    self.width = width
    self.height = height

    # define the geometry
    halfwidth_x = width * 0.5
    halfwidth_y = height * 0.5
    vertexes = [  [  halfwidth_x,  halfwidth_y ],
                  [  halfwidth_x, -halfwidth_y ],
                  [ -halfwidth_x, -halfwidth_y ],
                  [ -halfwidth_x,  halfwidth_y ] ]
    self.geometry = Polygon( vertexes )
