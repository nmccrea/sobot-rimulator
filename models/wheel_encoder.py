# Sobot Rimulator - A Robot Programming Tool
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Email mccrea.engineering@gmail.com for questions, comments, or to report bugs.





from math import *
from sensor import *

class WheelEncoder( Sensor ):

  def __init__( self, ticks_per_rev ):
    self.ticks_per_rev = ticks_per_rev
    self.real_revs = 0.0
    self.tick_count = 0

  # update the tick count for this wheel encoder
  # takes a float representing the number of forward revolutions made
  def step_revolutions( self, revolutions ):
    self.real_revs += revolutions
    self.tick_count = int( self.real_revs * self.ticks_per_rev )

  def read( self ):
    return self.tick_count
