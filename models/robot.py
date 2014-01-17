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
from differential_drive_dynamics import *
from polygon import *
from pose import *
from proximity_sensor import *
from robot_supervisor_interface import *
from supervisor import *
from wheel_encoder import *

# Khepera III Properties
K3_WHEEL_RADIUS = 0.021         # meters
K3_WHEEL_BASE_LENGTH = 0.0885   # meters
K3_WHEEL_TICKS_PER_REV = 2765
K3_MAX_WHEEL_DRIVE_RATE = 15.0  # rad/s

# Khepera III Dimensions
K3_BOTTOM_PLATE = [[ -0.024,  0.064 ],
                   [  0.033,  0.064 ],
                   [  0.057,  0.043 ],
                   [  0.074,  0.010 ],
                   [  0.074, -0.010 ],
                   [  0.057, -0.043 ],
                   [  0.033, -0.064 ],
                   [ -0.025, -0.064 ],
                   [ -0.042, -0.043 ],
                   [ -0.048, -0.010 ],
                   [ -0.048,  0.010 ],
                   [ -0.042,  0.043 ]]

K3_SENSOR_MIN_RANGE = 0.02
K3_SENSOR_MAX_RANGE = 0.2
K3_SENSOR_POSES = [[ -0.038,  0.048,  128 ], # x, y, theta_degrees
                   [  0.019,  0.064,  75  ],
                   [  0.050,  0.050,  42  ],
                   [  0.070,  0.017,  13  ],
                   [  0.070, -0.017, -13  ],
                   [  0.050, -0.050, -42  ],
                   [  0.019, -0.064, -75  ],
                   [ -0.038, -0.048, -128 ],
                   [ -0.048,  0.000,  180 ]]

class Robot: # Khepera III robot 
  
  def __init__( self ):
    # geometry
    self.geometry = Polygon( K3_BOTTOM_PLATE )
    self.global_geometry = Polygon( K3_BOTTOM_PLATE ) # actual geometry in world space

    # wheel arrangement
    self.wheel_radius = K3_WHEEL_RADIUS             # meters
    self.wheel_base_length = K3_WHEEL_BASE_LENGTH   # meters

    # pose
    self.pose = Pose( 0.0, 0.0, 0.0 )

    # wheel encoders
    self.left_wheel_encoder = WheelEncoder( K3_WHEEL_TICKS_PER_REV )
    self.right_wheel_encoder = WheelEncoder( K3_WHEEL_TICKS_PER_REV )
    self.wheel_encoders = [ self.left_wheel_encoder, self.right_wheel_encoder ]
    
    # IR sensors
    self.ir_sensors = []
    for _pose in K3_SENSOR_POSES:
      ir_pose = Pose( _pose[0], _pose[1], radians( _pose[2] ) )
      self.ir_sensors.append(
          ProximitySensor( self, ir_pose, K3_SENSOR_MIN_RANGE, K3_SENSOR_MAX_RANGE, radians( 20 ) ) )

    # dynamics
    self.dynamics = DifferentialDriveDynamics( self.wheel_radius, self.wheel_base_length )

    # supervisor
    self.supervisor = Supervisor( RobotSupervisorInterface( self ),
                                  K3_WHEEL_RADIUS, K3_WHEEL_BASE_LENGTH, K3_WHEEL_TICKS_PER_REV, K3_SENSOR_POSES, K3_SENSOR_MAX_RANGE )
    
    ## initialize state
    # set wheel drive rates (rad/s)
    self.left_wheel_drive_rate = 0.0
    self.right_wheel_drive_rate = 0.0

  # simulate the robot's motion over the given time interval
  def step_motion( self, dt ):
    v_l = self.left_wheel_drive_rate
    v_r = self.right_wheel_drive_rate

    # apply the robot dynamics to moving parts
    self.dynamics.apply_dynamics( v_l, v_r, dt,
                                  self.pose, self.wheel_encoders )

    # update global geometry
    self.global_geometry = self.geometry.get_transformation_to_pose( self.pose )
    
    # update all of the sensors
    for ir_sensor in self.ir_sensors:
      ir_sensor.update_position()
  
  # set the drive rates (angular velocities) for this robot's wheels in rad/s 
  def set_wheel_drive_rates( self, v_l, v_r ):
    # simulate physical limit on drive motors
    v_l = min( K3_MAX_WHEEL_DRIVE_RATE, v_l )
    v_r = min( K3_MAX_WHEEL_DRIVE_RATE, v_r )

    # set drive rates
    self.left_wheel_drive_rate = v_l
    self.right_wheel_drive_rate = v_r
