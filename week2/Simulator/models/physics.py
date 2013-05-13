#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import linalg2_util as linalg

from sim_exceptions.collision_exception import *

class Physics():

  def __init__( self, world ):
    # the world this physics engine acts on
    self.world = world

  def apply_physics( self ):
    self._detect_collisions()
    self._update_proximity_sensors()

  # test the world for existing collisions with solids
  # raises a CollisionException if one occurs
  def _detect_collisions( self ):
    colliders = self.world.colliders()
    solids = self.world.solids()

    for collider in colliders:
      polygon1 = collider.global_geometry     # polygon1

      for solid in solids:
        if solid is not collider: # don't test an object against itself
          polygon2 = solid.global_geometry    # polygon2
          
          if self._check_nearness( polygon1, polygon2 ): # don't bother testing objects that are not near each other
            if self._convex_polygon_intersect_test( polygon1, polygon2 ):
              raise CollisionException()

  # update any proximity sensors that are in range of solid objects
  def _update_proximity_sensors( self ):
    robots = self.world.robots
    solids = self.world.solids()
    
    for robot in robots:
      sensors = robot.ir_sensors

      for sensor in sensors:
        dmin = float('inf')
        detector_line = sensor.detector_line

        for solid in solids:

          if solid is not robot:  # assume that the sensor does not detect it's own robot
            solid_polygon = solid.global_geometry
            
            if self._check_nearness( detector_line, solid_polygon ): # don't bother testing objects that are not near each other
              intersection_exists, intersection, d = self._directed_line_segment_polygon_intersection( detector_line, solid_polygon )
              
              if intersection_exists and d < dmin:
                dmin = d

        # if there is an intersection, update the sensor with the new delta value
        if dmin != float('inf'):
          sensor.detect( dmin )

  # a fast test to determine if two geometries might be touching
  def _check_nearness( self, geometry1, geometry2 ):
    c1, r1 = geometry1.bounding_circle
    c2, r2 = geometry2.bounding_circle
    return linalg.distance( c1, c2 ) <= r1 + r2

  # determine if two convex polygons intersect
  def _convex_polygon_intersect_test( self, polygon1, polygon2 ):
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
      minA, maxA = self._range_project_polygon( projection_axis, polygonA )
      minB, maxB = self._range_project_polygon( projection_axis, polygonB )

      # test if projections overlap
      if minA > maxB or maxA < minB:
        intersect = False 
      edge_index += 1

    return intersect


  # get the min and max dot-products of a projection axis and the vertexes of a polygon - this is sufficient for overlap comparison
  def _range_project_polygon( self, axis_vector, polygon ):
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
  def _line_segment_intersection( self, line1, line2 ):
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
  def _directed_line_segment_polygon_intersection( self, line_segment, test_polygon ):
    test_line = line_segment.vertexes # get the raw line segment
    dmin = float('inf')
    intersection = None
    
    # a dumb algorithm that tests every edge of the polygon
    for edge in test_polygon.edges():
      intersection_exists, _intersection, d = self._line_segment_intersection( test_line, edge )

      if intersection_exists and d < dmin:
        dmin = d
        intersection = _intersection

    if dmin != float('inf'):
      return True, intersection, dmin
    else:
      return False, None, None
