#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import math_utils

class Pose:

  def __init__( self, x, y, phi ):
    self.x = x
    self.y = y
    self.phi = math_utils.normalize_angle( phi )

  def unpack( self ):
    return self.x, self.y, self.phi
