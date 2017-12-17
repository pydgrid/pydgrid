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
		{"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "UG1", "m": 100.0},
		{"bus_j": "Bus_3",  "bus_k": "Bus_2",  "code": "UG1", "m": 100.0}
		],
"buses":[
		{"bus": "Bus_1",  "pos_x":  0,  "pos_y": 0, "units": "m", "U_kV":0.4},
		{"bus": "Bus_2",  "pos_x":100,  "pos_y": 0, "units": "m", "U_kV":0.4},
		{"bus": "Bus_3",  "pos_x":200,  "pos_y": 0, "units": "m", "U_kV":0.4}
		],
"grid_formers":[
		{"bus": "Bus_1",
			"bus_nodes": [1, 2, 3, 4], "deg": [0, -120, -240],
			"kV": [0.23, 0.23, 0.23]},
		{"bus": "Bus_3",
			"bus_nodes": [1, 2, 3, 4], "deg": [0, -120, -240],
			"kV": [0.23, 0.23, 0.23]}
		],
"grid_feeders":[{ "bus": "Bus_2","bus_nodes": [1, 2, 3, 4],
					"kW": [-0.0, -0.0, -0.0], "kvar": [0.0,0.0,0.0],
					"kA": [0.0,0.0,0.0], "phi_deg":[-90, -90, -90]}
				],
"shunts":[
		{"bus": "Bus_1" , "R": 0.0001, "X": 0.0, "bus_nodes": [4,0]},
		{"bus": "Bus_3" , "R": 0.0001, "X": 0.0, "bus_nodes": [4,0]}
		]
}

sys1 = grid()
sys1.read(data)  # Load data
#sys1.pf()  # solve power flow


#sys1.get_v()      # post process voltages
#sys1.get_i()      # post process currents
#
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
