#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

# map the given angle to the equivalent angle in [ -pi, pi ]
def normalize_angle( theta ):
  if theta > pi:
    # subtracts a positive number of circles
    theta -= 2 * pi * int( ( theta + pi ) / ( 2 * pi ) )
  elif theta < -pi:
    # subtracts a negative number of circles
    theta -= 2 * pi * int( ( theta - pi ) / ( 2 * pi ) )

  return theta
  
def frange( x, y, jump = 1.0 ):
  r = []
  while x < y:
    r.append( x )
    x += jump

  return r
