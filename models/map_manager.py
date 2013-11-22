#!/usr/bin/python
# -*- Encoding: utf-8 -*

from random import *
import pickle

from models.polygon import *
from models.rectangle_obstacle import *

import utils.geometrics_util as geometrics

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

class MapManager:
  
  def __init__( self ):
    self.current_obstacles = []
    self.current_goal = None

  def random_map( self, robot_geometry ):
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

      if geometrics.convex_polygon_intersect_test( robot_geometry, obstacle.global_geometry ) == False:
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
        if geometrics.convex_polygon_intersect_test( goal_test_geometry, obstacle.global_geometry ):
          goal = None
          break
    
    self.current_obstacles = obstacles
    self.current_goal = goal
    
    
  def save_map( self, filename ):
    with open( filename, 'wb' ) as file:
      pickle.dump( self.current_obstacles, file )
      pickle.dump( self.current_goal, file )
      
      
  def load_map( self, filename ):
    with open( filename, 'rb' ) as file:
      self.current_obstacles = pickle.load( file )
      self.current_goal = pickle.load( file )