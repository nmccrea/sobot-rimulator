#!/usr/bin/python
# -*- Encoding: utf-8 -*

# Python implementation of the Week 2 exercise.

from random import *

from models.polygon import *
from models.rectangle_obstacle import *
from models.robot import *
from models.world import *
from views.world_view import *

from sim_exceptions.collision_exception import *

REFRESH_RATE = 20.0 # hertz

# random environment parameters
OBS_MIN_DIM = 0.1           # meters
OBS_MAX_DIM = 2.5           # meters
OBS_MAX_COMBINED_DIM = 2.6  # meters
OBS_MIN_COUNT = 10
OBS_MAX_COUNT = 50
OBS_MIN_DIST = 0.4          # meters
OBS_MAX_DIST = 6.0          # meters
GOAL_MIN_DIST = 2.0         # meters
GOAL_MAX_DIST = 4.0         # meters

class Week2Simulator:

  def __init__( self ):
    # timing control
    self.period = 1.0 / REFRESH_RATE  # seconds

    # create the simulation world
    self.world = World( self.period )
    self.world_view = WorldView()

    # create the robot
    robot = Robot()
    self._add_robot( robot )

    # generate a random environment parameters
    obstacles, goal = self._random_init( robot.global_geometry )
    # override random initialization here

    # add the generated obstacles
    for o in obstacles:
      width, height, x, y, theta = o
      self._add_obstacle( RectangleObstacle(  width, height,
                                              Pose( x, y, theta ) ) )

    # program the robot supervisor
    supervisor = robot.supervisor
    supervisor.goal = goal
    
    # run the simulation
    self.run_sim()

  def run_sim( self ):
    # initialize timing control
    next_refresh_time = time.time() + self.period

    # loop the simulation
    while self.world.world_time < 100:
      # increment the simulation
      try:
        self.world.step()
      except CollisionException:
        print "\n\nCOLLISION!\n\n"
        break
      except GoalReachedException:
        print "\n\nGOAL REACHED!\n\n"
        break

      # render the current state
      self.world_view.render_frame()

      # pause the simulation until the next refresh time
      while time.time() < next_refresh_time: time.sleep( 0 )  # loop sleep until time to refresh
      next_refresh_time = time.time() + self.period           # update next refresh time
    
    # pause the GUI thread ( app crashes otherwise ) 
    self.world_view.wait()

  def _add_robot( self, robot ):
    self.world.add_robot( robot )
    self.world_view.add_robot( robot )

  def _add_obstacle( self, obstacle ):
    self.world.add_obstacle( obstacle )
    self.world_view.add_obstacle( obstacle )

  def _random_init( self, robot_geometry ):
    # OBSTACLE PARAMS
    obs_min_dim = OBS_MIN_DIM
    obs_max_dim = OBS_MAX_DIM
    obs_max_combined_dim = OBS_MAX_COMBINED_DIM
    obs_min_count = OBS_MIN_COUNT
    obs_max_count = OBS_MAX_COUNT
    obs_min_dist = OBS_MIN_DIST
    obs_max_dist = OBS_MAX_DIST

    # GOAL PARAMS
    goal_min_dist = GOAL_MIN_DIST
    goal_max_dist = GOAL_MAX_DIST


    # BUILD RANDOM ELEMENTS
    obstacles = []
    obs_dim_range = obs_max_dim - obs_min_dim
    obs_dist_range = obs_max_dist - obs_min_dist
    goal_dist_range = goal_max_dist - goal_min_dist

    # generate the obstacles
    num_obstacles = randrange( obs_min_count, obs_max_count+1 )
    while len( obstacles ) < num_obstacles:
      
      # generate dimensions
      width = obs_min_dim + ( random() * obs_dim_range )
      height = obs_min_dim + ( random() * obs_dim_range )
      while width + height > obs_max_combined_dim:
        height = obs_min_dim + ( random() * obs_dim_range )
      
      # generate position 
      dist = obs_min_dist + ( random() * obs_dist_range )
      phi = -pi + ( random() * 2 * pi )
      x = dist * sin( phi )
      y = dist * cos( phi )
      
      # generate orientation
      theta = -pi + ( random() * 2 * pi )

      # test if the obstacle overlaps the robot
      obstacle = RectangleObstacle( width, height,
                                    Pose( x, y, theta ) )

      if self._convex_polygon_intersect_test( robot_geometry, obstacle.global_geometry ) == False:
        obstacles.append( [ width, height, x, y, theta ] )

    # generate the goal
    goal = None
    while goal == None:
      dist = goal_min_dist + ( random() * goal_dist_range )
      phi = -pi + ( random() * 2 * pi )
      x = dist * sin( phi )
      y = dist * cos( phi )
      goal = [ x, y ]

      # make sure the goal is not too close to any obstacles
      # NOTE: this is currently very hacky and inefficient
      r = 0.2
      n = 12
      goal_test_geometry = []
      for i in range( n ):
        goal_test_geometry.append(
            [ x + r*cos( i * 2*pi/n ),
              y + r*sin( i * 2*pi/n ) ] )
      goal_test_geometry = Polygon( goal_test_geometry )
      for obs in obstacles:
        width, height, x, y, theta = obs
        obstacle = RectangleObstacle( width, height,
                                      Pose( x, y, theta ) )
        if self._convex_polygon_intersect_test( goal_test_geometry, obstacle.global_geometry ):
          goal = None
          break

    print "\n\n"
    print "TO RECREATE THIS ENVIRONMENT, USE THE FOLLOWING DROP-IN CODE:"
    print "obstacles, goal = " + str( obstacles ) + ", " + str( goal )
    print "\n\n"

    return obstacles, goal

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



# RUN THE SIM:
Week2Simulator()
