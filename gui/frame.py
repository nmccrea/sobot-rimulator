#!/usr/bin/env python

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