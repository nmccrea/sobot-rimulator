# Sobot Rimulator - A Robot Programming Tool
# Copyright (C) 2013-2014 Nicholas S. D. McCrea
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
# Email mccrea.engineering@gmail.com for questions, comments, or to report bugs.





from color_palette import *
from math import *

class Painter:
  
  def __init__( self, drawing_area, pixels_per_meter ):
    self.drawing_area = drawing_area
    self.pixels_per_meter = pixels_per_meter
    
    
  def draw_frame( self, frame ):
    context = self.drawing_area.window.cairo_create()
    
    width_pixels = self.drawing_area.allocation.width
    height_pixels = self.drawing_area.allocation.height
    
    # transform the the view to metric coordinates
    context.translate( width_pixels/2.0, height_pixels/2.0 )        # move origin to center of window
    context.scale( self.pixels_per_meter, -self.pixels_per_meter )  # pull view to edges of window ( also flips y-axis )
    
    # draw the background in white
    self.set_color( context, 'white', 1.0 )
    context.paint()
    
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