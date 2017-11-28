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


data = {
"transformers":[
        {"bus_j": "Bus_0",  "bus_k": "Bus_1",  "S_n_kVA": 1500.0, "U_1_kV":66.0, "U_2_kV":20.0,
        "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Ygd11_3w",
        "conductors_1": 3, "conductors_2": 3}
        ],
"lines":[
        {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "pry_al_120", "m": 200.0}
        ],
"buses":[
        {"bus": "Bus_0",  "pos_x": 0,  "pos_y": 0, "units": "m", "U_kV":66.0},
        {"bus": "Bus_1",  "pos_x":10,  "pos_y": 0, "units": "m", "U_kV":20.0},
        {"bus": "Bus_2",  "pos_x":200, "pos_y": 0, "units": "m", "U_kV":20.0}
        ],
"grid_formers":[
        {"bus": "Bus_0",
        "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
        "kV": [38.105, 38.105, 38.105]}
        ],
"grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],
                "kW": [0, 0, 0], "kvar": [0,0,0],
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
        {"bus": "Bus_2" , "R": 1e12, "X": 0.0, "bus_nodes": [1,0]}
        ],
"groundings":[
        {"bus": "Bus_1" , "Z_gnd": 32, "conductors": 3}
        ]
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
print(sys1.params_pf['iters'] )


if __name__ == "__main__":
    pass

#    test_Dyn11()
#    test_Dyg11_3w()
