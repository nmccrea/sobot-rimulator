#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import linalg2_util as linalg
from sim_exceptions.goal_reached_exception import *

# state enumerations
STATE_AT_GOAL         = 0
STATE_GO_TO_GOAL      = 1
STATE_AVOID_OBSTACLES = 2
STATE_GTG_AND_AO      = 3

# event parameters
D_STOP = 0.05   # meters from goal
D_AVOID = 0.15  # meters from obstacle

class SupervisorStateMachine:

  def __init__( self, supervisor ):
    self.supervisor = supervisor

    # initialize state
    self.transition_to_state_go_to_goal()

  def update_state( self ):
    if self.current_state == STATE_GO_TO_GOAL:        self.execute_state_go_to_goal()
    elif self.current_state == STATE_AVOID_OBSTACLES: self.execute_state_avoid_obstacles()
    else: raise Exception( "undefined supervisor state" )


  # === STATE PROCEDURES ===
  def execute_state_go_to_goal( self ):
    print "EXECUTING go_to_goal"
    if self.condition_at_goal():          self.transition_to_state_at_goal()
    elif self.condition_at_obstacle():  self.transition_to_state_avoid_obstacles()

  def execute_state_avoid_obstacles( self ):
    print "EXECUTING avoid_obstacles"
    if self.condition_no_obstacle():    self.transition_to_state_go_to_goal()


  # === STATE TRANSITIONS ===
  def transition_to_state_at_goal( self ):
    print "TRANSITIONING TO STATE: AT_GOAL"
    self.current_state = STATE_AT_GOAL
    raise GoalReachedException()

  def transition_to_state_avoid_obstacles( self ):
    print "TRANSITIONING TO STATE: AVOID_OBSTACLES"
    self.current_state = STATE_AVOID_OBSTACLES
    self.supervisor.current_controller = self.supervisor.avoid_obstacles_controller

  def transition_to_state_go_to_goal( self ):
    print "TRANSITIONING TO STATE: GO_TO_GOAL"
    self.current_state = STATE_GO_TO_GOAL
    self.supervisor.current_controller = self.supervisor.go_to_goal_controller


  # === CONDITIONS ===
  def condition_at_goal( self ):
    print "TESTING at_goal"
    return linalg.distance( self.supervisor.estimated_pose.vposition(), self.supervisor.goal ) < D_STOP

  def condition_at_obstacle( self ):
    print "TESTING at_obstacle"
    for d in self._forward_sensor_distances():
      if d < D_AVOID: return True
    return False

  def condition_no_obstacle( self ):
    print "TESTING no_obstacle"
    for d in self._forward_sensor_distances():
      if d < D_AVOID: return False
    return True
    
 
  # === helper methods ===   
  def _forward_sensor_distances( self ):
    return self.supervisor.proximity_sensor_distances[1:7]
