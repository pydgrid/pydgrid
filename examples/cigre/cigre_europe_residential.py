#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:15:54 2017

@author: jmmauricio
"""


import numpy as np
from pydgrid.pydgrid import grid
grid_1 = grid()
grid_1.read('cigre_europe_residential.json')  # Load data
grid_1.pf()
print(grid_1.buses)