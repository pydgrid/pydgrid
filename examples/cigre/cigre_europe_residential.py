#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 09:15:54 2017

@author: jmmauricio
"""


import numpy as np
from pydgrid.pydgrid import grid
import time

grid_1 = grid()
grid_1.read('cigre_europe_residential.json')  # Load data

time_0 = time.time()
grid_1.pf()
time_1 = time.time()
print(grid_1.buses)

print(f'Solution found in {time_1-time_0:0.4f} s')