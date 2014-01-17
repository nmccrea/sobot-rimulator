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





from utils import linalg2_util as linalg
from geometry import *

class Polygon( Geometry ):

  def __init__( self, vertexes ):
    self.vertexes = vertexes  # a list of 2-dimensional vectors

    # define the centerpoint and radius of a circle containing this polygon
    # value is a tuple of the form ( [ cx, cy ], r )
    # NOTE: this may not be the "minimum bounding circle"
    self.bounding_circle = self._bounding_circle()

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

  # get the centerpoint and radius for a circle that completely contains this polygon
  def _bounding_circle( self ):
    # NOTE: this method is meant to give a quick bounding circle
    #   the circle calculated may not be the "minimum bounding circle"

    c = self._centroidish()
    r = 0.0
    for v in self.vertexes:
      d = linalg.distance( c, v )
      if d > r: r = d

    return c, r

  # approximate the centroid of this polygon
  def _centroidish( self ):
    # NOTE: this method is meant to give a quick and dirty approximation of center of the polygon
    #   it returns the average of the vertexes
    #   the actual centroid may not be equivalent

    n = len( self.vertexes )
    x = 0.0
    y = 0.0
    for v in self.vertexes:
      x += v[0]
      y += v[1]
    x /= n
    y /= n

    return [ x, y ]
