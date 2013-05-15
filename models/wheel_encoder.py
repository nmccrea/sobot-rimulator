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

  def step_ticks( self, wheel_velocity, dt ):
    # wheel_velocity = rad/s
    # dt = s
    d_angle = wheel_velocity * dt
    d_ticks = ( d_angle / (2*pi) ) * self.ticks_per_rev
    self.tick_count += int( d_ticks )

  def read( self ):
    return self.tick_count
