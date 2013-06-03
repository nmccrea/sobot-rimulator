#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

from utils import linalg2_util as linalg
from utils import math_util

class AvoidObstaclesController:

  def __init__( self, supervisor ):
    # bind the supervisor
    self.supervisor = supervisor

    # sensor gains (weights)
    self.sensor_gains = [   1.0-( (0.9*abs(p.theta)) / pi )   for p in supervisor.sensor_placements() ]

    # control gains
    self.kP = 5.0
    self.kI = 0.5
    self.kD = 0.1
    
    # stored values - for computing next results
    self.prev_time = 0.0
    self.prev_eP = 0.0
    self.prev_eI = 0.0

  def execute( self ):
    False
