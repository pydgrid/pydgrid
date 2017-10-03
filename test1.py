#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid.pydgrid import grid
from pydgrid.pf import time_serie
import matplotlib.pyplot as plt
import numpy as np

#sys1 = grid()
#t_0 = time.time()
#sys1.read('./examples/luna/luna_1_4w.json')  # Load data
#sys1.pf()
#sys1.get_v()
#sys1.get_i()
#print('iters: ', sys1.params_pf['iters'])
#    
sys1 = grid()
sys1.read('./examples/cigre/cigre_europe_residential.json')  # Load data
sys1.read_loads_shapes('./examples/cigre/cigre_europe_residential_load_shapes.json')
sys1.pf()
t_ini = 0.0
t_end = 24*60*60
Dt = 1*60
V_nodes,I_nodes = time_serie(t_ini,t_end,Dt,sys1.params_pf,sys1.params_lshapes)

sys1.get_v()
sys1.get_i()
print('iters: ', sys1.params_pf['iters'])
    
fig, ax = plt.subplots()
ax.plot(np.abs(V_nodes),'.')
ax.set_ylim([200,235])

