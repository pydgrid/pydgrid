#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 18:24:45 2017

@author: jmmauricio
"""

import numpy as np
from pydgrid.electric import bess_vsc, bess_vsc_eval
from pydgrid.pf import pf_eval

import numba

class simu(object):  # feed mode
    
    def __init__(self,grid,ig=0):  # todo: define ig
        
#        if type(data_input) == str:
#            json_file = data_input
#            self.json_file = json_file
#            self.json_data = open(json_file).read().replace("'",'"')
#            data = json.loads(self.json_data)
#        elif type(data_input) == dict:
#            data = data_input
#            self.data = data
#
        data = grid.data
        self.data = data
        
        self.Dt = 0.1  # integration step size
        if 'sim_params' in data:
            sim_params = data['sim_params']
            if 'Dt'  in sim_params:
                self.Dt =sim_params['Dt']
                
                
            
       
        self.N_x = 0
        ix_0 = 0
        
        # bess_vsc_feeder
        obj_bess_vsc = bess_vsc(data,grid)
        for item in obj_bess_vsc.params_bess_vsc:
            item['ix_0'] = ix_0
            ix_0 += item['N_x']
 
        N_x = ix_0
        
        dtype = np.dtype([('t_ini', 'float64'),
                          ('t_end', 'float64'),
                          ('Dt', 'float64'),
                          ('N_x','int64'),
                          ('N_steps','int32'),
                          ('x',np.float64,(N_x,1)),('f',np.float64,(N_x,1)),('h',np.float64,(N_x,1)),
                          ('N_bess_vsc_feeder','int32')
                 ])
                     
        element_list = []
        
        element_list += [(0.0,
                          0.0,
                          self.Dt, # Dt
                          N_x, # N_x
                          0, # N_steps 
                          np.zeros((N_x,1)),np.zeros((N_x,1)),np.zeros((N_x,1)),   # x, f, h
                          len(obj_bess_vsc.params_bess_vsc)
                          )] 
    
        self.params_simu= np.rec.array(element_list,dtype=dtype)
        self.params_bess_vsc = obj_bess_vsc.params_bess_vsc
        self.params_pf = grid.params_pf
    
        self.T = np.empty((0,1))
        self.V_nodes = np.empty((0,grid.N_nodes))
        self.I_nodes = np.empty((0,grid.N_nodes))
        self.X = np.empty((0,N_x)) 

    def ini(self, t_ini=0.0):
        ini_eval(t_ini,
                 self.params_pf,
                 self.params_simu,
                 self.params_bess_vsc)
        
        
    def run(self, t_end):
        T,V_nodes,I_nodes,X = run_eval(t_end,
                               self.params_pf,
                               self.params_simu,
                               self.params_bess_vsc)
        
        self.T = np.vstack((self.T,T))
        self.V_nodes =  np.vstack((self.V_nodes,V_nodes))
        self.I_nodes =  np.vstack((self.I_nodes,I_nodes))
        self.X =  np.vstack((self.X,X))   
        
        
#@numba.jit(nopython=True,cache=True)    
def ini_eval(t,
           params_pf,
           params_simu,
           params_bess_vsc):
    
    params_simu[0]['t_ini'] = t    
    # bess_vsc
    bess_vsc_eval(t,1,params_bess_vsc,params_pf,params_simu)




#@numba.jit(nopython=True,cache=True)    
def f_eval(t,
           params_pf,
           params_simu,
           params_bess_vsc):
    
    # update elements derivatives:
    bess_vsc_eval(t,2,params_bess_vsc,params_pf,params_simu)
        

         
    
#@numba.jit(nopython=True,cache=True,nogil=True)    
def run_eval(t_end,
             params_pf,
             params_simu,
             params_bess_vsc):

    N_v = params_pf[0].N_nodes_v
    N_i = params_pf[0].N_nodes_i
    N_x = params_simu[0].N_x
    t_ini = params_simu[0]['t_ini']
    N_nodes = int(N_v + N_i)    
    N_steps = int(np.ceil((t_end-t_ini)/params_simu[0].Dt) ) 
    T = np.zeros((N_steps,1), dtype=np.float64)                # time ouput 
    V_nodes = np.zeros((N_steps,N_nodes), dtype=np.complex128) # voltages ouputs 
    I_nodes = np.zeros((N_steps,N_nodes), dtype=np.complex128) # currents ouputs 
    X = np.zeros((N_steps,N_x), dtype=np.float64) # currents ouputs 
    for it in range(N_steps):
        t = params_simu[0].Dt*it
        f_eval(t,
               params_pf,
               params_simu,
               params_bess_vsc)
        # ode solver        
        params_simu[0].x[:] += params_simu[0].Dt*params_simu[0].f    

        
        # update elements outputs:
        bess_vsc_eval(t,4,params_bess_vsc,params_pf,params_simu)

        # update power flow
        V_node, I_node = pf_eval(params_pf)
       
        # outputs update
        T[it,0] = t + params_simu[0]['t_ini']
        V_nodes[it,:] = V_node[:,0]
        I_nodes[it,:] = I_node[:,0]
        X[it,:] = params_simu[0].x[:,0]        
    params_simu[0].N_steps = N_steps    
    params_simu[0]['t_ini'] = t_end
    return T,V_nodes,I_nodes,X

    