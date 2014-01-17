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





import pygtk

from math import *

class Frame:
  
  def __init__( self ):
    self.draw_list = []
    
    
  def add_circle( self,
                  pos, radius,
                  color, alpha=None ):
    self.draw_list.append({
      'type':   'circle',
      'pos':    pos,
      'radius': radius,
      'color':  color,
      'alpha':  alpha
    })
    
    
  def add_polygons( self,
                    polygons,
                    color, alpha=None ):
    self.draw_list.append({
      'type':     'polygons',
      'polygons': polygons,
      'color':    color,
      'alpha':    alpha
    })
    
    
  def add_lines( self,
                 lines, linewidth,
                 color, alpha=None ):
    self.draw_list.append({
      'type':       'lines',
      'lines':      lines,
      'linewidth':  linewidth,
      'color':      color,
      'alpha':      alpha
    })