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

  # test the world for existing collisions with solids
  # raises a CollisionException if one occurs
  def _detect_collisions( self ):
    colliders = self.world.colliders()
    solids = self.world.solids()

    for collider in colliders:
      for solid in solids:
        if collider is not solid: # don't test an object against itself
          # NOTE: it is currently safe to assume that all geometries are polygons
          polygon1 = collider.global_geometry
          polygon2 = solid.global_geometry
          if self._check_nearness( polygon1, polygon2 ): # don't bother testing objects that are not near each other

            if self._convex_polygon_intersect_test( polygon1, polygon2 ):
              raise CollisionException()

  def _update_proximity_sensors( self ):
    False

    # TODO:
    # for each robot r
    #   for each proximity sensor p
    #     set nearest_distance to infinity
    #
    #     for each solid c NOT r
    #       if p is "near" c
    #         find the intersection of p's line segment with c's polygon
    #         if distance from p to this point is less than nearest_distance
    #           set nearest_distance to this distance
    #
    #     set p's proximity to nearest_distance

  # a fast test to determine if two polygons might be touching
  def _check_nearness( self, polygon1, polygon2 ):
    c1, r1 = polygon1.bounding_circle
    c2, r2 = polygon2.bounding_circle
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

  # return the point at which the given line segments intersect
  def _line_segment_intersection( self, line1, line2 ):
    nointersect_token = None    # return this if the line segments do not intersect

    p1, s1 = line1[0],   linalg.sub( line1[1], line1[0] )
    p2, s2 = line2[0],   linalg.sub( line2[1], line2[0] )

    s1xs2 = float( linalg.cross( s1, s2 ) )
    if s1xs2 == 0.0: return nointersect_token
    p2subp1 = linalg.sub( p2, p1 )

    r1 = linalg.cross( p2subp1, s2 ) / s1xs2
    r2 = linalg.cross( p2subp1, s1 ) / s1xs2

    if r1 >= 0.0 and r1 <= 1.0 and r2 >= 0.0 and r2 <= 1.0:
      return linalg.add( p1, linalg.scale( s1, r1 ) )
    else:
      return nointersect_token

  def _directed_line_segment_polygon_intersection( self, line, polygon ):
    # TODO: return the point nearest to the beginning of a line segement where it intersects a polygon
    False
