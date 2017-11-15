#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid.pydgrid import grid
from pydgrid.pf import pf_eval,time_serie
from pydgrid.electric import bess_vsc, bess_vsc_eval
from pydgrid.simu import simu, f_eval, ini_eval, run_eval
import matplotlib.pyplot as plt
import numpy as np
import time

def test_dyn_bess():
    data = {
    "lines":[
            {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "UG1", "m": 10.0},
            {"bus_j": "Bus_2",  "bus_k": "Bus_3",  "code": "UG1", "m": 100.0},
            {"bus_j": "Bus_3",  "bus_k": "Bus_4",  "code": "UG1", "m": 100.0},
            ],
    "buses":[
            {"bus": "Bus_1",  "pos_x":   0.0, "pos_y": 0, "units": "m", "U_kV":0.4},
            {"bus": "Bus_2",  "pos_x":  10.0, "pos_y": 0, "units": "m", "U_kV":0.4},
            {"bus": "Bus_3",  "pos_x": 110.0, "pos_y": 0, "units": "m", "U_kV":0.4},
            {"bus": "Bus_4",  "pos_x": 210.0, "pos_y": 0, "units": "m", "U_kV":0.4}
            ],
    "grid_formers":[
            {"bus": "Bus_1",
            "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
            "kV": [0.23094, 0.23094, 0.23094]},
            {"bus": "Bus_4",
            "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
            "kV": [0.23094, 0.23094, 0.23094]}
            ],
    "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],
                    "kW": [-10,-10,-10], "kvar": [0,0,0],
                    "kA": [0,0,0], "phi_deg":[30, 30, 30]},
                    {"bus": "Bus_3","bus_nodes": [1, 2, 3],
                    "kW": [-5, -5, -5], "kvar": [0,0,0],
                    "kA": [0,0,0], "phi_deg":[30, 30, 30]}
                    ],
    "line_codes":
        {"pry_al_50":  {"R1":0.8,    "X1":	0.148, "R0":0.8,   "X0":	0.148},
         "pry_al_95":  {"R1":0.403,  "X1":	0.129, "R0":0.403, "X0":	0.129},
         "pry_al_120": {"R1":0.321,  "X1":	0.123, "R0":0.321, "X0":	0.321},
         "pry_al_185": {"R1":0.209,  "X1":	0.113, "R0":0.209, "X0":	0.209},
         "pry_al_300": {"R1":0.128,  "X1":	0.105, "R0":0.128, "X0":	0.128}
         },
    "shunts":[
            {"bus": "Bus_1" , "R": 0.1, "X": 0.0, "bus_nodes": [4,0]},
            {"bus": "Bus_4" , "R": 0.1, "X": 0.0, "bus_nodes": [4,0]}
            ],
    "bess_vsc":[{"id":"gformer.Bus_1","source_mode":"grid_former","ctrl_mode":3,"s_n_kVA":50.0,"V_dc":800.0,
                "soc_max_kWh":1.0,"soc_ini_kWh":0.5},
                {"id":"gfeeder.Bus_2","source_mode":"grid_feeder","ctrl_mode":3,"s_n_kVA":50.0,"V_dc":800.0,
                "soc_max_kWh":1.0,"soc_ini_kWh":0.5},
                {"id":"gfeeder.Bus_3","source_mode":"grid_feeder","ctrl_mode":3,"s_n_kVA":50.0,"V_dc":800.0,
                "soc_max_kWh":1.0,"soc_ini_kWh":0.5},            
                {"id":"gformer.Bus_4","source_mode":"grid_former","ctrl_mode":3,"s_n_kVA":50.0,"V_dc":800.0,
                "soc_max_kWh":1.0,"soc_ini_kWh":0.5}]
    }
            
    sys1 = grid()
    sys1.read(data)  # Load data
    #gfeed_powers = np.copy(sys1.params_pf['gfeed_powers'])
    #sys1.params_pf['gfeed_powers'] = 0.0*gfeed_powers
    sys1.pf_solver = 1
    #sys1.pf()  # solve power flow
    #print(sys1.params_pf['iters'] )
    
    #sys1.params_pf['gfeed_powers'] = gfeed_powers
    
    sys1.pf()  # solve power flow
    sys1.get_v()      # post process voltages
    sys1.get_i()      # post process currents
    
    
    simu1 = simu(data,sys1)
    simu1.Dt = 0.1
    ini_eval(0.0,sys1.params_pf,simu1.params_simu,simu1.params_bess_vsc)
    
    T,V_nodes,I_nodes,X = run_eval(100,sys1.params_pf,simu1.params_simu,simu1.params_bess_vsc)
    assert abs(T[-1,0]-99.9)<0.01

if __name__ == "__main__":
    pass

#    test_Dyn11()
#    test_Dyg11_3w()
