#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
from sensor import *

class WheelEncoder( Sensor ):

  def __init__( self,
                wheel_radius,
                ticks_per_rev ):
    self.wheel_radius = wheel_radius
    self.ticks_per_rev = ticks_per_rev

    self.tick_count = 0

  def update_ticks( self, wheel_velocity, dt ):
    # wheel_velocity = rad/s
    # dt = s
    d_rotation = wheel_velocity * dt
    d_ticks = ( d_rotation / (2*pi) ) * self.ticks_per_rev
    self.tick_count += floor( d_ticks )

  def ticks_to_revolutions( self ):
    return self.tick_count / self.ticks_per_rev

  def ticks_to_distance( self ):
    revs = self.ticks_to_revolutions()
    return revs * 2 * pi * self.wheel_radius

  def read( self ):
    return self.tick_count
