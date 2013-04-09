#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import math_util

class Pose:

  def __init__( self, x, y, theta ):
    self.x = x
    self.y = y
    self.theta = math_util.normalize_angle( theta )

  def unpack( self ):
    return self.x, self.y, self.theta
