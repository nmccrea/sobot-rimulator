#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
from sensor import *

class WheelEncoder( Sensor ):

  def __init__( self, ticks_per_rev ):
    self.ticks_per_rev = ticks_per_rev
    self.tick_count = 0

  # update the tick count for this wheel encoder
  # takes a float representing the number of forward revolutions made
  def step_revolutions( self, revolutions ):
    self.tick_count += int( revolutions * self.ticks_per_rev )

  def read( self ):
    return self.tick_count
