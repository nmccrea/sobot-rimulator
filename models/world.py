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





import time
from physics import *

class World:

  def __init__( self, dt = 0.05 ):
    # initialize physics engine
    self.physics = Physics( self )

    # initialize world time
    self.world_time = 0.0 # seconds
    self.dt = dt          # seconds
    
    # initialize lists of world objects
    self.supervisors = []
    self.robots = []
    self.obstacles = []

  # step the simulation through one time interval
  def step( self ):
    dt = self.dt
    
    # step all the robots
    for robot in self.robots:
      # step robot motion
      robot.step_motion( dt )

    # apply physics interactions
    self.physics.apply_physics()

    # NOTE: the supervisors must run last to ensure they are observing the "current" world
    # step all of the supervisors
    for supervisor in self.supervisors:
      supervisor.step( dt )

    # increment world time
    self.world_time += dt

  def add_robot( self, robot ):
    self.robots.append( robot )
    self.supervisors.append( robot.supervisor )

  def add_obstacle( self, obstacle ):
    self.obstacles.append( obstacle )

  # return all objects in the world that might collide with other objects in the world during simulation
  def colliders( self ):
    # moving objects only
    return self.robots  # as obstacles are static we should not test them against each other

  # return all solids in the world
  def solids( self ):
    return self.robots + self.obstacles
