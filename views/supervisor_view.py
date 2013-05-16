#!/usr/bin/python
# -*- Encoding: utf-8 -*

class SupervisorView:

  def __init__( self, viewer, supervisor, robot_geometry ):
    self.viewer = viewer
    self.supervisor = supervisor

    # information for rendering
    self.robot_geometry = robot_geometry

  # draw a representation of the supervisor's internal state to the frame
  def draw_supervisor_to_frame( self, frame ):
    self._draw_goal_to_frame( frame )
    self._draw_robot_state_estimate_to_frame( frame )

  def _draw_goal_to_frame( self, frame ):
    goal = self.supervisor.goal
    frame.add_circle( pos = goal,
                      radius = 0.05,
                      color = "dark green",
                      alpha = 0.25 )
    frame.add_circle( pos = goal,
                      radius = 0.01,
                      color = "black",
                      alpha = 0.5 )

  def _draw_robot_state_estimate_to_frame( self, frame ):
    estimated_pose = self.supervisor.estimated_pose

    vertexes = self.robot_geometry.get_transformation_to_pose( estimated_pose ).vertexes[:]
    vertexes.append( vertexes[0] )    # close the drawn polygon
    frame.add_lines(  [ vertexes ],
                      color = "black",
                      linewidth = 0.0075,
                      alpha = 0.5 )
