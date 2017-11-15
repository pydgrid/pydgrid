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


#def test_medina_sidonia_1():
'''  '''

p = 2000/3
q= 0e3
data = {
    "lines":[
        {"bus_j": "POI_MT",  "bus_k": "W1mv",  "code": "pry_al_50", "m":460},
        {"bus_j": "POI_MT",  "bus_k": "W2mv",  "code": "pry_al_50", "m":710},
        {"bus_j": "POI_MT",  "bus_k": "W3mv",  "code": "pry_al_300", "m":1030},
        {"bus_j": "W3mv",  "bus_k": "W4mv",  "code": "pry_al_185", "m":325},
        {"bus_j": "W4mv",  "bus_k": "W5mv",  "code": "pry_al_120", "m":870},
        {"bus_j": "W5mv",  "bus_k": "W6mv",  "code": "pry_al_95", "m":680},
        {"bus_j": "W6mv",  "bus_k": "W7mv",  "code": "pry_al_50", "m":1200},
        {"bus_j": "W7mv",  "bus_k": "W8mv",  "code": "pry_al_50", "m":380}
            ],
    "buses":[
            {"bus": "POI_MT",  "pos_x": 0.0, "pos_y":  0.0, "units": "m", "U_kV":20.0},
            {"bus": "W1",  "pos_x": 332.6, "pos_y":  -200.7, "units": "m", "U_kV":0.69},
            {"bus": "W2",  "pos_x": 475.1, "pos_y":  213.3, "units": "m", "U_kV":0.69},
            {"bus": "W3",  "pos_x": -515.2, "pos_y":  288.3, "units": "m", "U_kV":0.69},
            {"bus": "W4",  "pos_x": -505.1, "pos_y":  544.2, "units": "m", "U_kV":0.69},
            {"bus": "W5",  "pos_x": -495.9, "pos_y":  898.1, "units": "m", "U_kV":0.69},
            {"bus": "W6",  "pos_x": -476.3, "pos_y":  1179.5, "units": "m", "U_kV":0.69},
            {"bus": "W7",  "pos_x": -1297.8, "pos_y":  1205.9, "units": "m", "U_kV":0.69},
            {"bus": "W8",  "pos_x": -1367.2, "pos_y":  873.1, "units": "m", "U_kV":0.69},
            {"bus": "W1mv",  "pos_x": 352.6, "pos_y":  -200.7, "units": "m", "U_kV":20.0},
            {"bus": "W2mv",  "pos_x": 495.1, "pos_y":  213.3, "units": "m", "U_kV":20.0},
            {"bus": "W3mv",  "pos_x": -495.2, "pos_y":  288.3, "units": "m", "U_kV":20.0},
            {"bus": "W4mv",  "pos_x": -485.1, "pos_y":  544.2, "units": "m", "U_kV":20.0},
            {"bus": "W5mv",  "pos_x": -475.9, "pos_y":  898.1, "units": "m", "U_kV":20.0},
            {"bus": "W6mv",  "pos_x": -456.3, "pos_y":  1179.5, "units": "m", "U_kV":20.0},
            {"bus": "W7mv",  "pos_x": -1277.8, "pos_y":  1205.9, "units": "m", "U_kV":20.0},
            {"bus": "W8mv",  "pos_x": -1347.2, "pos_y":  873.1, "units": "m", "U_kV":20.0}
    		],
    "transformers":[
                    {"bus_j": "W1mv",  "bus_k": "W1",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                    {"bus_j": "W2mv",  "bus_k": "W2",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                    {"bus_j": "W3mv",  "bus_k": "W3",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                    {"bus_j": "W4mv",  "bus_k": "W4",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                    {"bus_j": "W5mv",  "bus_k": "W5",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                    {"bus_j": "W6mv",  "bus_k": "W6",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                    {"bus_j": "W7mv",  "bus_k": "W7",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                    {"bus_j": "W8mv",  "bus_k": "W8",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                    "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3}
                    ],
    "grid_formers":[
    		{"bus": "POI_MT","bus_nodes": [1, 2, 3],
    			"kV": [11.547, 11.547, 11.547], "deg": [30, 150, 270.0]
    		}
    		],
    "grid_feeders":[{"bus": "W1","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]},
                    {"bus": "W2","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]},
                    {"bus": "W3","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]},
                    {"bus": "W4","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]},
                    {"bus": "W5","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]},
                    {"bus": "W6","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]},
                    {"bus": "W7","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]},
                    {"bus": "W8","bus_nodes": [1, 2, 3],"kW": p, "kvar": q, "kA": [0,0,0], "phi_deg":[0, 0, 0]}
    ],
    "line_codes":
        {"pry_al_50":  {"R1":0.8,    "X1":	0.148, "R0":0.8,   "X0":	0.148},
         "pry_al_300": {"R1":0.128,  "X1":	0.105, "R0":0.128, "X0":	0.128},
         "pry_al_185": {"R1":0.209,  "X1":	0.113, "R0":0.209, "X0":	0.209},
         "pry_al_120": {"R1":0.321,  "X1":	0.123, "R0":0.321, "X0":	0.321},
         "pry_al_95":  {"R1":0.403,  "X1":	0.129, "R0":0.403, "X0":	0.129}
    	  }
    }

# pydgrid calculation
sys1 = grid()
sys1.read(data)  # Load data
sys1.pf_solver = 2
sys1.pf()  # solve power flow    
#sys1.pf()  # solve power flow    
sys1.get_v()      # post process voltages
sys1.get_i()      # post process currents


##    I_12_pydgrid = sys1.lines[0]['i_a_m']    
##
##    # positive sequence "manual" calculation
#V_1_m = sys1.buses[0]['v_an']
#V_2_m = sys1.buses[1]['v_an']
#
#DV = V_1_m - V_2_m
#DU_pydgrid = np.sqrt(3)*DV
#DU_catalog = 24.41
#
## comparison
#error = DU_pydgrid - DU_catalog
#    
    #assert abs(error)<0.001
phases = ['an','bn','cn']

for bus in sys1.buses:
    for phase in phases:
        print(bus['bus'],bus['v_{:s}'.format(phase)],bus['deg_{:s}'.format(phase)])
print(sys1.params_pf['iters'])
#if __name__ == "__main__":
#    
##    test_line_sequence_z()
#    test_pr_mt_h()
