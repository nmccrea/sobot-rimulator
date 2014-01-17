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
from pose import *

class DifferentialDriveDynamics:
  
  def __init__( self, wheel_radius, wheel_base_length):
    self.wheel_radius = wheel_radius
    self.wheel_base_length = wheel_base_length
  
  # apply physical dynamics to the given representations of moving parts
  def apply_dynamics( self, v_l, v_r, d_t,                                # dynamics parameters
                            pose, wheel_encoders ):                       # the moving parts

    # calculate the change in wheel angle (in radians)
    d_angle_left  = d_t * v_l
    d_angle_right = d_t * v_r
    
    # calculate the distance traveled
    wheel_meters_per_rad = self.wheel_radius
    d_left_wheel = d_angle_left * wheel_meters_per_rad
    d_right_wheel = d_angle_right * wheel_meters_per_rad
    d_center = ( d_left_wheel + d_right_wheel ) / 2.0
    
    # calculate the new pose
    old_x, old_y, old_theta = pose.sunpack()
    new_x = old_x + ( d_center * cos( old_theta ) )
    new_y = old_y + ( d_center * sin( old_theta ) )
    new_theta = old_theta + ( ( d_right_wheel - d_left_wheel ) / self.wheel_base_length )
    
    # calculate the number of rotations each wheel has made
    revolutions_left  = d_angle_left / ( 2*pi )
    revolutions_right = d_angle_right / ( 2*pi )
    
    # update the state of the moving parts
    pose.supdate( new_x, new_y, new_theta )
    wheel_encoders[0].step_revolutions( revolutions_left )
    wheel_encoders[1].step_revolutions( revolutions_right )
