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


def test_no_gnd():
    '''
    Transformer without grounding.
    Fault from a phase to ground.
    Under this condition it is supposed that there are no fault currents and overvoltage is espected.
    
    '''
    data = {
        "transformers":[
                {"bus_j": "B0",  "bus_k": "B1",  "S_n_kVA": 1500.0, "U_j_kV":66.0, "U_k_kV":20.0,
                "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Ygd11_3w",
                "conductors_1": 3, "conductors_2": 3}
                ],
        "lines":[
                {"bus_j": "B1",  "bus_k": "B2",  "code": "pry_al_120", "m": 200.0}
                ],
        "buses":[
                {"bus": "B0",  "pos_x": 0,  "pos_y": 0, "units": "m", "U_kV":66.0},
                {"bus": "B1",  "pos_x":10,  "pos_y": 0, "units": "m", "U_kV":20.0},
                {"bus": "B2",  "pos_x":200, "pos_y": 0, "units": "m", "U_kV":20.0}
                ],
        "grid_formers":[
                {"bus": "B0",
                "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
                "kV": [38.105, 38.105, 38.105]}
                ],
        "grid_feeders":[{"bus": "B2","bus_nodes": [1, 2, 3],
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
                {"bus": "B1" , "R": 1e12, "X": 0.0, "bus_nodes": [1,0]},
                {"bus": "B1" , "R": 1e12, "X": 0.0, "bus_nodes": [2,0]},
                {"bus": "B1" , "R": 1e12, "X": 0.0, "bus_nodes": [3,0]},
                {"bus": "B2" , "R": 1e-12, "X": 0.0, "bus_nodes": [1,0]}   # applied fault
            ]
    }
            
    grid_1 = grid()
    grid_1.read(data)  # Load data
    grid_1.pf_solver = 1
    grid_1.pf()  # solve power flow
    grid_1.get_v()      # post process voltages
    grid_1.get_i()      # post process currents
    
    assert grid_1.buses[1]['v_an'] < 0.001
    assert grid_1.buses[1]['v_bn'] > 20e3*0.999
    assert grid_1.buses[1]['v_cn'] > 20e3*0.999  
    assert grid_1.lines[0]['i_a_m'] < 0.001

    
def test_zigzag_gnd():
    '''
    Transformer without grounding.
    Grounding with zig-zag.
    Fault from a phase to ground.
    Under this condition it is supposed that there are fault current limited by grounding impedance.
    Overvoltages should be less than in the previous ungrounded  case.
    
    '''
    Z_b = (20.0e3)**2/1500.0e3
    Z_cc = (0.01 + 1j*0.04)*Z_b
    
    
    data = {
    "transformers":[
            {"bus_j": "Bus_0",  "bus_k": "Bus_1",  "S_n_kVA": 15000.0, "U_1_kV":66.0, "U_2_kV":20.0,
            "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Ygd11_3w",
            "conductors_1": 3, "conductors_2": 3}
            ],
    "lines":[
            {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "pry_al_120", "m": 0.1}
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
            {"bus": "Bus_2" , "R": 1e-12, "X": 0.0, "bus_nodes": [1,0]},
        #{"bus": "Bus_2" , "R": 1e-12, "X": 0.0, "bus_nodes": [2,0]},
        #{"bus": "Bus_2" , "R": 1e-12, "X": 0.0, "bus_nodes": [3,0]},
            ],
    "groundings":[
            {"bus": "Bus_1" , "R_gnd":Z_cc.real, "X_gnd":Z_cc.imag, "conductors": 3}
            ]
    }
            
    grid_1 = grid()
    grid_1.read(data)  # Load data
    grid_1.pf_solver = 1
    grid_1.pf()  # solve power flow
    grid_1.get_v()      # post process voltages
    grid_1.get_i()      # post process currents
    

    I_cc = np.abs((20.0e3/np.sqrt(3))/(Z_cc))
    
    assert grid_1.buses[1]['v_an'] < 10.0
    assert grid_1.buses[1]['v_bn'] < 20e3*0.9
    assert grid_1.buses[1]['v_cn'] < 20e3*0.9  
    assert grid_1.lines[0]['i_a_m'] > I_cc*0.8


 

    
        
        
#data = {
#"transformers":[
#        {"bus_j": "Bus_0",  "bus_k": "Bus_1",  "S_n_kVA": 1500.0, "U_1_kV":66.0, "U_2_kV":20.0,
#        "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Ygd11_3w",
#        "conductors_1": 3, "conductors_2": 3}
#        ],
#"lines":[
#        {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "pry_al_120", "m": 200.0}
#        ],
#"buses":[
#        {"bus": "Bus_0",  "pos_x": 0,  "pos_y": 0, "units": "m", "U_kV":66.0},
#        {"bus": "Bus_1",  "pos_x":10,  "pos_y": 0, "units": "m", "U_kV":20.0},
#        {"bus": "Bus_2",  "pos_x":200, "pos_y": 0, "units": "m", "U_kV":20.0}
#        ],
#"grid_formers":[
#        {"bus": "Bus_0",
#        "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
#        "kV": [38.105, 38.105, 38.105]}
#        ],
#"grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],
#                "kW": [0, 0, 0], "kvar": [0,0,0],
#                "kA": [0,0,0], "phi_deg":[30, 30, 30]}
#                ],
#    "line_codes":
#        {"pry_al_50":  {"R1":0.8,    "X1":	0.148, "R0":0.8,   "X0":	0.148},
#         "pry_al_95":  {"R1":0.403,  "X1":	0.129, "R0":0.403, "X0":	0.129},
#         "pry_al_120": {"R1":0.321,  "X1":	0.123, "R0":0.321, "X0":	0.321},
#         "pry_al_185": {"R1":0.209,  "X1":	0.113, "R0":0.209, "X0":	0.209},
#         "pry_al_300": {"R1":0.128,  "X1":	0.105, "R0":0.128, "X0":	0.128}
#         },
#"shunts":[
#        {"bus": "Bus_2" , "R": 1e12, "X": 0.0, "bus_nodes": [1,0]}
#        ],
#"groundings":[
#        {"bus": "Bus_1" , "Z_gnd": 32, "conductors": 3}
#        ]
#}
#
#sys1 = grid()
#sys1.read(data)  # Load data
##gfeed_powers = np.copy(sys1.params_pf['gfeed_powers'])
##sys1.params_pf['gfeed_powers'] = 0.0*gfeed_powers
#sys1.pf_solver = 1
##sys1.pf()  # solve power flow
##print(sys1.params_pf['iters'] )
#
##sys1.params_pf['gfeed_powers'] = gfeed_powers
#
#sys1.pf()  # solve power flow
#sys1.get_v()      # post process voltages
#sys1.get_i()      # post process currents
#print(sys1.params_pf['iters'] )


if __name__ == "__main__":
    grid_1 = test_no_gnd()
    grid_1 = test_zigzag_gnd()#    test_Dyn11()
#    test_Dyg11_3w()
