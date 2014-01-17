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





from math import *
from polygon import *
from pose import *

class RectangleObstacle:

  def __init__( self, width, height, pose ):
    self.pose = pose
    self.width = width
    self.height = height

    # define the geometry
    halfwidth_x = width * 0.5
    halfwidth_y = height * 0.5
    vertexes = [  [  halfwidth_x,  halfwidth_y ],
                  [  halfwidth_x, -halfwidth_y ],
                  [ -halfwidth_x, -halfwidth_y ],
                  [ -halfwidth_x,  halfwidth_y ] ]
    self.geometry = Polygon( vertexes )
    self.global_geometry = Polygon( vertexes ).get_transformation_to_pose( self.pose )
