#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import linalg2_util as linalg

from sim_exceptions.collision_exception import *

class Physics():

  def __init__( self, world ):
    # the world this physics engine acts on
    self.world = world

  def apply_physics( self ):
    self._test_for_collisions()

  # test the world for existing collisions with solids
  # raises a CollisionException if one occurs
  def _test_for_collisions( self ):
    colliders = self.world.colliders()
    collidables = self.world.collidables()

    for collider in colliders:
      for collidable in collidables:
        if collider is not collidable: # don't test an object against itself
          # it is currently safe to assume that all geometries are polygons
          polygon1 = collider.global_geometry
          polygon2 = collidable.global_geometry
          if self._convex_polygon_intersect_test( polygon1, polygon2 ):
            raise CollisionException()



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
