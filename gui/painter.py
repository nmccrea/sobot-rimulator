#!/usr/bin/env python

from color_palette import *
from math import *

class Painter:
  
  def __init__( self, drawing_area ):
    self.drawing_area = drawing_area
    
    
  def draw_frame( self, frame ):
    context = self.drawing_area.window.cairo_create()
    
    draw_list = frame.draw_list
    for component in draw_list:
      if component['type'] == 'circle':
        self.draw_circle( context,
                          component['pos'],
                          component['radius'],
                          component['color'],
                          component['alpha'] )
      elif component['type'] == 'polygons':
        self.draw_polygons( context,
                            component['polygons'],
                            component['color'],
                            component['alpha'] )
      elif component['type'] == 'lines':
        self.draw_lines( context,
                         component['lines'],
                         component['linewidth'],
                         component['color'],
                         component['alpha'] )
                            
                            
  def draw_circle( self, context,
                   pos, radius,
                   color, alpha ):
    self.set_color( context, color, alpha )
    context.arc( pos[0], pos[1], radius, 0, 2.0 * pi )
    context.fill()
    
    
  def draw_polygons( self, context,
                     polygons,
                     color, alpha ):
    self.set_color( context, color, alpha )
    for polygon in polygons:
      context.new_path()
      context.move_to( *polygon[0] )
      for point in polygon[1:]:
        context.line_to( *point )
      context.fill()
      
      
  def draw_lines( self, context,
                  lines, linewidth,
                  color, alpha ):
    self.set_color( context, color, alpha )
    context.set_line_width( linewidth )
    for line in lines:
      context.new_path()
      context.move_to( *line[0] )
      for point in line[1:]:
        context.line_to( *point )
      context.stroke()
      
      
  def set_color( self, cairo_context, color_string, alpha ):
    ColorPalette.dab( cairo_context, color_string, alpha )