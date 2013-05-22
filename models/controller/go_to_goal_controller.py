#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

from utils import linalg2_util as linalg
from utils import math_util

class GoToGoalController:

  def __init__( self, supervisor ):
    # bind the supervisor
    self.supervisor = supervisor

    # gains
    self.kP = 5.0
    self.kI = 0.01
    self.kD = 0.1
    
    # stored values - for computing next results
    self.prev_time = 0.0
    self.prev_eP = 0.0
    self.prev_eI = 0.0

  def execute( self ):
    position, theta = self.supervisor.estimated_pose().vunpack()

    # calculate the time that has passed since the last iteration
    current_time = self.supervisor.time()
    dt = current_time - self.prev_time

    # calculate the desired heading
    vect_to_goal = linalg.sub( self.supervisor.goal(), position )
    theta_d = atan2( vect_to_goal[1], vect_to_goal[0] )

    # calculate the error terms
    eP = math_util.normalize_angle( theta_d - theta )
    eI = self.prev_eI + eP*dt
    eD = ( eP - self.prev_eP ) / dt

    # calculate angular velocity
    omega = self.kP * eP + self.kI * eI + self.kD * eD
    
    # calculate translational velocity
    # velocity is v_max when omega is 0,
    # drops rapidly to zero as |omega| rises
    v_max = 2.0 # TODO: move this
    v = v_max / ( log( abs( omega ) + 1 ) + ( 10 * abs( omega ) ) + 1 )

    # store values for next control iteration
    self.prev_time = current_time
    self.prev_eP = eP
    self.prev_eI = eI

    self.supervisor.set_outputs( v, omega )

    # print "\n\n"
    # print "=============="
    # print "ERRORS:"
    # print "eP: " + str( eP )
    # print "eI: " + str( eI )
    # print "eD: " + str( eD )
    # print ""
    # print "CONTROL COMPONENTS:"
    # print "kP * eP = " + str( self.kP ) + " * " + str( eP )
    # print "= " + str( self.kP * eP )
    # print "kI * eI = " + str( self.kI ) + " * " + str( eI )
    # print "= " + str( self.kI * eI )
    # print "kD * eD = " + str( self.kD ) + " * " + str( eD )
    # print "= " + str( self.kD * eD )
    # print ""
    # print "OUTPUTS:"
    # print "omega: " + str( omega )
    # print "v    : " + str( v )
