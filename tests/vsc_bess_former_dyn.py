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
"lines":[
		{"bus_j": "B1",  "bus_k": "B2",  "code": "UG1", "m": 50.0},
		{"bus_j": "B2",  "bus_k": "B3",  "code": "UG1", "m": 100.0}
		],
"buses":[
		{"bus": "B1",  "pos_x":  0,  "pos_y": 0, "units": "m", "U_kV":0.4},
		{"bus": "B2",  "pos_x":100,  "pos_y": 0, "units": "m", "U_kV":0.4},
		{"bus": "B3",  "pos_x":200,  "pos_y": 0, "units": "m", "U_kV":0.4}
		],
"grid_formers":[
		{"bus": "B1",
			"bus_nodes": [1, 2, 3, 4], "deg": [0, -120, -240, 0.0],
			"kV": [0.23, 0.23, 0.23, 0.0], "code":"bess_100kVA_300kWh"},
		{"bus": "B3",
			"bus_nodes": [1, 2, 3, 4], "deg": [0, -120, -240, 0.0],
			"kV": [0.23, 0.23, 0.23, 0.0], "code":"bess_100kVA_300kWh"},
		],
"grid_feeders":[{ "bus": "B2","bus_nodes": [1, 2, 3, 4],
					"kW": [-100.0, -0.0, -0.0], "kvar": [-20.0,0.0,0.0],
					"kA": [0.0,0.0,0.0], "phi_deg":[-90, -90, -90]}
				],
"shunts":[
		{"bus": "B1" , "R": 1.0, "X": 0.0, "bus_nodes": [4,0]},
		{"bus": "B3" , "R": 1.0, "X": 0.0, "bus_nodes": [4,0]}
		],
"bess_vsc":{
            "bess_100kVA_300kWh":{"ctrl_mode":3, "s_n_kVA":100.0, "V_dc":800.0, 
                     "soc_max_kWh":300.0, "soc_ini_kWh":100.0, 
                     "source_mode":"grid_former", "L":1.0e-3, "R":1.0,
                     "R_0":0.1, "R_1":0.2, "C_1":100.0,
                     "K_v":0.02, "K_ang":0.02,"T_v":1, "T_ang":1 }},
"sim_params":{"Dt":0.01}
}

grid_1 = grid()
grid_1.read(data)  # Load data
simu_1 = simu(grid_1) 

grid_1.pf()  # solve power flow
simu_1.ini()
simu_1.run(10)
    
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
