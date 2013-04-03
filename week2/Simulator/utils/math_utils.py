#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

def rotate_vector( x, y, theta ):
  sin_theta = sin( theta )
  cos_theta = cos( theta )
  
  x_new = x*cos_theta - y*sin_theta
  y_new = x*sin_theta + y*cos_theta

  return x_new, y_new

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
