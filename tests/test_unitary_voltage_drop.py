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


def test_manufacturer_1():
    '''
    Open circuit like test
    '''
    
    phi = -np.arccos(0.8)*180./np.pi
    I = -0.428
    data = {
        "lines":[
                {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "lv_cu_240", "m": 150.0}
                ],
        "buses":[
        		{"bus": "Bus_1",  "pos_x": 10, "pos_y":  0, "units": "m", "U_kV":0.4},
        		{"bus": "Bus_2",  "pos_x": 200, "pos_y": 0, "units": "m", "U_kV":0.4}
        		],
        "grid_formers":[
        		{"bus": "Bus_1","bus_nodes": [1, 2, 3],
        			"kV": [0.4/3**0.5, 0.4/3**0.5, 0.4/3**0.5],
        			"deg": [0, 120, 240.0]
        		}
        		],
        "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],"kW": [0,0,0],
                         "kvar": [0,0,0],"kA": [I,I,I], "phi_deg":[phi, phi, phi]}],
        "line_codes":
        		{"lv_cu_240":  {"u90_pf10":0.17,"u90_pf08":0.22, 'T_deg':90.0, 'alpha':0.004}
        		},
                "shunts":[
                 {"bus": "Bus_1" , "R": 0.01, "X": 0.0, "bus_nodes": [4,0]}
                 ],
        		        }

    # pydgrid calculation
    sys1 = grid()
    sys1.read(data)  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow
    sys1.get_v()      # post process voltages

    DU = 400.0 - sys1.buses[1]['v_ab'] 
    DU_manufacturer = 14.124

    error = DU_manufacturer - DU
    

    assert abs(error)<0.001
    
 



if __name__ == "__main__":
#    test_Dyg11_3w()
    test_manufacturer_1()
    pass

#    test_Dyn11()
#    test_Dyg11_3w()
