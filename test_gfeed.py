#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid.pydgrid import grid
from pydgrid.pf import pf_eval,time_serie
from pydgrid.electric import bess_vsc_feeder, bess_vsc_feeder_eval
from pydgrid.simu import simu, f_eval, ini_eval, run_eval
import matplotlib.pyplot as plt
import numpy as np
import time
#sys1 = grid()
#t_0 = time.time()
#sys1.read('./examples/luna/luna_1_4w.json')  # Load data
#sys1.pf()
#sys1.get_v()
#sys1.get_i()
#print('iters: ', sys1.params_pf['iters'])
#    
sys1 = grid()
sys1.read('./examples/luna/luna_gfeeder_dyn.json')  # Load data
sys1.pf()

simu1 = simu('./examples/luna/luna_gfeeder_dyn.json',sys1)

simu1.params_simu.Dt = 0.1
t = 0.0
ini_eval(t,
         sys1.params_pf,
         simu1.params_simu,
         simu1.params_bess_vsc_feeder)

t_0 = time.time()
T,V_nodes, I_nodes = run_eval(60*60*24,
                           sys1.params_pf,
                           simu1.params_simu,
                           simu1.params_bess_vsc_feeder)

print('time: {:f}'.format(time.time()-t_0))

print(simu1.params_bess_vsc_feeder.soc/1000/3600)

print(np.abs(sys1.params_pf.V_node))

print(simu1.params_simu.N_steps)
print(simu1.params_bess_vsc_feeder.switch)


fig, ax = plt.subplots()

ax.plot(T,abs(V_nodes))
ax.set_ylim((200,300))
