#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *

from utils import linalg2_util as linalg
from utils import math_util

class GoToGoalController:

  def __init__( self ):
    # gains
    self.kP = 5.0
    self.kI = 0.01
    self.kD = 0.1

    self.prev_eP = 0.0
    self.prev_eI = 0.0

  def execute( self, estimated_pose, goal ):
    vect_to_goal = linalg.sub( goal, estimated_pose.vunpack()[0] )
    theta_d = atan2( vect_to_goal[1], vect_to_goal[0] )
    theta = estimated_pose.theta
    
    eP = math_util.normalize_angle( theta_d - theta )
    eI = self.prev_eI + eP*0.05
    eD = ( eP - self.prev_eP ) / 0.05

    self.prev_eP = eP
    self.prev_eI = eI

    omega = self.kP * eP + self.kI * eI + self.kD * eD
    
    # velocity is v_max when omega is 0,
    # drops rapidly to zero as |omega| rises
    v_max = 2.0
    v = v_max / ( log( abs( omega ) + 1 ) + ( 10 * abs( omega ) ) + 1 )

    print "\n\n"
    print "=============="
    print "ERRORS:"
    print "eP: " + str( eP )
    print "eI: " + str( eI )
    print "eD: " + str( eD )
    print ""
    print "CONTROL COMPONENTS:"
    print "kP * eP = " + str( self.kP ) + " * " + str( eP )
    print "= " + str( self.kP * eP )
    print "kI * eI = " + str( self.kI ) + " * " + str( eI )
    print "= " + str( self.kI * eI )
    print "kD * eD = " + str( self.kD ) + " * " + str( eD )
    print "= " + str( self.kD * eD )
    print ""
    print "OUTPUTS:"
    print "omega: " + str( omega )
    print "v    : " + str( v )

    return v, omega
