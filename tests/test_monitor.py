#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid import grid
from pydgrid.pf import pf_eval,time_serie
from pydgrid.electric import bess_vsc, bess_vsc_eval
from pydgrid.simu import simu, f_eval, ini_eval, run_eval
import matplotlib.pyplot as plt
import numpy as np
import time

def test_monitor1():
    
    data = {
    "transformers":[
            {"bus_j": "Bus_MV",  "bus_k": "Bus_LV",  "S_n_kVA": 150.0, "U_1_kV":20.0, "U_2_kV":0.4,
            "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyn11", 
            "conductors_1": 3, "conductors_2": 4}
            ],
    "lines":[
            {"bus_j": "Bus_LV",  "bus_k": "Client_1",  "code": "UG1", "m": 100.0},
            {"bus_j": "Client_1",  "bus_k": "Bus_LV",  "code": "UG2", "m": 100.0},
            {"bus_j": "Client_1",  "bus_k": "C1_c1",  "code": "UG1", "m": 20.0},
            {"bus_j": "Client_1",  "bus_k": "C1_c2",  "code": "UG1", "m": 30.0},
            {"bus_j": "Client_2",  "bus_k": "Bus_LV",  "code": "UG1", "m": 200.0},
            {"bus_j": "Client_2",  "bus_k": "C2_c1",  "code": "UG1", "m": 10.0}
            ],
    "buses":[
            {"bus": "Bus_MV",  "pos_x": 0,  "pos_y": 0, "units": "m", "U_kV":20.0},
            {"bus": "Bus_LV",  "pos_x":10,  "pos_y": 0, "units": "m", "U_kV":0.4},
            {"bus": "Client_1",  "pos_x":100, "pos_y": 20, "units": "m", "U_kV":0.4},
            {"bus": "C1_c1",  "pos_x":120, "pos_y": 30, "units": "m", "U_kV":0.4},
            {"bus": "C1_c2",  "pos_x":130, "pos_y": 10, "units": "m", "U_kV":0.4},
            {"bus": "Client_2",  "pos_x":200, "pos_y": -30, "units": "m", "U_kV":0.4},
            {"bus": "C2_c1",  "pos_x":210, "pos_y": -30, "units": "m", "U_kV":0.4}
            ],
    "grid_formers":[
            {"bus": "Bus_MV",
            "bus_nodes": [1, 2, 3], "deg": [0, -120, -240], 
            "kV": [11.547, 11.547, 11.547]}
            ],
    "grid_feeders":[{"bus": "C1_c1","bus_nodes": [1, 2, 3, 4],
                    "kW": [0, 0, 0], "kvar": [0,0,0],
                    "kA": [0,0,0], "phi_deg":[0, 0, 0]}
                    ],
    "loads":[
             {"bus": "C1_c2" , "kVA":   20.0, "pf": 0.8,"type":"3P"},
            # {"bus": "C1_c2" , "kVA":   20.0, "pf": 0.8,"type":"1P+N","bus_nodes": [1,4]},    
             {"bus": "C2_c1" , "kVA":   30.0, "pf": 0.8,"type":"3P"},
            ],
    "shunts":[
            {"bus": "Bus_LV" , "R": 0.0001, "X": 0.0, "bus_nodes": [4,0]},
            {"bus": "Bus_LV" , "R": 0.0001, "X": 0.0, "bus_nodes": [4,0]}
            ]
    }   
    
    sys1 = grid()
    sys1.read(data)  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow

    sys1.get_v()      # post process voltages
    sys1.get_i()      # post process currents
    mon1 = sys1.monitor('Client_1','Bus_LV')
    mon2 = sys1.monitor('Client_2','Bus_LV')

    
    results = {'P1': (-0.8*20*1000, mon1.P),#'Q1': (-0.6*20*100, mon1.Q),
               #'P2': (-0.8*30*1000, mon2.P),'Q2': (-0.6*30*100, mon2.Q)
               }
    for item in results:
        expected, obtained = results[item]
        error = expected - obtained

        assert abs(error)<100.0
 