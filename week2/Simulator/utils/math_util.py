#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

def normalize_angle( theta ):
  if theta > pi:
    theta -= 2*pi
  elif theta < -pi:
    theta += 2*pi

  return theta
  
def frange( x, y, jump = 1.0 ):
  r = []
  while x < y:
    r.append( x )
    x += jump

  return r
