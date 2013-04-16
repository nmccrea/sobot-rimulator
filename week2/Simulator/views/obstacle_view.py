#!/usr/bin/python
# -*- Encoding: utf-8 -*

import Euv.Shapes as Shapes
import utils.linalg2_util as linalg

class ObstacleView:

  def __init__( self, viewer, obstacle ):
    self.viewer = viewer
    self.obstacle = obstacle

  def draw_obstacle_to_frame( self, frame ):
    obstacle = self.obstacle

    # grab the obstacle pose
    obstacle_pos, obstacle_theta = obstacle.pose.vunpack()

    # draw the obstacle to the frame
    obstacle_poly = obstacle.global_geometry.vertexes
    frame.add_polygons( [ obstacle_poly ],
                        color = "red",
                        alpha = 0.7 )
