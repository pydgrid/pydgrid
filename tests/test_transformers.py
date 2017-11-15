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


def test_Dyn11_OC():
    '''
    Open circuit like test
    '''
    data = {
        "buses":[{"bus": "Bus_1",  "pos_x": 10.0, "pos_y":  0.0, "units": "m", "U_kV":20.0},
                 {"bus": "Bus_2",  "pos_x": 15.0, "pos_y":  0.0, "units": "m", "U_kV":0.4}],
        "transformers":[{"bus_j": "Bus_1",  "bus_k": "Bus_2",  "S_n_kVA": 1000.0, "U_j_kV":20.0, "U_k_kV":0.4,
                        "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyn11",   "conductors_j": 3, "conductors_k": 4}],
        "grid_formers":[{"bus": "Bus_1","bus_nodes": [1, 2, 3],"kV": [11.547, 11.547, 11.547], "deg": [0, 120, 240.0]}],
        "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],"kW": [0,0,0], 
                         "kvar": [0,0,0],"kA": [0,0,0], "phi_deg":[0, 0, 0]}],
        "shunts":[{"bus": "Bus_2" , "R": 0.001, "X": 0.0, "bus_nodes": [4,0]}]}
    
    # pydgrid calculation
    sys1 = grid()
    sys1.read(data)  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow    
    sys1.get_v()      # post process voltages
    
    # positive sequence calculation
    U_1_n = data["transformers"][0]["U_j_kV"]*1000
    U_2_n = data["transformers"][0]["U_k_kV"]*1000
    r_t = U_1_n/U_2_n
    
    V_2_manual  = U_1_n/np.sqrt(3)/r_t*np.exp(1j*np.deg2rad(30))
    V_2_pydgrid = sys1.buses[1]['v_an']*np.exp(1j*np.deg2rad(sys1.buses[1]['deg_an']))
    
    error = V_2_manual - V_2_pydgrid
    assert abs(error)<0.001

def test_Dyn11_SC():
    '''
    Short circuit like test
    '''
    data = {
        "buses":[{"bus": "Bus_1",  "pos_x": 10.0, "pos_y":  0.0, "units": "m", "U_kV":0.4},
                 {"bus": "Bus_2",  "pos_x": 15.0, "pos_y":  0.0, "units": "m", "U_kV":0.4}],
        "transformers":[{"bus_j": "Bus_1",  "bus_k": "Bus_2",  "S_n_kVA": 1000.0, "U_j_kV":20.0, "U_k_kV":0.4,
                        "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyn11",   "conductors_j": 3, "conductors_k": 4}],
        "grid_formers":[{"bus": "Bus_1","bus_nodes": [1, 2, 3],"kV": [11.547, 11.547, 11.547], "deg": [0, 120, 240.0]}],
        "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],"kW": [0,0,0], 
                         "kvar": [0,0,0],"kA": [0,0,0], "phi_deg":[0, 0, 0]}],
        "shunts":[{"bus": "Bus_2" , "R": 0.001, "X": 0.0, "bus_nodes": [4,0]},
                  {"bus": "Bus_2" , "R": 1.0e-8, "X": 0.0, "bus_nodes": [1,0]},
                  {"bus": "Bus_2" , "R": 1.0e-8, "X": 0.0, "bus_nodes": [2,0]},
                  {"bus": "Bus_2" , "R": 1.0e-8, "X": 0.0, "bus_nodes": [3,0]}]}
    
    U_1_n = data["transformers"][0]["U_j_kV"]*1000
    U_2_n = data["transformers"][0]["U_k_kV"]*1000
    
    R_cc_pu = data["transformers"][0]["R_cc_pu"]
    X_cc_pu = data["transformers"][0]["X_cc_pu"]
    Z_cc_pu = R_cc_pu + 1j*X_cc_pu
    
    V_cc = np.abs(Z_cc_pu)*U_1_n/np.sqrt(3)
    V_cc_kV = V_cc/1000
    data["grid_formers"][0]["kV"] = [V_cc_kV, V_cc_kV, V_cc_kV]
    
    # pydgrid calculation
    sys1 = grid()
    sys1.read(data)  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow    
    sys1.get_v()  # post process voltages
    sys1.get_i()  
    
    p_a,p_b,p_c = sys1.buses[0]['p_a'],sys1.buses[0]['p_b'],sys1.buses[0]['p_c']
    p_cc = p_a + p_b + p_c
    i_1a_m = sys1.transformers[0]['i_1a_m']
    R_cc_pydgrid = p_cc/(3*i_1a_m**2)
    Z_cc_pydgrid = V_cc/i_1a_m 
    X_cc_pydgrid = np.sqrt(Z_cc_pydgrid**2 - R_cc_pydgrid**2)
    Z_b = U_1_n**2/1000.0e3
    R_cc_pu_pydgrid = R_cc_pydgrid/Z_b    
    X_cc_pu_pydgrid = X_cc_pydgrid/Z_b
    Z_cc_pu_pydgrid = R_cc_pu_pydgrid + 1j*X_cc_pu_pydgrid
    print('Z_cc_pu',Z_cc_pu)
    print('Z_cc_pu_pydgrid',Z_cc_pu_pydgrid)
    error = Z_cc_pu - Z_cc_pu_pydgrid
    assert abs(error)<0.001
      

def test_Dyg11_3w():
    data = {"buses":[{"bus": "Bus_1",  "pos_x": 10.0, "pos_y":  0.0, "units": "m", "U_kV":20.0},
                     {"bus": "Bus_2",  "pos_x": 15.0, "pos_y":  0.0, "units": "m", "U_kV":0.4}],
            "transformers":[{"bus_j": "Bus_1",  "bus_k": "Bus_2",  "S_n_kVA": 1000.0, "U_j_kV":20.0, "U_k_kV":0.4,
                        "R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyg11_3w",   "conductors_j": 3, "conductors_k": 3}],
            "grid_formers":[{"bus": "Bus_1","bus_nodes": [1, 2, 3],"kV": [11.547, 11.547, 11.547], "deg": [0, 120, 240.0]}],
            "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],"kW": [0,0,0],"kvar": [0,0,0],"kA": [0,0,0], "phi_deg":[0, 0, 0]}]}
        
    # pydgrid calculation
    sys1 = grid()
    sys1.read(data)  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow    
    sys1.get_v()      # post process voltages
    
    # positive sequence calculation
    U_1_n = data["transformers"][0]["U_j_kV"]*1000
    U_2_n = data["transformers"][0]["U_k_kV"]*1000
    r_t = U_1_n/U_2_n
    
    V_2_manual  = U_1_n/np.sqrt(3)/r_t*np.exp(1j*np.deg2rad(30))
    V_2_pydgrid = sys1.buses[1]['v_an']*np.exp(1j*np.deg2rad(sys1.buses[1]['deg_an']))
    print('V_2_manual',V_2_manual)
    print('V_2_pydgrid',V_2_pydgrid)    
    error = V_2_manual - V_2_pydgrid
    assert abs(error)<0.001


if __name__ == "__main__":
#    test_Dyg11_3w()
    pass

#    test_Dyn11()
#    test_Dyg11_3w()
