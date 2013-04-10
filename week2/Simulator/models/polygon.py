#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import linalg2_util as linalg

class Polygon:

  def __init__( self, vertexes ):
    self.vertexes = vertexes # a list of 2-dimensional vectors

  def get_transformation_to_pose( self, pose ):
    p_pos, p_theta = pose.vunpack()
    return linalg.rotate_and_translate_vectors( self.vertexes, p_theta, p_pos )
