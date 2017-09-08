#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 11:41:44 2017

@author: jmmauricio
"""

import numpy as np
import numba

'''

Calculando inversa deY_ii, usando producto en pf.py
Y_primitive 2.7596044540405273
Y_primitive 0.002088785171508789
Ys calc 0.24035334587097168
inv_Y_ii 7.129778146743774
sys1.read() 10.854152202606201
sys1.pf() 0.5933837890625
'''
@numba.jit(nopython=True,cache=True)
def pf_eval(params,ig=0,max_iter=50):
    '''
    
    
    '''
    Y_vv =  params[ig].Y_vv
    inv_Y_ii = params[ig].inv_Y_ii
    #Y_ii = params[ig].Y_ii
    Y_iv =  params[ig].Y_iv
    N_v = params[ig].N_nodes_v
    N_i = params[ig].N_nodes_i
    N_nz_nodes = params[ig].N_nz_nodes
    
    N_pq_3pn  = params[ig].N_pq_3pn
    pq_3pn_int = params[ig].pq_3pn_int
    pq_3pn     = params[ig].pq_3pn
    N_pq_3p  = params[ig].N_pq_3p
    pq_3p_int = params[ig].pq_3p_int
    pq_3p     = params[ig].pq_3p
    N_pq_1p  = params[ig].N_pq_1p
    pq_1p_int = params[ig].pq_1p_int
    pq_1p     = params[ig].pq_1p
    N_pq_1pn  = params[ig].N_pq_1pn
    pq_1pn_int = params[ig].pq_1pn_int
    pq_1pn     = params[ig].pq_1pn
    
    V_node = params[ig].V_node
    I_node = params[ig].I_node
    
    V_unknown = np.copy(V_node[N_v:])
    I_known   = np.copy(I_node[N_v:])
    V_known   = np.copy(V_node[0:N_v])
    
    Y_vi =  Y_iv.T
    V_unknown_0 = V_unknown
    
    #print(np.abs(V_unknown))
    for iteration in range(max_iter):
        
        I_known   = np.copy(I_node[N_v:])
        
        if N_pq_3pn > 0:
            for it in range(pq_3pn_int.shape[0]):
               
                V_abc = V_unknown[pq_3pn_int[it][0:3],0]
                S_abc_3 = pq_3pn[it,:]
               
                I_known[pq_3pn_int[it][0:3],0] = np.conj(S_abc_3/V_abc)
                I_known[pq_3pn_int[it][3],0] =  -np.sum(I_known[pq_3pn_int[it][0:3],0])
                
        if N_pq_3p > 0:        
            for it in range(pq_3p_int.shape[0]):
                
                V_abc = V_unknown[pq_3p_int[it],0]
                S_abc_1 = pq_3p[it,0]
               
                I_known[pq_3p_int[it],0] = np.conj(S_abc_1/V_abc)
                #I_known[pq_3p_int[it][0],0] =  -np.sum(I_known[pq_3p_int[it][0:3],0])

        if N_pq_1p > 0:
             
            for it in range(pq_1p_int.shape[0]):
                
                V_abc = V_unknown[pq_1p_int[it],0]
                S_abc = pq_1p[it,:]
               
                I_known[pq_1p_int[it],0] = np.conj(S_abc/V_abc)
                #I_known[pq_3p_int[it][0],0] =  -np.sum(I_known[pq_3p_int[it][0:3],0])           
 
        if N_pq_1pn > 0:
             
            for it in range(pq_1pn_int.shape[0]):
                a=1
                
                V_ph = V_unknown[pq_1pn_int[it][0],0]
                V_n  = V_unknown[pq_1pn_int[it][1],0]
                S_pn = pq_1pn[it,0]
               
                I_pn = np.conj(S_pn/(V_ph-V_n))
                
                I_known[pq_1pn_int[it][0],0] +=  I_pn
                I_known[pq_1pn_int[it][1],0] += -I_pn  
                
        I_aux = ( I_known - Y_iv @ V_known)    
        V_unknown = inv_Y_ii[:,0:N_nz_nodes] @ I_aux[0:N_nz_nodes,:]
        #V_unknown = inv_Y_ii  @ I_aux 
        #V_unknown = np.linalg.solve(Y_ii, I_known - Y_iv @ V_known)
        
        if np.linalg.norm(V_unknown - V_unknown_0,np.inf) <1.0e-10: break
        V_unknown_0 = V_unknown

    I_unknown =Y_vv @ V_known + Y_vi @ V_unknown
    
    V_node[0:N_v,:] = V_known 
    V_node[N_v:,:]  = V_unknown 

    I_node[0:N_v,:] = I_unknown 
    I_node[N_v:,:]  = I_known 
    
    params[ig].iters = iteration
        
    return V_node,I_node


@numba.jit(nopython=True,cache=True)
def set_load_factor(t,params_pf,params_lshapes,ig=0):
    for it in range(params_lshapes[ig].N_loads):
        time_idx = np.argmax(params_lshapes[ig].time[it,:]>t)
        params_pf[ig]['pq_1p'][it] = params_pf[ig]['pq_1p_0'][it] *params_lshapes[ig].shapes[it,time_idx] 
                

@numba.jit(nopython=True,cache=True)
def time_serie(t_ini,t_end,Dt,params_pf,params_lshapes):
    ig = 0
    N_times = int(np.ceil(t_end-t_ini)/Dt)
    N_v = params_pf[ig].N_nodes_v
    N_i = params_pf[ig].N_nodes_i
    N_nodes = int(N_v + N_i)
    V_nodes = np.zeros((N_times,N_nodes), dtype=np.complex128)
    I_nodes = np.zeros((N_times,N_nodes), dtype=np.complex128)
    for it in range(N_times):
        t=it*Dt
        set_load_factor(t,params_pf,params_lshapes,ig=0) 
        V_node,I_node = pf_eval(params_pf,ig=0,max_iter=50)
        V_nodes[it,:] = V_node[:,0]
        I_nodes[it,:] = I_node[:,0]
    return V_nodes,I_nodes

 
if __name__ == "__main__":
    import time
    import pydss
    test ='lveurope'
    if test=='lveurope': 
        t_0 = time.time()
        sys1 = pydss.pydss()
        sys1.read('lv_europe_connected.json')  # Load data
        sys1.read_loads_shapes('load_shapes_list.json')
        sys1.pf()
        t_0 = time.time()
        pf_eval(sys1.params_pf,ig=0,max_iter=50)
        print('pf_eval()',time.time()-t_0) 
        t_0 = time.time()
        t_ini = 0.0
        t_end = 24*60*60
        Dt = 60
        t_0 = time.time()
        V_nodes,I_nodes = time_serie(t_ini,t_end,Dt,sys1.params_pf,sys1.params_lshapes)
        print('time_serie()',time.time()-t_0) 