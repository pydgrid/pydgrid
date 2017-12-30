#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid import grid
from pydgrid.pydgrid import phasor2time, pq
from pydgrid.pf import pf_eval,time_serie
from pydgrid.electric import bess_vsc, bess_vsc_eval
from pydgrid.simu import simu, f_eval, ini_eval, run_eval
import matplotlib.pyplot as plt
import numpy as np
import time


#def test_vsc_lipo():

data = {
"buses":[
        {"bus": "Bus_1",  "pos_x":   0.0, "pos_y": 0, "units": "m", "U_kV":0.4},
        {"bus": "Bus_2",  "pos_x":  10.0, "pos_y": 0, "units": "m", "U_kV":0.4},
        ],
"lines":[
        {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "UG1", "m": 100.0}
        ],
"grid_formers":[
        {"bus": "Bus_1",
        "bus_nodes": [1, 2, 3], "deg": [0, -120, -240],
        "kV": [0.23094, 0.23094, 0.23094], "code":"bess_100kVA_300kWh", "N_conductors":3}
        ],
"grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3],
                "kW": [0,0,0], "kvar": [0,0,0],
                "kA": [0,0,0], "phi_deg":[30, 30, 30], "code":"load_100kVA_300kWh",
                "shape":"shape_1", "N_conductors":3}],
"line_codes":
    {"pry_al_50":  {"R1":0.8,    "X1":	0.148, "R0":0.8,   "X0":	0.148},
     "pry_al_95":  {"R1":0.403,  "X1":	0.129, "R0":0.403, "X0":	0.129},
     "pry_al_120": {"R1":0.321,  "X1":	0.123, "R0":0.321, "X0":	0.321},
     "pry_al_185": {"R1":0.209,  "X1":	0.113, "R0":0.209, "X0":	0.209},
     "pry_al_300": {"R1":0.128,  "X1":	0.105, "R0":0.128, "X0":	0.128}
     },
"shunts":[
        {"bus": "Bus_1" , "R": 0.1, "X": 0.0, "bus_nodes": [4,0]},
        {"bus": "Bus_2" , "R": 0.1, "X": 0.0, "bus_nodes": [4,0]}
        ],
"bess_vsc":{
            "bess_100kVA_300kWh":{"ctrl_mode":3, "s_n_kVA":100.0, "V_dc":800.0, 
                     "soc_max_kWh":300.0, "soc_ini_kWh":100.0, 
                     "source_mode":"grid_former", "L":1.0e-3, "R":1.0,
                     "R_0":0.00206732473453, "R_1":0.00174134896562, "C_1":29358.4107982,
                     "K_v":0.02, "K_ang":0.02,"T_v":1, "T_ang":1,
                     "soc_ah_e":[[0.0,3.0],[5.0,3.28],[30,3.31],[36.57,3.35],[40.6,3.4],
                                 [41.28,3.42],[42,3.45],[42.4,3.5],[42.6,3.57],[42.87,3.79],[42.94,3.9]],
                                 "N_serie":213,"N_parallel":4},
            "load_100kVA_300kWh":{"ctrl_mode":12, "s_n_kVA":100.0, "V_dc":800.0, 
                     "soc_max_kWh":300.0, "soc_ini_kWh":100.0, 
                     "source_mode":"grid_feeder", "L":1.0e-3, "R":1.0,
                     "R_0":0.00206732473453, "R_1":0.00174134896562, "C_1":29358.4107982,
                     "soc_ah_e":[[0.0,3.0],[5.0,3.28],[30,3.31],[36.57,3.35],[40.6,3.4],
                                 [41.28,3.42],[42,3.45],[42.4,3.5],[42.6,3.57],[42.87,3.79],[42.94,3.9]],
                                 "N_serie":213,"N_parallel":4}
            },
"shapes":{"shape_1":{"t_s":[0,100,200,3600*24],
                     "kW":  [0,100,-100,0],
                     "kvar":[0,0,0,0]
                     }},
"sim_params":{"Dt":1.0}          
}


grid_1 = grid()
grid_1.read(data)  # Load data
simu_1 = simu(grid_1) 

grid_1.pf()  # solve power flow
simu_1.ini()
simu_1.run(200)

fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(8, 8), sharex = True)


axes[0].plot(simu_1.T, abs(simu_1.V_nodes))
axes[1].plot(simu_1.T, simu_1.X[:,0])
axes[1].plot(simu_1.T, simu_1.X[:,10])

axes[0].set_ylim((220,240))

axes[0].grid(True)
axes[1].grid(True)
    
#t = 0.0
#ini_eval(t,
#         grid_1.params_pf,
#         simu_1.params_simu,
#         simu_1.params_bess_vsc)
#
#T,V_nodes,I_nodes,X = run_eval(10,
#                               grid_1.params_pf,
#                               simu_1.params_simu,
#                               simu_1.params_bess_vsc)
#
#grid_1.get_v()      # post process voltages
#grid_1.get_i()      # post process currents 
#v_2_a,v_2_b,v_2_c,t = phasor2time(sys1.v_abc('Bus_3'))
#i_2_a,i_2_b,i_2_c,t = phasor2time(sys1.i_abc('Bus_3'))
#p,q,q_lipo,t = pq(sys1.v_abc('Bus_3'),sys1.i_abc('Bus_3'))
    
#    assert np.abs(p_ref-np.average(p))< 1.0
#    assert np.abs(p_ref-np.max(p))< 1.0
#    assert np.abs(p_ref-np.min(p))< 1.0
#    assert np.abs(np.average(q_lipo)-np.max(q_lipo))< 1.0
#    assert np.abs(np.average(q_lipo)-np.min(q_lipo))< 1.0
        
if __name__ == "__main__":
    pass
    #test_vsc_leon()

#    test_Dyn11()
#    test_Dyg11_3w()
