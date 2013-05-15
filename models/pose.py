#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import math_util

class Pose:

  def __init__( self, *args ):
    if len( args ) == 2: # initialize using a vector ( vect, theta )
      vect = args[0]
      theta = args[1]

      self.x = vect[0]
      self.y = vect[1]
      self.theta = math_util.normalize_angle( theta )
    elif len( args ) == 3: #initialize using scalars ( x, y theta )
      x = args[0]
      y = args[1]
      theta = args[2]

      self.x = x
      self.y = y
      self.theta = math_util.normalize_angle( theta )
    else:
      raise TypeError( "Wrong number of arguments. Pose requires 2 or 3 arguments to initialize" )

  # update pose using a vector
  def vupdate( self, vect, theta ):
    self.x = vect[0]
    self.y = vect[1]
    self.theta = theta

  # update pose using scalars
  def supdate( self, x, y, theta ):
    self.x = x
    self.y = y
    self.theta = theta

  # return the constituents of this pose with location as a vector
  def vunpack( self ):
    return [ self.x, self.y ], self.theta

  # return the constituents of this pose as all scalars
  def sunpack( self ):
    return self.x, self.y, self.theta
