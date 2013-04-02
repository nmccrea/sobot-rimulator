#!/usr/bin/python
# -*- Encoding: utf-8 -*

from pose import *

class RectangleObstacle:

  def __init__( self, pose, width, height ):
    self.pose = pose
    self.width = width
    self.height = height
