# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 16:35:40 2017

@author: jmmauricio
"""

import pydgrid

test=2

if test == 1:
    sys1 = pydgrid.grid()
    
    data = {
    "transformers":[
    		{"bus_j": "Bus_0",  "bus_k": "Bus_1",  "S_n_kVA": 150.0, "U_1_kV":20.0, "U_2_kV":0.4,
    		"R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyn11", 
    		"conductors_1": 3, "conductors_2": 4}
            ],
    "lines":[
            {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "UG1_luna", "m": 200.0}
            ],
    "buses":[
    		{"bus": "Bus_0",  "pos_x": 0, "pos_y":   0, "units": "m", "U_kV":20.0},
    		{"bus": "Bus_1",  "pos_x": 0, "pos_y":  10, "units": "m", "U_kV":0.4},
    		{"bus": "Bus_2",  "pos_x": 0, "pos_y": 200, "units": "m", "U_kV":0.4}
    		],
    "grid_formers":[
    		{"bus": "Bus_0",
              "bus_nodes": [10, 2, 3], "deg": [0, -120, -240], 
    		 "kV": [11.547, 11.547, 11.547]}
    		],
    "loads":[
    		{"bus": "Bus_2" , "kVA": 50.0, "pf": 0.85,"type":"1P+N","bus_nodes": [1,4]},
    		{"bus": "Bus_2" , "kVA": 30.0, "pf": 0.85,"type":"1P+N","bus_nodes": [2,4]},
    		{"bus": "Bus_2" , "kVA": 20.0, "pf": 0.85,"type":"1P+N","bus_nodes": [3,4]}
            ],
    "shunts":[
    		{"bus": "Bus_1" , "R": 0.0001, "X": 0.0, "bus_nodes": [4,0]},
    		{"bus": "Bus_2" , "R": 0.0001,   "X": 0.0, "bus_nodes": [4,0]}
            ]
    }
            
    sys1.read(data)  # Load data
    sys1.pf()
    sys1.get_v()
    sys1.get_i()



if test == 2:
    sys1 = pydgrid.grid()
    
    data = {
    "transformers":[
    		{"bus_j": "Bus_0",  "bus_k": "Bus_1",  "S_n_kVA": 150.0, "U_1_kV":20.0, "U_2_kV":0.4,
    		"R_cc_pu": 0.01, "X_cc_pu":0.04, "connection": "Dyn11", 
    		"conductors_1": 3, "conductors_2": 4}
            ],
    "lines":[
            {"bus_j": "Bus_1",  "bus_k": "Bus_2",  "code": "UG1_luna", "m": 200.0}
            ],
    "buses":[
    		{"bus": "Bus_0",  "pos_x": 0,  "pos_y": 0, "units": "m", "U_kV":20.0},
    		{"bus": "Bus_1",  "pos_x":10,  "pos_y": 0, "units": "m", "U_kV":0.4},
    		{"bus": "Bus_2",  "pos_x":200, "pos_y": 0, "units": "m", "U_kV":0.4}
    		],
    "grid_formers":[
    		{"bus": "Bus_0",
              "bus_nodes": [1, 2, 3], "deg": [0, -120, -240], 
    		 "kV": [11.547, 11.547, 11.547]}
    		],
    "grid_feeders":[{"bus": "Bus_2","bus_nodes": [1, 2, 3, 4],
                     "kW": [0, 0, 0], "kvar": [0,0,0],
                     "kA": [.5,.5,.5], "phi_deg":[-90, -90, -90]},
                   ],
    "shunts":[
    		{"bus": "Bus_1" , "R": 0.0001, "X": 0.0, "bus_nodes": [4,0]},
    		{"bus": "Bus_2" , "R": 0.0001, "X": 0.0, "bus_nodes": [4,0]}
            ]
    }
            
    sys1.read(data)  # Load data
    sys1.pf()
    sys1.get_v()
    sys1.get_i()
    print(sys1.params_pf['iters'])
    for item in ['v_an','v_bn','v_cn']:
        print(item,sys1.buses[2][item])

