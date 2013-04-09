#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

def rotate_vector( x, y, theta ):
  sin_theta = sin( theta )
  cos_theta = cos( theta )
  
  x_new = x*cos_theta - y*sin_theta
  y_new = x*sin_theta + y*cos_theta

  return x_new, y_new

def dot( a, b ):
  return a[0]*b[0] + a[1]*b[1]
