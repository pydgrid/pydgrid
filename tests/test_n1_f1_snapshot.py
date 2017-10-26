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

sys1 = grid()
sys1.read('./examples/n1_f1/n1_f1.json')  # Load data
sys1.read_loads_shapes('./examples/n1_f1/n1_f1_load_shapes.json')  
sys1.pf_solver = 2
sys1.snapshot(12*3600)
sys1.pf()  # solve power flow
print(sys1.params_pf[0]['pq_1p'])
sys1.get_v()      # post process voltages
sys1.get_i()      # post process currents

