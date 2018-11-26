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


def test_wind_farm_ss():
    p_gen = 2000.0  # kW
    q_gen = 0       # kvar

    p_statcom = 0.0  # kW
    q_statcom = 0.0     # kvar

    data = {
        "lines":[
            {"bus_j": "W1mv",  "bus_k": "W2mv",   "code": "mv_al_300", "m":500},
            {"bus_j": "W2mv",  "bus_k": "W3mv",   "code": "mv_al_300", "m":500},    
            {"bus_j": "W3mv",  "bus_k": "POImv",  "code": "mv_al_300", "m":500},      
            {"bus_j": "POI",  "bus_k": "GRID",  "code": "hv_line", "m":50.0e3},
                ],
        "buses":[
                {"bus": "W1lv",  "pos_x": -1500.0, "pos_y":  200.0, "units": "m", "U_kV":0.69},
                {"bus": "W2lv",  "pos_x": -1000.0, "pos_y":  200.0, "units": "m", "U_kV":0.69},
                {"bus": "W3lv",  "pos_x":  -500.0, "pos_y":  200.0, "units": "m", "U_kV":0.69},
                {"bus": "W1mv",  "pos_x": -1500.0, "pos_y":  180.0, "units": "m", "U_kV":20.0},
                {"bus": "W2mv",  "pos_x": -1000.0, "pos_y":  180.0, "units": "m", "U_kV":20.0},
                {"bus": "W3mv",  "pos_x":  -500.0, "pos_y":  180.0, "units": "m", "U_kV":20.0},        
                {"bus": "POImv", "pos_x":     0.0, "pos_y":    0.0, "units": "m", "U_kV":20.0},
                {"bus": "POI",   "pos_x":   100.0, "pos_y":    0.0, "units": "m", "U_kV":66.0},
                {"bus": "GRID",  "pos_x":   500.0, "pos_y":    0.0, "units": "m", "U_kV":66.0},
                ],
        "transformers":[
                        {"bus_j": "POImv",  "bus_k": "POI",  "S_n_kVA": 10000.0, "U_1_kV":20.0, "U_2_kV":66.0,
                        "R_cc_pu": 0.01, "X_cc_pu":0.08, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                        {"bus_j": "W1mv",  "bus_k": "W1lv",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                        "R_cc_pu": 0.01, "X_cc_pu":0.06, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                        {"bus_j": "W2mv",  "bus_k": "W2lv",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                        "R_cc_pu": 0.01, "X_cc_pu":0.06, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                        {"bus_j": "W3mv",  "bus_k": "W3lv",  "S_n_kVA": 2500.0, "U_1_kV":20, "U_2_kV":0.69,
                        "R_cc_pu": 0.01, "X_cc_pu":0.06, "connection": "Dyg11_3w",   "conductors_1": 3, "conductors_2": 3},
                        ],
        "grid_formers":[
                {"bus": "GRID","bus_nodes": [1, 2, 3],
                    "kV": [38.105, 38.105, 38.105], "deg": [30, 150, 270.0]
                }
                ],
        "grid_feeders":[{"bus": "W1lv","bus_nodes": [1, 2, 3],"kW": p_gen, "kvar": q_gen},
                        {"bus": "W2lv","bus_nodes": [1, 2, 3],"kW": p_gen, "kvar": q_gen},
                        {"bus": "W3lv","bus_nodes": [1, 2, 3],"kW": p_gen, "kvar": q_gen},
                        {"bus": "POImv","bus_nodes": [1, 2, 3],"kW": p_statcom, "kvar": q_statcom} # STATCOM
        ],
        "groundings":[
            {"bus": "POImv" , "R_gnd":32.0, "X_gnd":0.0, "conductors": 3}
        ],
        "line_codes":
            {
            "mv_al_150":   {"R1":0.262,  "X1":0.118, "C_1_muF":0.250 },
            "mv_al_185":   {"R1":0.209,  "X1":0.113, "C_1_muF":0.281 },
            "mv_al_240":   {"R1":0.161,  "X1":0.109, "C_1_muF":0.301 },  
            "mv_al_300":   {"R1":0.128,  "X1":0.105, "C_1_muF":0.340 }, 
            "hv_line":  {"R1":0.219, "X1":0.365, "R0":0.219,   "X0":0.365}            
            }
        }

    grid_1 = grid()
    grid_1.read(data)  # Load data
    grid_1.pf()  # solve power flow
    mon = grid_1.monitor(bus_from='POI',bus_to='GRID')                   

    assert abs(mon.P-5910895.785662318)<0.0001     # from case resolved in november 2018
    assert abs(mon.Q-(-490329.45241958584))<0.0001 # from case resolved in november 2018


if __name__ == "__main__":

    test_wind_farm_ss()
    pass

