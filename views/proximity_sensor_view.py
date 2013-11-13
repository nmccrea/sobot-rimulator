#!/usr/bin/python
# -*- Encoding: utf-8 -*

from math import *
import utils.linalg2_util as linalg

class ProximitySensorView:

  def __init__( self, viewer, proximity_sensor ):
    self.viewer = viewer
    self.proximity_sensor = proximity_sensor

  def draw_proximity_sensor_to_frame( self, frame ):
    proximity_sensor = self.proximity_sensor

    # grab proximity sensor pose values
    sensor_pos, sensor_theta = proximity_sensor.pose.vunpack()

    # build the sensor cone
    r = proximity_sensor.max_range
    phi = proximity_sensor.phi_view
    sensor_cone_poly = [ [0.0, 0.0],
                         [r*cos(-phi/2), r*sin(-phi/2)],
                         [r, 0.0],
                         [r*cos(phi/2), r*sin(phi/2)] ]
    sensor_cone_poly = linalg.rotate_and_translate_vectors( sensor_cone_poly,
                                                            sensor_theta,
                                                            sensor_pos )

    # shade the sensor cone according to positive detection
    if self.proximity_sensor.target_delta != None:
      alpha = 0.9 - 0.8*self.proximity_sensor.target_delta
    else:
      alpha = 0.1

    # add the sensor cone to the frame
    frame.add_polygons( [ sensor_cone_poly ],
                        color = "red",
                        alpha = alpha )

    # === FOR DEBUGGING: ===
    # self._draw_detector_line_to_frame( frame )
    # self._draw_detector_line_origins_to_frame( frame )
    # self._draw_bounding_circle_to_frame( frame )
    # self._draw_detection( frame )

  def _draw_detection( self, frame ):
    target_delta = self.proximity_sensor.target_delta
    if target_delta != None:
      detector_endpoints = self.proximity_sensor.detector_line.vertexes
      detector_vector = linalg.sub( detector_endpoints[1], detector_endpoints[0] )
      target_vector = linalg.add( detector_endpoints[0], linalg.scale( detector_vector, target_delta ) )
      
      frame.add_circle( pos = target_vector,
                        radius = 0.02,
                        color = "black",
                        alpha = 0.7 )
  
  def _draw_detector_line_to_frame( self, frame ):
    vertexes = self.proximity_sensor.detector_line.vertexes

    frame.add_lines(  [ vertexes ],
                      linewidth = 0.005,
                      color = "black",
                      alpha = 0.7 )

  def _draw_detector_line_origins_to_frame( self, frame ):
    origin = self.proximity_sensor.detector_line.vertexes[0]
    frame.add_circle( pos = (origin[0], origin[1]),
                      radius = 0.02,
                      color = "black" )

  def _draw_bounding_circle_to_frame( self, frame ):
    c, r = self.proximity_sensor.detector_line.bounding_circle
    frame.add_circle( pos = c,
                      radius = r,
                      color = "black",
                      alpha = 0.2 )
    frame.add_circle( pos = c,
                      radius = 0.005,
                      color = "black",
                      alpha = 0.3 )
