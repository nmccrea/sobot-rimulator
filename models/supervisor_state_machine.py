#!/usr/bin/python
# -*- Encoding: utf-8 -*

class SupervisorStateMachine:

  def __init__( self, supervisor ):
    self.supervisor = supervisor

  def update_state( self ):
    print "UPDATING STATE MACHINE"
