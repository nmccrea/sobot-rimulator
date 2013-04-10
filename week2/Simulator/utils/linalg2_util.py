#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *


# get the sum of two vectors
def add( a, b ):
  return [ a[0]+b[0], a[1]+b[1] ]

# get the dot-product of two vectors
def dot( a, b ):
  return a[0]*b[0] + a[1]*b[1]

# get the magnitude of a vector
def mag( a ):
  return sqrt( a[0]**2 + a[1]**2 )

# get the unit vector of a vector
def unit( a ):
  m = mag( a )
  return( [ a[0]/m, a[1]/m ] )

# get the right-hand unit normal of a vector
def runormal( a ):
  return unit( [ a[1], -a[0] ] )

# get the left-hand unit normal of a vector
def lunormal( a ):
  return unit( [ -a[1], a[0] ] )

# get the projection of vector a onto vector b
def proj( a, b ):
  scale = float( dot( a, b ) ) / ( b[0]**2 + b[1]**2 )
  return( [ scale*b[0], scale*b[1] ] )

# get the result of rotating a vector by theta radians
def rotate_vector( a, theta ):
  sin_theta = sin( theta )
  cos_theta = cos( theta )
  
  a0 = a[0]*cos_theta - a[1]*sin_theta
  a1 = a[0]*sin_theta + a[1]*cos_theta

  return [ a0, a1 ]

# get the result of rotating a set of vectors by theta radians
def rotate_vectors( vects, theta ):
  sin_theta = sin( theta )
  cos_theta = cos( theta )
  
  rotvects = []
  for a in vects:
    a0 = a[0]*cos_theta - a[1]*sin_theta
    a1 = a[0]*sin_theta + a[1]*cos_theta
    rotvects.append( [ a0, a1 ] )

  return rotvects

# get the result of rotating and translating a vector
def rotate_and_translate_vector( a, tvect, theta ):
  return add( rotate_vector( a, theta ), tvect )

# get the rsult of rotating and translating a set of vectors
def rotate_and_translate_vectors( vects, tvect, theta ):
  rtvects = []
  for a in rotate_vectors( vects, theta ):
    rtvects.append( add( a, tvect ) )

  return rtvects
