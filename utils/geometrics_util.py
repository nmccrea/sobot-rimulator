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





import utils.linalg2_util as linalg

# a fast test to determine if two geometries might be touching
def check_nearness( geometry1, geometry2 ):
  c1, r1 = geometry1.bounding_circle
  c2, r2 = geometry2.bounding_circle
  return linalg.distance( c1, c2 ) <= r1 + r2

# determine if two convex polygons intersect
def convex_polygon_intersect_test( polygon1, polygon2 ):
  # assign polygons according to which has fewest sides - we will test against the polygon with fewer sides first
  if polygon1.numedges() <= polygon2.numedges():
    polygonA = polygon1
    polygonB = polygon2
  else:
    polygonA = polygon2
    polygonB = polygon1

  # perform Seperating Axis Test
  intersect = True
  edge_index = 0
  edges = polygonA.edges() + polygonB.edges()
  while intersect == True and edge_index < len( edges ): # loop through the edges of polygonA searching for a separating axis
    # get an axis normal to the current edge
    edge = edges[ edge_index ]
    edge_vector = linalg.sub( edge[1], edge[0] )
    projection_axis = linalg.lnormal( edge_vector )

    # get the projection ranges for each polygon onto the projection axis
    minA, maxA = range_project_polygon( projection_axis, polygonA )
    minB, maxB = range_project_polygon( projection_axis, polygonB )

    # test if projections overlap
    if minA > maxB or maxA < minB:
      intersect = False 
    edge_index += 1

  return intersect


# get the min and max dot-products of a projection axis and the vertexes of a polygon - this is sufficient for overlap comparison
def range_project_polygon( axis_vector, polygon ):
  vertexes = polygon.vertexes

  c = linalg.dot( axis_vector, vertexes[0] )
  minc = c
  maxc = c
  for i in range( 1, len( vertexes ) ):
    c = linalg.dot( axis_vector, vertexes[i] )

    if c < minc:    minc = c
    elif c > maxc:  maxc = c

  return minc, maxc

# test two line segments for intersection
# takes raw line segments, i.e. a pair of vectors
# returns
#   intersection_exists - boolean         - value indicating whether an intersection was found
#   intersection        - vector          - the intersection point, or None if none was found
#   d                   - float in [0,1]  - distance along line1 at which the intersection occurs
def line_segment_intersection( line1, line2 ):
  # see http://stackoverflow.com/questions/563198
  nointersect_symbol = ( False, None, None )

  p1, r1 = line1[0],   linalg.sub( line1[1], line1[0] )
  p2, r2 = line2[0],   linalg.sub( line2[1], line2[0] )

  r1xr2 = float( linalg.cross( r1, r2 ) )
  if r1xr2 == 0.0: return nointersect_symbol
  p2subp1 = linalg.sub( p2, p1 )

  d1 = linalg.cross( p2subp1, r2 ) / r1xr2
  d2 = linalg.cross( p2subp1, r1 ) / r1xr2

  if d1 >= 0.0 and d1 <= 1.0 and d2 >= 0.0 and d2 <= 1.0:
    return True, linalg.add( p1, linalg.scale( r1, d1 ) ), d1
  else:
    return nointersect_symbol

# test a line segment and a polygon for intersection
# returns:
#   intersection_exists - boolean         - value indicating whether an intersection was found
#   intersection        - vector          - the intersection point, or None if none was found
#   d                   - float in [0, 1] - distance along the thest line at which the intersection occurs
def directed_line_segment_polygon_intersection( line_segment, test_polygon ):
  test_line = line_segment.vertexes # get the raw line segment
  dmin = float('inf')
  intersection = None
  
  # a dumb algorithm that tests every edge of the polygon
  for edge in test_polygon.edges():
    intersection_exists, _intersection, d = line_segment_intersection( test_line, edge )

    if intersection_exists and d < dmin:
      dmin = d
      intersection = _intersection

  if dmin != float('inf'):
    return True, intersection, dmin
  else:
    return False, None, None
