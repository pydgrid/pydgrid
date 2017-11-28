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

def test_line_sequence_z():
    ''' Test that positive sequence phasor calculations match pydgrid result'''
    data = {
        "lines":[
                {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "RX", "m": 1000}
                ],
        "buses":[
        		{"bus": "Bus_1",  "pos_x": 10, "pos_y":  0, "units": "m", "U_kV":0.4},
        		{"bus": "Bus_2",  "pos_x": 200, "pos_y": 0, "units": "m", "U_kV":0.4}
        		],
        "grid_formers":[
        		{"bus": "Bus_1","bus_nodes": [1, 2, 3],
        			"kV": [11.547, 11.547, 11.547],
        			"deg": [0, 120, 240.0]
        		}
        		],
        "loads":[
        		{"bus": "Bus_2" , "kVA": 2000.0, "pf": 0.9,"type":"3P"}
                ],
        "line_codes":
        		{"RX":
        		{"R1":0.8, "X1":0.6,"R0":2.4, "X0":1.8
        		}
        		}
        }

    # pydgrid calculation
    sys1 = grid()
    sys1.read(data)  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow
    sys1.get_v()      # post process voltages
    sys1.get_i()      # post process currents
    I_12_pydgrid = sys1.lines[0]['i_a_m']

    # positive sequence "manual" calculation
    V_1_m = sys1.buses[0]['v_an']
    V_2_m = sys1.buses[1]['v_an']
    theta_1 = np.deg2rad(sys1.buses[0]['deg_an'])
    theta_2 = np.deg2rad(sys1.buses[1]['deg_an'])
    V_1 = V_1_m*np.exp(1j*theta_1)
    V_2 = V_2_m*np.exp(1j*theta_2)
    R_1 = data["line_codes"]["RX"]["R1"]
    X_1 = data["line_codes"]["RX"]["X1"]
    Z_1 = R_1 + 1j*X_1
    I_12_manual = np.abs((V_1-V_2)/Z_1)

    # comparison
    error = I_12_manual - I_12_pydgrid

    assert abs(error)<0.001
#    phases = ['v_an','v_bn','v_cn']
#    for bus in sys1.buses:
#        for phase in phases:
#            print(bus[phase])

def test_pr_mt_h():
    ''' Test that positive sequence phasor calculations match pydgrid result'''
    data = {
        "lines":[
                {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "RX", "m": 200}
                ],
        "buses":[
        		{"bus": "Bus_1",  "pos_x": 10, "pos_y":  0, "units": "m", "U_kV":0.4},
        		{"bus": "Bus_2",  "pos_x": 200, "pos_y": 0, "units": "m", "U_kV":0.4}
        		],
        "grid_formers":[
        		{"bus": "Bus_1","bus_nodes": [1, 2, 3],
        			"kV": [11.547, 11.547, 11.547],
        			"deg": [0, 120, 240.0]
        		}
        		],
        "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],
                "kW": [0, 0, 0], "kvar": [0,0,0],
                "kA": [-0.245,-0.245,-0.245], "phi_deg":[-36.8698976, -36.8698976, -36.8698976]}],
        "line_codes":
        		{"RX":
        		{"R1":0.277, "X1":0.11,"R0":0.0, "X0":0.01
        		}
        		}
        }

    # pydgrid calculation
    sys1 = grid()
    sys1.read(data)  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow
    sys1.get_v()      # post process voltages
    sys1.get_i()      # post process currents
#    I_12_pydgrid = sys1.lines[0]['i_a_m']
#
#    # positive sequence "manual" calculation
    V_1_m = sys1.buses[0]['v_an']
    V_2_m = sys1.buses[1]['v_an']

    DV = V_1_m - V_2_m
    DU_pydgrid = np.sqrt(3)*DV
    DU_catalog = 24.41

    # comparison
    error = DU_pydgrid - DU_catalog

    assert abs(error)<0.001
#    phases = ['v_an','v_bn','v_cn']
#    for bus in sys1.buses:
#        for phase in phases:
#            print(bus[phase])


if __name__ == "__main__":

#    test_line_sequence_z()
    test_pr_mt_h()
