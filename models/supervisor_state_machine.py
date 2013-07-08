#!/usr/bin/python
# -*- Encoding: utf-8 -*

from control_state import *
from utils import linalg2_util as linalg
from sim_exceptions.goal_reached_exception import *

# event parameters
D_STOP = 0.05     # meters from goal
D_CAUTION = 0.15  # meters from obstacle
D_DANGER = 0.06   # meters from obstacle

class SupervisorStateMachine:

  def __init__( self, supervisor ):
    self.supervisor = supervisor

    # initialize state
    self.transition_to_state_go_to_goal()

  def update_state( self ):
    if self.current_state == ControlState.GO_TO_GOAL:        self.execute_state_go_to_goal()
    elif self.current_state == ControlState.AVOID_OBSTACLES: self.execute_state_avoid_obstacles()
    elif self.current_state == ControlState.GTG_AND_AO:      self.execute_state_gtg_and_ao()
    else: raise Exception( "undefined supervisor state" )


  # === STATE PROCEDURES ===
  def execute_state_go_to_goal( self ):
    if self.condition_at_goal():        self.transition_to_state_at_goal()
    elif self.condition_at_obstacle():  self.transition_to_state_gtg_and_ao()

  def execute_state_avoid_obstacles( self ):
    if self.condition_at_goal():        self.transition_to_state_at_goal()
    if not self.condition_danger():     self.transition_to_state_gtg_and_ao()

  def execute_state_gtg_and_ao( self ):
    if self.condition_at_goal():        self.transition_to_state_at_goal()
    elif self.condition_danger():       self.transition_to_state_avoid_obstacles()
    elif self.condition_no_obstacle():  self.transition_to_state_go_to_goal()


  # === STATE TRANSITIONS ===
  def transition_to_state_at_goal( self ):
    self.current_state = ControlState.AT_GOAL
    raise GoalReachedException()

  def transition_to_state_avoid_obstacles( self ):
    self.current_state = ControlState.AVOID_OBSTACLES
    self.supervisor.current_controller = self.supervisor.avoid_obstacles_controller

  def transition_to_state_go_to_goal( self ):
    self.current_state = ControlState.GO_TO_GOAL
    self.supervisor.current_controller = self.supervisor.go_to_goal_controller

  def transition_to_state_gtg_and_ao( self ):
    self.current_state = ControlState.GTG_AND_AO
    self.supervisor.current_controller = self.supervisor.gtg_and_ao_controller


  # === CONDITIONS ===
  def condition_at_goal( self ):
    return linalg.distance( self.supervisor.estimated_pose.vposition(), self.supervisor.goal ) < D_STOP

  def condition_at_obstacle( self ):
    for d in self._forward_sensor_distances():
      if d < D_CAUTION: return True
    return False

  def condition_danger( self ):
    for d in self._forward_sensor_distances():
      if d < D_DANGER: return True
    return False

  def condition_no_obstacle( self ):
    for d in self._forward_sensor_distances():
      if d < D_CAUTION: return False
    return True
    
 
  # === helper methods === 
  def _forward_sensor_distances( self ):
    return self.supervisor.proximity_sensor_distances[1:7]
