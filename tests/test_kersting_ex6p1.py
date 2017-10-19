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
#/home/jmmauricio/Documents/workspace/pydgrid
sys1 = grid()
sys1.read('../examples/kersting_ex6p1.json')  # Load data
sys1.pf_solver = 2
sys1.pf()  # solve power flow

sys1.get_v()      # post process voltages
sys1.get_i()      # post process currents

print(sys1.buses)
print(sys1.lines)

print(sys1.Y.toarray().real)
print(sys1.Y.toarray().imag)

Phases = ['an','bn','cn']
for bus in sys1.buses:
    for ph in Phases:
        print('V_{:s}_n = {:2.2f}|{:2.2f}º V'.format(ph,bus['v_'+ph],bus['deg_'+ph]))

Phases = ['a','b','c']
for line in sys1.lines:
    for ph in Phases:
        print('I_{:s}_n = {:2.2f}|{:2.2f}º A'.format(ph,line['i_'+ph+'_m'],line['deg_'+ph]))
        
#for ph,v in zip(Phases,V_unknown[:,0]):
#    print('V_{:s}_m = {:2.2f}|{:2.2f}º V'.format(ph,abs(v),np.angle(v,deg=True)))
#
print(sys1.Y.toarray().imag)