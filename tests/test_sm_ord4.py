#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  9 23:22:02 2017

@author: jmmauricio
"""

from pydgrid.pydgrid import grid
from pydgrid.pf import pf_eval,time_serie
from pydgrid.electric import bess_vsc_feeder, bess_vsc_feeder_eval,sm_ord4_eval
from pydgrid.simu import simu, f_eval, ini_eval, run_eval
import matplotlib.pyplot as plt
import numpy as np
import time

def d2np(d):
    
    names = []
    numbers = ()
    dtypes = []
    for item in d:
        names += item   
        if type(d[item]) == float:
            numbers += (d[item],)
            dtypes += [(item,float)]
        if type(d[item]) == int:
            numbers += (d[item],)
            dtypes += [(item,int)]
        if type(d[item]) == np.ndarray:
            if d[item].dtype == np.dtype('int32'):
                numbers += (d[item],)
                dtypes += [(item,np.int32,d[item].shape)]
            if d[item].dtype == np.dtype('int64'):
                numbers += (d[item],)
                dtypes += [(item,np.int64,d[item].shape)]
            if d[item].dtype == np.dtype('float64'):
                numbers += (d[item],)
                dtypes += [(item,np.float64,d[item].shape)]
            if d[item].dtype == np.dtype('complex128'):
                numbers += (d[item],)
                dtypes += [(item,np.complex128,d[item].shape)]
    return np.rec.array([numbers],dtype=dtypes)

d =dict(
S_n = 2220.0e6,
U_n = 24e3,
V_dc_n = 5e3,
H = 3.5,
X_d = 1.81,
X_q = 1.76,
X1d = 0.3,
X1q = 0.65,
X2d = 0.23,
X2q = 0.25,
X_l = 0.15,
R_s = 0.003,
D = 0.01,
Omega_b = 2*np.pi*50,
T1d0 = 8.0,
T1q0 = 1.0,
T2d0 = 0.03,
T2q0 = 0.07,
V_m = 1.0,
theta= 0.0,
delta = 0.2,
omega = 1.0,
e1q = 0.2,
e1d = 1.0,
e_fd = 1.1,
p_m = 1.0,
p_e = 0.0,
P = 0.9,
Q = 0.436,
P_pu = 1.0,
Q_pu = 0.0,
i_d = 0.0,
i_q = 0.0,
I_m = 0.0,
theta_i = 0.0,
x=np.zeros((4,1)),
f=np.zeros((4,1)),
y=np.zeros((2,1)),
g=np.zeros((2,1)),
ix_0 = 0,
nodes = np.array([0,1,2,3]),
bus_nodes = np.array([0,1,2,3]),
N_conductors = 4,
ctrl_mode = 0,
gfeed_idx = np.array([0]),
i_abcn = np.zeros((4,1), np.complex128)
)
        
        
alpha = np.exp(2.0/3*np.pi*1j)
A_0a =  np.array([[1, 1, 1],
                  [1, alpha**2, alpha],
                  [1, alpha, alpha**2]])

A_a0 = 1/3* np.array([[1, 1, 1],
                      [1, alpha, alpha**2],
                      [1, alpha**2, alpha]])

params = d2np(d)

S = 0.9+1j*0.436
V_m = 1.0
theta = np.deg2rad(28.34)
V_pos = V_m*np.exp(1j*theta)
I_pos = np.conj(S/V_pos)
I_012 = np.zeros((3,1),np.complex128)
V_012 = np.zeros((3,1),np.complex128)
I_012[1,0] = I_pos
V_012[1,0] = V_pos
I_abc = A_0a @ I_012
V_abc = A_0a @ V_012
i_abcn = np.zeros((4,1),np.complex128)
v_abcn = np.zeros((4,1),np.complex128)
i_abcn[0:3,:] = I_abc
v_abcn[0:3,:] = V_abc

gfeed_powers = np.ones((1,4),np.complex128)*S
gfeed_currents = np.zeros((1,4),np.complex128)

d_pf =dict(
gfeed_powers = gfeed_powers,           
gfeed_currents = gfeed_currents,
i_abcn = i_abcn,
v_abcn = v_abcn,
V_node = v_abcn 
)

params_pf = d2np(d_pf)


d_simu =dict(
x = np.zeros((4,1))+0.0
)

params_simu = d2np(d_simu)


mode = 0
t = 0.0
sm_ord4_eval(t,mode,params,params_pf,params_simu)

print(params_simu.x)
print('e_fd',params.e_fd)
print('p_m',params.p_m)
#def test_sm_kundur13p2():
#    sys1 = grid()
#    sys1.read('./examples/kersting_ex6p1.json')  # Load data
#    sys1.pf_solver = 1
#    sys1.pf()  # solve power flow
#    
#    sys1.get_v()      # post process voltages
#    sys1.get_i()      # post process currents
#
#    expected_results = {'v_ab': 12469.993267073232,'v_an': 7199.5507766249302, 
#                        'v_bc': 12469.99825654443,'v_bn': 7199.5575295511126,
#                        'v_ca': 12469.991908615197,  'v_cn': 7199.55569880254723,
#                        'deg_an': -3.3473807241894507e-05,'deg_bn': -120.00002841365294,'deg_cn': 119.99996507934871,'deg_ng': 0.0,
#                        'p_a': -1799999.9999999979, 'p_b': -1800000.0000000126, 'p_c': -1799999.9999999909,
#                        'q_a': -871779.78870811954, 'q_b': -871779.78870815237, 'q_c': -871779.7887081306}
#    for item in expected_results:
#        den = expected_results[item]
#        if abs(den)<0.001:
#            den = 0.001
#        relative_error = (sys1.buses[1][item] - expected_results[item])/den
#        
#        assert abs(relative_error)<0.001
#
#def test_solver2():
#    sys1 = grid()
#    sys1.read('./examples/kersting_ex6p1.json')  # Load data
#    sys1.pf_solver = 2
#    sys1.pf()  # solve power flow
#    
#    sys1.get_v()      # post process voltages
#    sys1.get_i()      # post process currents
#
#    expected_results = {'v_ab': 12469.993267073232,'v_an': 7199.5507766249302, 
#                        'v_bc': 12469.99825654443,'v_bn': 7199.5575295511126,
#                        'v_ca': 12469.991908615197,  'v_cn': 7199.55569880254723,
#                        'deg_an': -3.3473807241894507e-05,'deg_bn': -120.00002841365294,'deg_cn': 119.99996507934871,'deg_ng': 0.0,
#                        'p_a': -1799999.9999999979, 'p_b': -1800000.0000000126, 'p_c': -1799999.9999999909,
#                        'q_a': -871779.78870811954, 'q_b': -871779.78870815237, 'q_c': -871779.7887081306}
#    for item in expected_results:
#        den = expected_results[item]
#        if abs(den)<0.001:
#            den = 0.001
#        relative_error = (sys1.buses[1][item] - expected_results[item])/den
#        
#        assert abs(relative_error)<0.001
        


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
    
