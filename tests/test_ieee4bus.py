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


def test_ieee4bus_Dyn11():
    feet2m = 0.3048
    mile2m = 1609.34
    mile2km = mile2m/1000
    inch2m = 0.0253999368683


    # Results from IEEE 

    V2_ag = 12350*np.exp(1j*np.deg2rad(29.6 ))
    V2_bg = 12314*np.exp(1j*np.deg2rad(-90.4))
    V2_cg = 12333*np.exp(1j*np.deg2rad(149.8))

    V3_ag = 2290*np.exp(1j*np.deg2rad(-32.4 ))
    V3_bg = 2261*np.exp(1j*np.deg2rad(-153.8))
    V3_cg = 2214*np.exp(1j*np.deg2rad(85.2))

    V4_ag = 2157*np.exp(1j*np.deg2rad(-34.2))
    V4_bg = 1936*np.exp(1j*np.deg2rad(-157.0))
    V4_cg = 1849*np.exp(1j*np.deg2rad(73.4))

    I12_a = 285.7*np.exp(1j*np.deg2rad(-27.6))
    I12_b = 402.7*np.exp(1j*np.deg2rad(-149.6))
    I12_c = 349.1*np.exp(1j*np.deg2rad(74.4))

    I34_a = 695.5*np.exp(1j*np.deg2rad(-66.0))
    I34_b = 1033*np.exp(1j*np.deg2rad(177.1))
    I34_c = 1352*np.exp(1j*np.deg2rad(55.2 ))

    s_a = V4_ag*np.conj(I34_a)
    s_b = V4_bg*np.conj(I34_b)
    s_c = V4_cg*np.conj(I34_c)


    feet2m = 0.3048

    data = {
    "lines":[
            {"bus_j": "1",  "bus_k": "2",  "code": "4wires3", "m": 2000.0*feet2m},
            {"bus_j": "3",  "bus_k": "4",  "code": "4wires", "m": 2500.0*feet2m}
            ],
    "buses":[
            {"bus": "1",  "pos_x":             0, "pos_y": 0, "units": "m", "U_kV":12.47},
            {"bus": "2",  "pos_x": 2000.0*feet2m, "pos_y": 0, "units": "m", "U_kV":12.47},
            {"bus": "3",  "pos_x": 2400.0*feet2m, "pos_y": 0, "units": "m", "U_kV":4.16},
            {"bus": "4",  "pos_x": 4500.0*feet2m, "pos_y": 0, "units": "m", "U_kV":4.16},
            ],
    "grid_formers":[
            {"bus": "1","bus_nodes": [1, 2, 3],
            "kV": [7.2, 7.2, 7.2],
            "deg": [0, -120.0, 120.0]
            }
            ],
    "transformers":[
                    {"bus_j": "2",  "bus_k": "3",  "S_n_kVA": 6000.0, "U_j_kV":12.47, "U_k_kV":4.16,
                    "R_cc_pu": 0.01, "X_cc_pu":0.06, "connection": "Dyn11",   "conductors_j": 3, "conductors_k": 4},
                ],
    "loads":[
            {"bus": "4" , "kW":  [s_a.real/1000,s_b.real/1000,s_c.real/1000], 
                        "kvar":  [s_a.imag/1000,s_b.imag/1000,s_c.imag/1000],"type":"3P+N"}
            ],
            "shunts":[
                    {"bus": "3" , "R": 1.0e-8, "X": 0.0, "bus_nodes": [4,0]},
                    {"bus": "4" , "R": 1.0e-8, "X": 0.0, "bus_nodes": [4,0]}
                    ],
        "line_codes":
        {"4wires":{
                    'GMR':[0.0244*feet2m,0.0244*feet2m,0.0244*feet2m,0.00814*feet2m], # m
                    'diam_c':[1.05/100]*4,    # m
                    'R_cond':[0.306/mile2m, 0.306/mile2m,0.306/mile2m,0.592/mile2m],    # Ohm/m
                    'pos_x':[-4*feet2m, -1.5*feet2m, 3.0*feet2m, 0.0*feet2m],
                    'pos_y':[28*feet2m, 28*feet2m, 28*feet2m, 24*feet2m],
                    'freq':60.0
        },
            "3wires":{
            "R":[[0.45753751, 0.15593636, 0.15347119],
                [0.15593636, 0.4666138 , 0.15799251],
                [0.15347119, 0.15799251, 0.46145871]],
            "X":[[1.07802078, 0.50165398, 0.38491254],
        [0.50165398, 1.04815115, 0.42362819],
        [0.38491254, 0.42362819, 1.06504486]
                ],
            "unit":"miles"
            },
        "4wires3":{
            "R":[
                [0.4576, 0.1559, 0.1535],
                [0.1559, 0.4666, 0.1580],
                [0.1535, 0.1580, 0.4615]
                ],
            "X":[
                [1.4133, 0.8515, 0.7266],
                [0.8515, 1.4133, 0.7802],
                [0.7266, 0.7802, 1.4133]
                ],
            "unit":"miles"
            },
            }
    }   
    grid_1 = grid()
    grid_1.read(data)  # Load data

    grid_1.pf()  # solve power flow
 
    error_v4_a = (abs(V4_ag)-abs(grid_1.res['4'].v_ag))/abs(V4_ag)*100
    error_v4_b = (abs(V4_bg)-abs(grid_1.res['4'].v_bg))/abs(V4_bg)*100
    error_v4_c = (abs(V4_cg)-abs(grid_1.res['4'].v_cg))/abs(V4_cg)*100
                        
    assert abs(error_v4_a)<0.05 # as stated by Dugan
    assert abs(error_v4_b)<0.05 # as stated by Dugan
    assert abs(error_v4_c)<0.05 # as stated by Dugan

if __name__ == "__main__":
#    test_Dyg11_3w()
    # test_Ygd11_3w_OC()
    # test_Ygd11_3w_SC()

    test_ieee4bus_Dyn11()

    pass

#    test_Dyn11()
#    test_Dyg11_3w()
