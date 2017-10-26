#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid.pydgrid import grid
from pydgrid.pf import pf_eval,time_serie
from pydgrid.electric import bess_vsc_feeder, bess_vsc_feeder_eval
from pydgrid.simu import simu, f_eval, ini_eval, run_eval
import matplotlib.pyplot as plt
import numpy as np
import time

def test_solver1():
    sys1 = grid()
    sys1.read('./examples/kersting_ex6p1.json')  # Load data
    sys1.pf_solver = 1
    sys1.pf()  # solve power flow
    
    sys1.get_v()      # post process voltages
    sys1.get_i()      # post process currents

    expected_results = {'v_ab': 12469.993267073232,'v_an': 7199.5507766249302, 
                        'v_bc': 12469.99825654443,'v_bn': 7199.5575295511126,
                        'v_ca': 12469.991908615197,  'v_cn': 7199.55569880254723,
                        'deg_an': -3.3473807241894507e-05,'deg_bn': -120.00002841365294,'deg_cn': 119.99996507934871,'deg_ng': 0.0,
                        'p_a': -1799999.9999999979, 'p_b': -1800000.0000000126, 'p_c': -1799999.9999999909,
                        'q_a': -871779.78870811954, 'q_b': -871779.78870815237, 'q_c': -871779.7887081306}
    for item in expected_results:
        den = expected_results[item]
        if abs(den)<0.001:
            den = 0.001
        relative_error = (sys1.buses[1][item] - expected_results[item])/den
        
        assert abs(relative_error)<0.001

def test_solver2():
    sys1 = grid()
    sys1.read('./examples/kersting_ex6p1.json')  # Load data
    sys1.pf_solver = 2
    sys1.pf()  # solve power flow
    
    sys1.get_v()      # post process voltages
    sys1.get_i()      # post process currents

    expected_results = {'v_ab': 12469.993267073232,'v_an': 7199.5507766249302, 
                        'v_bc': 12469.99825654443,'v_bn': 7199.5575295511126,
                        'v_ca': 12469.991908615197,  'v_cn': 7199.55569880254723,
                        'deg_an': -3.3473807241894507e-05,'deg_bn': -120.00002841365294,'deg_cn': 119.99996507934871,'deg_ng': 0.0,
                        'p_a': -1799999.9999999979, 'p_b': -1800000.0000000126, 'p_c': -1799999.9999999909,
                        'q_a': -871779.78870811954, 'q_b': -871779.78870815237, 'q_c': -871779.7887081306}
    for item in expected_results:
        den = expected_results[item]
        if abs(den)<0.001:
            den = 0.001
        relative_error = (sys1.buses[1][item] - expected_results[item])/den
        
        assert abs(relative_error)<0.001
        


#    Phases = ['an','bn','cn']
#    for bus in sys1.buses:
#        for ph in Phases:
#            print('V_{:s}_n = {:2.2f}|{:2.2f}º V'.format(ph,bus['v_'+ph],bus['deg_'+ph]))
#    
#    Phases = ['a','b','c']
#    for line in sys1.lines:
#        for ph in Phases:
#            print('I_{:s}_n = {:2.2f}|{:2.2f}º A'.format(ph,line['i_'+ph+'_m'],line['deg_'+ph]))
#            
#
    
