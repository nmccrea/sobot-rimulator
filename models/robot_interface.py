#!/usr/bin/python
# -*- Encoding: utf-8 -*

# a class representing the available interactions a supervisor may have with a robot
class RobotInterface:

  def __init__( self, robot ):
    self.robot = robot
  
  # read the proximity sensors
  def read_proximity_sensors( self ):
    return [ s.read() for s in self.robot.proximity_sensors ]

  # read the wheel encoders
  def read_wheel_encoders( self ):
    return [ e.read() for e in self.robot.wheel_encoders ]
