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

class ObstacleView:

  def __init__( self, viewer, obstacle ):
    self.viewer = viewer
    self.obstacle = obstacle

  def draw_obstacle_to_frame( self ):
    obstacle = self.obstacle

    # grab the obstacle pose
    obstacle_pos, obstacle_theta = obstacle.pose.vunpack()

    # draw the obstacle to the frame
    obstacle_poly = obstacle.global_geometry.vertexes
    self.viewer.current_frame.add_polygons( [ obstacle_poly ],
                                            color = "dark red",
                                            alpha = 0.4 )

    # === FOR DEBUGGING: ===
    # self._draw_bounding_circle_to_frame()

  def _draw_bounding_circle_to_frame( self ):
    c, r = self.obstacle.global_geometry.bounding_circle
    self.viewer.current_frame.add_circle( pos = c,
                                          radius = r,
                                          color = "black",
                                          alpha = 0.2 )
