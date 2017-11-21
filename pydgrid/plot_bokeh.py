#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 16:06:38 2017

@author: jmmauricio
"""

from bokeh.io import output_notebook, show
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.io import push_notebook
from bokeh.resources import INLINE
output_notebook(INLINE)


def plot_results(grid):
    grid.bokeh_tools()
    
    p = figure(width=600, height=400,
               title='Results')
    
    # trafos:
    source = ColumnDataSource(grid.transformer_data)
    trafo = p.multi_line(source=source, xs='x_s', ys='y_s', color="green", alpha=0.5, line_width=5)
    
    # lines:
    source = ColumnDataSource(grid.line_data)
    lin = p.multi_line(source=source, xs='x_s', ys='y_s', color="red", alpha=0.5, line_width=5)
    
    # buses:
    source = ColumnDataSource(grid.bus_data)
    cr = p.circle(source=source, x='x', y='y', size=15, color="navy", alpha=0.5)
    
    p.add_tools(HoverTool(renderers=[trafo], tooltips=grid.transformer_tooltip))
    p.add_tools(HoverTool(renderers=[lin], tooltips=grid.line_tooltip))
    p.add_tools(HoverTool(renderers=[cr], tooltips=grid.bus_tooltip))
    show(p)
    
    return p