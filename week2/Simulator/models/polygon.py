#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import linalg2_util as linalg

class Polygon:

  def __init__( self, vertexes ):
    self.vertexes = vertexes # a list of 2-dimensional vectors
  
  # return a copy of this polygon transformed to the given pose
  def get_transformation_to_pose( self, pose ):
    p_pos, p_theta = pose.vunpack()
    return Polygon( linalg.rotate_and_translate_vectors( self.vertexes, p_theta, p_pos ) )
  
  # get a list of of this polygon's edges as vertex pairs
  def edges( self ):
    vertexes = self.vertexes

    edges = []
    n = len( vertexes )
    for i in range( n ):
      edges.append( [ vertexes[i], vertexes[(i+1)%n] ] )

    return edges

  # get the number of edges of this polygon
  def numedges( self ):
    return len( self.vertexes )
