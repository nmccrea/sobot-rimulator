#!/usr/bin/python
# -*- Encoding: utf-8 -*

from utils import math_util

class GoToAngleController:

  def __init__( self ):
    # gains
    self.k_p = 1.2

  def execute( self, estimated_pose, theta_d ):
    theta = estimated_pose.theta
    e = math_util.normalize_angle( theta_d - theta )
    omega = self.k_p * e

    return omega
