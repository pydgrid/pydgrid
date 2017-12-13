#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 12 17:55:24 2017

@author: jmmauricio
"""

import numpy as np
import numba
import json


# %%
class bess_vsc(object):  # feed mode
    
    '''
    
    problem: in np.rec.array elemennts of the same dtype must have the same size. 
    solution: one vector for every family, with pointers for accessing it from different users
    
    for grid_formers and grid_feeders
    relation between bess_vsc's and power flow sources given by:
        gfeed_idx for grid feeders
        gform_idx for grid formers
    '''
    
    def __init__(self,data_input,grid):
        
        if type(data_input) == str:
            json_file = data_input
            self.json_file = json_file
            self.json_data = open(json_file).read().replace("'",'"')
            data = json.loads(self.json_data)
        elif type(data_input) == dict:
            data = data_input
            self.data = data
        
        
        if not 'bess_vsc' in data:
            return
        else:
            bess_vsc = data['bess_vsc']
        
        N_x = 4
        ig = 0
        N_s_points = 100
        elements_data = []

        s_times = []
        s_shapes = []
        s_npoints = []
        gfeed_idx = 0
        gform_idx = 0
        for item in bess_vsc:
            if item['source_mode'] == 'grid_feeder': 
                source_mode = 0
                ctrl_mode = item['ctrl_mode']
                if 'p_ref' in item: p_ref = item['p_ref']
                if 'q_ref' in item: q_ref = item['q_ref']
                gfeed_idx = grid.gfeed_id.index(item['id'])
                bus_nodes = grid.gfeed_bus_nodes[gfeed_idx]+grid.N_nodes_v
                nodes =  grid.gfeed_bus_nodes[gfeed_idx]
            if item['source_mode'] == 'grid_former':
                source_mode = 1
                ctrl_mode = item['ctrl_mode']
                gform_idx = grid.gformer_id.index(item['id'])
                nodes = grid.gformer_nodes[gform_idx]
                bus_nodes = grid.gformer_bus_nodes[gform_idx] 
            
            N_x = N_x
            ix_0 = 0
            
            S_base = item['s_n_kVA']*1000.0
            V_dc  = item['V_dc']
            L  = item['L']
            R  = item['R']
            if 'C_ac' in item: 
                C_ac  = item['C_ac'] 
            else: 
                C_ac = 1e-8
            v_abcn_0 = np.zeros((4,1))
            i_abcn_0 = np.zeros((4,1))
            v_abcn = np.zeros((4,1))
            i_abcn = np.zeros((4,1))
            e_abcn = np.zeros((4,1))
            eta_abcn = np.zeros((4,1))
            S_ref = np.zeros((4,1))
            S = np.zeros((4,1))        
            S_0 = np.zeros((4,1))
            x   = np.zeros((N_x,1))
            f   = np.zeros((N_x,1))
            h   = np.zeros((N_x,1))            
            m = np.zeros((4,1))
            N_conductors= 4
            thermal_model = 0
            soc_max= item['soc_max_kWh']*1000*3600
            soc_0 = item['soc_ini_kWh']*1000*3600
            soc= item['soc_ini_kWh']*1000*3600
            switch = 1.0
            p_ref = 0.0
            q_ref = 0.0
            s_times  =  np.zeros((N_s_points,1))
            s_shapes =  np.zeros((N_s_points,1),dtype=np.complex128)  
            s_npoints = 0                                     
            if item["ctrl_mode"]==12:  # pq reference
                shape_id = item['shape']
                shape = data['shapes'][shape_id]
                npoints = len(shape['t_s'])
                s_times[0:npoints,0] = np.array(shape['t_s'])
                s_shapes[0:npoints,0] = (np.array(shape['kW']) + 1j*np.array(shape['kvar']))*1000
                s_npoints = npoints
   
            ig += 1
                
            elements_data += [
                             (source_mode,
                              ctrl_mode,
                              gfeed_idx,
                              gform_idx,
                              N_x,
                              ix_0,
                              nodes,
                              bus_nodes,
                              S_base,
                              L,
                              R,
                              C_ac,
                              V_dc,
                              e_abcn,
                              eta_abcn,
                              v_abcn_0,
                              i_abcn_0,
                              v_abcn,
                              i_abcn,
                              S_ref,
                              S,      
                              S_0,
                              x,
                              f,
                              h,           
                              m,
                              N_conductors,
                              thermal_model,
                              soc_max,
                              soc_0,
                              soc,
                              switch,
                              s_times,
                              s_shapes,
                              s_npoints,
                              p_ref,
                              q_ref
                             )
                             ]
            
        dtype_list =[ ('source_mode','int32'),
                      ('ctrl_mode','int32'),# ctrl_mode_list
                      ('gfeed_idx','int32'), # g_idx_list
                      ('gform_idx','int32'), # g_idx_list
                      ('N_x','int32'),
                      ('ix_0','int32'), # N_x_list, ix_0_list
                      ('nodes',np.int32,(4,)),  #  bus_nodes_list
                      ('bus_nodes',np.int32,(4,)),  #  bus_nodes_list
                      ('S_base',np.float64),  # S_base_list
                      ('L','float64'), # switch_list
                      ('R','float64'), # switch_list
                      ('C_ac','float64'), # switch_list
                      ('V_dc',np.float64), # V_dc_list
                      ('e_abcn',np.complex128,(4,1)), # 
                      ('eta_abcn',np.complex128,(4,1)), # 
                      ('v_abcn_0',np.complex128,(4,1)), # 
                      ('i_abcn_0',np.complex128,(4,1)), # 
                      ('v_abcn',np.complex128,(4,1)), # 
                      ('i_abcn',np.complex128,(4,1)), # 
                      ('S_ref',np.complex128,(4,1)), # S_ref_list
                      ('S',np.complex128,(4,1)), # S_list
                      ('S_0',np.complex128,(4,1)), # S_0_list
                      ('x',np.float64,(N_x,1)),  #  x_list
                      ('f',np.float64,(N_x,1)),  # f_list
                      ('h',np.float64,(N_x,1)), # h_list
                      ('m','float64',(4,1)), # m_list
                      ('N_conductors','int32'), # N_conductors_list
                      ('thermal_model','int32'), # thermal_model_list
                      ('soc_max','float64'), # soc_max_list
                      ('soc_0','float64'), # soc_0_list
                      ('soc','float64'),  # soc_list
                      ('switch','float64'), # switch_list
                      ('s_times',np.float64,(N_s_points,1)), # s_times
                      ('s_shapes',np.complex128,(N_s_points,1)), # s_shapes
                      ('s_npoints','int64'),  # s_npoints     
                      ('p_ref','float64'),
                      ('q_ref','float64')
                     ]
        dtype = np.dtype(dtype_list)     
        
        self.params_bess_vsc  = np.rec.array(elements_data,dtype=dtype) 
        self.N_bess_vsc = ig
        self.N_x = N_x


        
    def thermal_abb(self, file_1,file_2,idxs_1,idxs_2,Rth_sink,tau_sink,T_a,N_switch_sink):       
        '''
        I_rms  -> 15
        p_igbt -> 2
        p_diode-> 6
        fp-> 17
        V_rms -> 14
        T_igbt -> 3
        T_diode -> 7
        '''
        
        # Test group 2
        fobj = open(file_1)
        lines = fobj.readlines()
        fobj.close()
        N_tests = int(len(lines)/22)
        tests_list = []
        for it in range(N_tests):
            tests_list+= [[float(item.split(' ')[0]) for item in lines[it::N_tests]]]    
        tests_1 = np.array(tests_list)
        
        
        # Test group 2
        fobj = open(file_2)
        lines = fobj.readlines()
        fobj.close()    
        N_tests = int(len(lines)/22)
        tests_list = []
        for it in range(N_tests):
            tests_list+= [[float(item.split(' ')[0]) for item in lines[it::N_tests]]]    
        tests_2 = np.array(tests_list)
                
        # merge Test_1 and Test_2 data
        i =   np.hstack((tests_1[idxs_1,15],tests_2[idxs_2,15]))
        p_i = np.hstack((tests_1[idxs_1,2] ,tests_2[idxs_2,2]))
        p_d = np.hstack((tests_1[idxs_1,6] ,tests_2[idxs_2,6]))
        fp =  np.hstack((tests_1[idxs_1,17],tests_2[idxs_2,17]))
        m =   np.hstack((tests_1[idxs_1,14],tests_2[idxs_2,14]))*np.sqrt(2)/700*2
        alpha = fp*m
        
        # Compute coeficients
        A = np.zeros((5,5))
        b_i = np.zeros((5,1))
        b_d = np.zeros((5,1))
        for it in range(5):
            A[it,:] = np.array([1.0, i[it], i[it]*alpha[it], i[it]**2, i[it]**2*alpha[it]])
            b_i[it] = p_i[it]
            b_d[it] = p_d[it]
            
        self.coef_i = np.linalg.inv(A) @ b_i
        self.coef_d = np.linalg.inv(A) @ b_d

        
        a_i = self.coef_i[0]
        b_i = self.coef_i[1]
        c_i = self.coef_i[2]
        d_i = self.coef_i[3]
        e_i = self.coef_i[4]
        a_d = self.coef_d[0]
        b_d = self.coef_d[1]
        c_d = self.coef_d[2]
        d_d = self.coef_d[3]
        e_d = self.coef_d[4]
        
#        def p_igbt_eval(i,m,fp):    
#            return a_i + (b_i + c_i*m*fp)*i + (d_i + e_i*m*fp)*i**2
#        
#        def p_diode_eval(i,m,fp):    
#            return a_d + (b_d + c_d*m*fp)*i + (d_d + e_d*m*fp)*i**2
        # Thermal from central test_1 data
        p_igbt_test_1 = p_i[1]
        p_diode_test_1 = p_d[1]
        

        p_total = p_igbt_test_1+p_diode_test_1
        T_sink = T_a + p_total*Rth_sink
        
        Rth_c_igbt = 0.04069
        Rth_c_diode = 0.0195818

    # T_j_igbt = T_sink + p_igbt*(Rth_j_igbt+Rth_c_igbt)
    
        Rth_j_igbt  = (tests_1[idxs_1[1],3] - T_sink)/p_igbt_test_1 - Rth_c_igbt
        Rth_j_diode = (tests_1[idxs_1[1],7] - T_sink)/p_diode_test_1 - Rth_c_diode
        
        print(tests_1[idxs_1[1],3])
        print(Rth_j_igbt)
        print(Rth_j_diode)
        
        Cth_sink = tau_sink/Rth_sink/N_switch_sink
        
        data = {'a_i': self.coef_i[0],
        'b_i' : self.coef_i[1],
        'c_i' : self.coef_i[2],
        'd_i' : self.coef_i[3],
        'e_i' : self.coef_i[4],
        'a_d' : self.coef_d[0],
        'b_d' : self.coef_d[1],
        'c_d' : self.coef_d[2],
        'd_d' : self.coef_d[3],
        'e_d' : self.coef_d[4],
        "Rth_sink":[Rth_sink],
        "Rth_c_igbt":[Rth_c_igbt],
        "Rth_c_diode":[Rth_c_diode],
        "Rth_j_igbt":[Rth_j_igbt],
        "Rth_j_diode":[Rth_j_diode],
        "T_a":[T_a],
        "Cth_sink":[Cth_sink],
        "N_switch_sink":[N_switch_sink]}
        
        data_list = ['a_i','b_i','c_i','d_i','e_i','a_d','b_d','c_d','d_d','e_d']
        data_list += ["Rth_sink", "Rth_c_igbt", "Rth_c_diode", "Rth_j_igbt", "Rth_j_diode","T_a", "Cth_sink", "N_switch_sink"]
        string = ''
        for item in data_list:
            string += '"{:s}"'.format(item)
            string += ':'
            string += '{:3.4e}'.format(data[item][0])
            string += ', '
        
        print(string)
        
        string = ''
        for item in data_list:
            string += "('{:s}','float64')".format(item)
            string += ', '
        
        print(string)
        
            

@numba.jit (nopython=True, cache=True) # ,parallel=True, nogil=True)
def vsc_pf_eval(it,params_pf):
    ig = 0
    
    gfeed_bus_nodes = params_pf[ig].gfeed_bus_nodes
       
# %% power flow    
    N_v = params_pf[ig].N_nodes_v
    v_abcn = params_pf[ig].V_node[gfeed_bus_nodes[it]+N_v,:]    # todo: check that nodes are correct

    v_abc = v_abcn[0:3,:]

    L = params_pf[ig].gfeed_L[it]
    R = params_pf[ig].gfeed_R[it] 
    v_dc = params_pf[ig].gfeed_V_dc[it]  
    
    omega = 2*np.pi*50.0
    w=omega
    alpha = np.exp(2.0/3*np.pi*1j)
    A_0a = np.zeros((3,3), np.complex128)
    A_0a[0,0] = 1.0
    A_0a[0,1] = 1.0
    A_0a[0,2] = 1.0
    A_0a[1,0] = 1.0
    A_0a[1,1] = alpha**2
    A_0a[1,2] = alpha
    A_0a[2,0] = 1.0
    A_0a[2,1] = alpha
    A_0a[2,2] = alpha**2

    A_a0 = np.zeros((3,3), np.complex128)
    A_a0[0,0] = 1.0/3.0
    A_a0[0,1] = 1.0/3.0
    A_a0[0,2] = 1.0/3.0
    A_a0[1,0] = 1.0/3.0
    A_a0[1,1] = alpha/3.0
    A_a0[1,2] = alpha**2/3.0
    A_a0[2,0] = 1.0/3.0
    A_a0[2,1] = alpha**2/3.0
    A_a0[2,2] = alpha/3.0
    
    # Fortescue
    v_zpn = A_a0 @ v_abc 
    v_z = v_zpn[0,0]
    v_p = v_zpn[1,0]
    v_n = v_zpn[2,0]
    
    # PLL
    theta_pll = np.angle(v_p)
    
    # Park
    v_dq_p = v_p*np.exp(-1j*theta_pll)*np.sqrt(2)
    v_dq_n = v_n*np.exp( 1j*theta_pll)*np.sqrt(2)
    
    v_d_p = v_dq_p.imag
    v_q_p = v_dq_p.real
    v_d_n = v_dq_n.imag
    v_q_n = v_dq_n.real
    
    # References
    p_ref = params_pf[ig].gfeed_p_ref[it]
    q_ref = params_pf[ig].gfeed_q_ref[it]
    
    
    mode = int(params_pf[ig].gfeed_ctrl_type[it])
    
    i_d_p_ref = 0.0
    i_q_p_ref = 0.0
    i_d_n_ref = 0.0
    i_q_n_ref = 0.0
        
        
    if mode == 1: # i_pos
        i_d_p_ref = -(0.666666666666667*p_ref*v_d_p*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2) + 0.666666666666667*q_ref*v_q_p*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_q_p_ref = 0.666666666666667*(-p_ref*v_q_p*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2) + q_ref*v_d_p*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_d_n_ref = 0
        i_q_n_ref = 0
        
    if mode == 12: # 'q_cte'
        i_d_p_ref = 0.666666666666667*(p_ref*v_d_p*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2) + q_ref*v_q_p*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_q_p_ref = 0.666666666666667*(p_ref*v_q_p*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2) - q_ref*v_d_p*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_d_n_ref = 0.666666666666667*(p_ref*v_d_n*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2) - q_ref*v_q_n*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_q_n_ref = 0.666666666666667*(p_ref*v_q_n*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2) + q_ref*v_d_n*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)    
    
    if mode == 13: #'pq_cte': # Lipo
        i_d_p_ref = 0.666666666666667*(-p_ref*v_d_p + q_ref*v_q_p)/(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2)
        i_q_p_ref = -(0.666666666666667*p_ref*v_q_p + 0.666666666666667*q_ref*v_d_p)/(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2)
        i_d_n_ref = 0.666666666666667*(p_ref*v_d_n + q_ref*v_q_n)/(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2)
        i_q_n_ref = 0.666666666666667*(p_ref*v_q_n - q_ref*v_d_n)/(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2)
    
    if mode == 11: # 'pq_leon':
        #print('mode',mode)
        i_d_p_ref = -(0.666666666666667*p_ref*v_d_p*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2) + 0.666666666666667*q_ref*v_q_p*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_q_p_ref =   0.666666666666667*(-p_ref*v_q_p*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2) + q_ref*v_d_p*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_d_n_ref =   0.666666666666667*(p_ref*v_d_n*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2) - q_ref*v_q_n*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)
        i_q_n_ref =   0.666666666666667*(p_ref*v_q_n*(v_d_n**2 + v_d_p**2 + v_q_n**2 + v_q_p**2) + q_ref*v_d_n*(v_d_n**2 - v_d_p**2 + v_q_n**2 - v_q_p**2))/(v_d_n**4 + 2.0*v_d_n**2*v_q_n**2 - v_d_p**4 - 2.0*v_d_p**2*v_q_p**2 + v_q_n**4 - v_q_p**4)

    if mode == 20: # 'z_mode':
        I_p_ref = np.conj((p_ref+1j*q_ref)/v_p)/3/np.sqrt(3)
        Z_p = v_p/I_p_ref
        I_n_ref = np.conj((p_ref+1j*q_ref)/v_n)/3/np.sqrt(3)
        Z_n = v_n/I_n_ref
        i_d_p_ref = ((v_q_p + 1j*v_d_p)/Z_p).imag
        i_q_p_ref = ((v_q_p + 1j*v_d_p)/Z_p).real
        i_d_n_ref = ((v_q_n + 1j*v_d_n)/Z_n).imag
        i_q_n_ref = ((v_q_n + 1j*v_d_n)/Z_n).real
        
    # Control
    eta_d_p = 2.0/v_dc*(R*i_d_p_ref + L*w*i_q_p_ref + v_d_p)
    eta_q_p = 2.0/v_dc*(R*i_q_p_ref - L*w*i_d_p_ref + v_q_p)
    eta_d_n = 2.0/v_dc*(R*i_d_n_ref + L*w*i_q_n_ref + v_d_n)
    eta_q_n = 2.0/v_dc*(R*i_q_n_ref - L*w*i_d_n_ref + v_q_n)
    
    eta_dq_p = eta_q_p + 1j*eta_d_p
    e_dq_p = v_dc/2.0*eta_dq_p       # phase-neutral peak value
     
    eta_dq_n = eta_q_n + 1j*eta_d_n
    e_dq_n = v_dc/2.0*eta_dq_n       # phase-neutral peak value
    
    # Modulation
    e_p = e_dq_p *np.exp( 1j*theta_pll)/np.sqrt(2) # phase-neutral RMS value   
    e_n = e_dq_n *np.exp(-1j*theta_pll)/np.sqrt(2) # phase-neutral RMS value
    e_z = v_z
    #e_n = 0.0

    e_zpn = np.zeros((3,1),np.complex128)
    e_zpn[0,0] = e_z
    e_zpn[1,0] = e_p
    e_zpn[2,0] = e_n
        
    e_abc = A_0a @ e_zpn
    
    # Plant 
    Z_1 = R +1j *L*omega
    Z_2 = Z_1
    Z_0 = Z_1

    Z_012 = np.zeros((3,3),np.complex128)  
    Z_012[0,0] = Z_0
    Z_012[1,1] = Z_1
    Z_012[2,2] = Z_2
        
    Z_abc = A_0a @ Z_012 @ A_a0
    
    Y_abc = np.linalg.inv(Z_abc)
    i_abc = Y_abc @ (e_abc-v_abc)
    
    params_pf[ig].gfeed_currents[it,0:3] = i_abc[:,0]
##    print('p_ref',p_ref)
##    print('q_ref',q_ref)    
##    print('i_d_p_ref',i_d_p_ref)
##    print('i_q_p_ref',i_q_p_ref)
##    print('i_d_n_ref',i_d_n_ref)
##    print('i_q_n_ref',i_q_n_ref)
##    print(abs(params_pf[ig].gfeed_currents[it,0:3]))
#    
##    return i_abc
    
    
#@numba.jit(nopython=True,parallel=True, nogil=True)
def bess_vsc_eval(t,mode,params,params_pf,params_simu):
    '''
    
    Parameters
    ----------

    source_mode: int
        0: grid_feeder, 1:grid_former
    mode: int
        0:power flow, 1: ini, 2:der, 3:discrete, 4:out
    ctrl_mode: int
        1:  grid former, fix_v + secondary
        3:  grid former, p-v, q-ang
        4:  grid former, ruben
        10: grid feeder, fix current
        11: grid feeder, constant power
        12: grid feeder, power profile
        
        
    '''

    N = len(params) # total number of bess_vsc_feeder
    for it in range(N):
        source_mode = params[it].source_mode  
        ix_0 = params[it].ix_0
        nodes = params[it].nodes
        N_conductors = params[it].N_conductors
        v_abcn = params_pf[0].V_node[nodes,:]
        v_abc = v_abcn[0:3,:]
        i_abcn = params[it].i_abcn
        if source_mode==1:
            i_abcn = params_pf[0].I_node[nodes,:]
        gfeed_idx = params[it].gfeed_idx 
        gform_idx = params[it].gform_idx        
        
        ctrl_mode = params[it].ctrl_mode 

            
   

            
            

            
            
            
# %% initialization    
        if mode == 1:  # ini
            i_abcn_0 = np.zeros((4,1), dtype=np.complex128)
            
            if source_mode==0: 
            
                S_ref = params_pf[0].gfeed_powers[gfeed_idx]            
                I_ref = params_pf[0].gfeed_currents[gfeed_idx]*np.exp(1j*np.angle(v_abcn[:,0]))
     
                I_abc_ref =  I_ref + np.conjugate(S_ref/v_abcn[:,0])
                I_n = -np.sum(I_abc_ref)
            
                i_abcn_0[0:4,0] = I_abc_ref
                i_abcn_0[3,:] = I_n
   
                v_abcn_0 = np.copy(v_abcn)
  
                S_0 = v_abcn_0*np.conj(i_abcn_0)
    
                params[it].v_abcn_0[:] = v_abcn_0
                params[it].i_abcn_0[:] = i_abcn_0     
                params[it].i_abcn[:] = np.copy(i_abcn_0)
                params[it].S_0[:] = S_0
                params[it].S_ref[:] = S_0
            
            params_simu[0].x[ix_0+0,0] = params[it].soc_0

#            # thermal model 
#            if params[it].thermal_model>0:
#                params[it].x[3:4,0] = params[it].T_a
#                params[it].T_sink =  params[it].x[3,0]  
#                params[it].T_j_igbt_abcn[:]  = params[it].T_sink
    
 
# %% derivatives    
        if mode == 2:  # der
            S_ctrl = params[it].S_ref
    
            S_abcn = v_abcn*np.conj(i_abcn)
            P_abcn = S_abcn.real + S_ctrl.real
            if N_conductors == 3:
                p_ac_total = np.sum(P_abcn[0:3,:])  
            if N_conductors == 4:
                p_ac_total = np.sum(P_abcn[0:3,:]) 
            
            
            params_simu[0].f[ix_0+0,0] =  -p_ac_total*params[it].switch

            #bess_control_eval(t,it,ctrl_mode,1,params)
            
            
# %% out
        if mode == 4: # out

            if source_mode==0: 
                S_ctrl = params[it].S_ref
                ix_0 = params[it].ix_0
                
    #            bess_control_eval(t,it,ctrl_mode,3,params)
                
                params_pf[0].gfeed_powers[gfeed_idx,:]   = params[it].i_abcn_0[:,0]*0.0
                params_pf[0].gfeed_currents[gfeed_idx,:] = params[it].i_abcn_0[:,0]*np.exp(-1j*np.angle(v_abcn))[:,0]*0            
                
                params[it].soc = params_simu[0].x[ix_0+0,0]
                
                switch = 1.0
                if params[it].soc < params[it].soc_max*0.05:
                    switch = 0.0
                if params[it].soc > params[it].soc_max:
                    switch = 0.0
                    
                params[it].i_abcn[:] = np.copy(params[it].i_abcn_0)*switch
                params_pf[0].gfeed_i_abcn[gfeed_idx,:] = params[it].i_abcn[:,0]
                params_pf[0].gfeed_powers[gfeed_idx,0:3] = S_ctrl[0:3,0]*switch
                
                params[it].switch = switch



@numba.jit(nopython=True,cache=True, nogil=True)
def bess_control_eval(t,it,ctrl_mode,mode,params):
    
    if ctrl_mode == 12:
        bess_pq_profile(t,it,ctrl_mode,mode,params)
    
@numba.jit(nopython=True,cache=True)
def bess_pq_profile(t,it,ctrl_mode,mode,params):
    s_shapes = params[it]['s_shapes']
    s_npoints = params[it]['s_npoints']
    s_times = params[it]['s_times']
    time_idx = np.argmax(s_times>t)
    if time_idx>0:
        params[it].S_ref[:,0] = s_shapes[time_idx]*np.array([1.0,1.0,1.0,0.0])

            
    
    
    
    
#@numba.jit(nopython=True,parallel=True, nogil=True)
def sm_ord4_eval(t,mode,params,params_pf,params_simu):
    '''
    
    Parameters
    ----------


    mode: int
        0: ini, 1:der, 2:out
 
        
    '''

    alpha = np.exp(2.0/3*np.pi*1j)
    A_0a =  np.array([[1, 1, 1],
                      [1, alpha**2, alpha],
                      [1, alpha, alpha**2]])

    A_a0 = 1/3* np.array([[1, 1, 1],
                          [1, alpha, alpha**2],
                          [1, alpha**2, alpha]])
            
    struct = params         
    N = len(params) # total number of bess_vsc_feeder
    for it in numba.prange(N):
        ix_0 = params[it].ix_0
        nodes = params[it].bus_nodes
        N_conductors = params[it].N_conductors
        v_abcn = params_pf[0].V_node[nodes,:]
        i_abcn = params[it].i_abcn
        g_idx = params[it].g_idx    
        ctrl_mode = params[it].ctrl_mode    
    
        R_s = struct[it]['R_s']
        X_d,X_q = struct[it]['X_d'],struct[it]['X_q']
        X1d,X1q,X_l = struct[it]['X1d'],struct[it]['X1q'],struct[it]['X_l']
 
# %% power flow    
        if mode == 0:  # pf
            i_abcn_0 = np.zeros((4,1), dtype=np.complex128)

            S_ref = params_pf[0].gfeed_powers[g_idx,0:3]            
            I_ref = params_pf[0].gfeed_currents[g_idx]*np.exp(1j*np.angle(v_abcn[:,0]))

            I_abc_0 =   np.conjugate(S_ref[:,0:3]/v_abcn[0:3,0]).T # + I_ref 
            I_n = -np.sum(I_abc_0)       
            V_abc_0 = v_abcn[0:3,:] 
            
            I_012 = A_a0 @ I_abc_0
            V_012 = A_a0 @ V_abc_0
            print(I_012.shape)
            I_zero = I_012[0,0] 
            V_zero = V_012[0,0]             
            I_pos = I_012[1,0] 
            V_pos = V_012[1,0] 
            I_neg = I_012[2,0] 
            V_neg = V_012[2,0] 
            
            # positive sequence initialization
            E = V_pos + (R_s + 1j*(X_q-X_l))*I_pos
            delta = np.angle(E)
            
            v_dq = V_pos*np.exp(-1j*(delta-np.pi/2)) 
            i_dq = I_pos*np.exp(-1j*(delta-np.pi/2))
            
            v_d,v_q = v_dq.real,v_dq.imag
            i_d,i_q = i_dq.real,i_dq.imag
            
            e1q = v_q + R_s*i_q + (X1d-X_l)*i_d
            e1d = v_d + R_s*i_d - (X1q-X_l)*i_q

    
            delta_0 = delta
            omega_0 = 1.0
            e1q_0 = e1q
            e1d_0 = e1d
            
            e_fd_0 = e1q + (X_d - X1d)*i_d
            p_e = (v_q + R_s * i_q) * i_q + (v_d + R_s*i_d) * i_d
            p_m_0 = p_e
            
            params_simu[0].x[ix_0+0,0] = delta_0
            params_simu[0].x[ix_0+1,0] = omega_0            
            params_simu[0].x[ix_0+2,0] = e1q_0
            params_simu[0].x[ix_0+3,0] = e1d_0
            
            params[it].p_m  = p_m_0
            params[it].e_fd = e_fd_0



# %% initialization    
        if mode == 1:  # ini
            i_abcn_0 = np.zeros((4,1), dtype=np.complex128)

            S_ref = params_pf[0].gfeed_powers[g_idx,0:3]            
            I_ref = params_pf[0].gfeed_currents[g_idx]*np.exp(1j*np.angle(v_abcn[:,0]))

            I_abc_0 =   np.conjugate(S_ref[:,0:3]/v_abcn[0:3,0]).T # + I_ref 
            I_n = -np.sum(I_abc_0)       
            V_abc_0 = v_abcn[0:3,:] 
            
            I_012 = A_a0 @ I_abc_0
            V_012 = A_a0 @ V_abc_0
            print(I_012.shape)
            I_zero = I_012[0,0] 
            V_zero = V_012[0,0]             
            I_pos = I_012[1,0] 
            V_pos = V_012[1,0] 
            I_neg = I_012[2,0] 
            V_neg = V_012[2,0] 
            
            # positive sequence initialization
            E = V_pos + (R_s + 1j*(X_q-X_l))*I_pos
            delta = np.angle(E)
            
            v_dq = V_pos*np.exp(-1j*(delta-np.pi/2)) 
            i_dq = I_pos*np.exp(-1j*(delta-np.pi/2))
            
            v_d,v_q = v_dq.real,v_dq.imag
            i_d,i_q = i_dq.real,i_dq.imag
            
            e1q = v_q + R_s*i_q + (X1d-X_l)*i_d
            e1d = v_d + R_s*i_d - (X1q-X_l)*i_q

    
            delta_0 = delta
            omega_0 = 1.0
            e1q_0 = e1q
            e1d_0 = e1d
            
            e_fd_0 = e1q + (X_d - X1d)*i_d
            p_e = (v_q + R_s * i_q) * i_q + (v_d + R_s*i_d) * i_d
            p_m_0 = p_e
            
            params_simu[0].x[ix_0+0,0] = delta_0
            params_simu[0].x[ix_0+1,0] = omega_0            
            params_simu[0].x[ix_0+2,0] = e1q_0
            params_simu[0].x[ix_0+3,0] = e1d_0
            
            params[it].p_m  = p_m_0
            params[it].e_fd = e_fd_0

    
 
# %% derivatives    
        if mode == 2:  # der
            pass
            
            
# %% out
        if mode == 4: # out
            pass
        

def thermal_vsc(params):
    '''
    Compute thermal losses for an IGBT based VSC
    
    Inputs
    ------
    
    numpy structure with at least the following fields:
        
        Rth_sink: float
                  Thermal resistance from sink to enviroment
        Rth_c_igbt: float
                    Thermal resistance from IGBT case to sink
        Rth_c_diode: float
                     Thermal resistance drom diode case to sink
        Rth_c_igbt: float
                    Thermal resistance  from IGBT jucture to case
        Rth_c_diode: float
                     Thermal resistance from DIODE juncture to case        
        a_i, b_i, c_i, d_i, e_i: floats
                                 IGBT loss power function coeficients
        a_d, b_d, c_d, d_d, e_d: floats
                                 DIODE loss power function coeficients                                 
    
    '''
    
    
    I_abc = params[it].i_abcn[0:3,:] # phase currents (without neutral)                    
    S = V_abc*np.conj(I_abc) # phase complex power
    params[it].S[:] = S[:]   
        
    I_abc_m = np.abs(I_abc)
    
    a_i = params[it].a_i
    b_i = params[it].b_i
    c_i = params[it].c_i
    d_i = params[it].d_i
    e_i = params[it].e_i
    
    a_d = params[it].a_d
    b_d = params[it].b_d
    c_d = params[it].c_d
    d_d = params[it].d_d
    e_d = params[it].e_d

    Rth_sink  = params[it].Rth_sink
    Rth_c_igbt = params[it].Rth_c_igbt
    Rth_c_diode  = params[it].Rth_c_diode
    Rth_j_igbt = params[it].Rth_j_igbt
    Rth_j_diode = params[it].Rth_j_diode
    T_a = params[it].T_a
    Cth_sink  = params[it].Cth_sink
                  
    I_abcn = params[it].i_abcn
    V_abcn = params[it].v_abcn
    m = (np.abs(V_abcn)*np.sqrt(2.0)/params[it].V_dc*2.0)[:]
    #m = np.abs(V_abcn)

    
    fp = np.cos(np.angle(I_abcn) - np.angle(V_abcn))[:]
    I_abcn_m = np.abs(params[it].i_abcn)[:]
    
    
#            print(fp[0,0])
#            print(fp[1,0])
    params[it].p_igbt_abcn[:]  = (a_i + (b_i + c_i*m*fp)*I_abcn_m + (d_i + e_i*m*fp)*I_abcn_m**2)
    params[it].p_diode_abcn[:] = (a_d + (b_d + c_d*m*fp)*I_abcn_m + (d_d + e_d*m*fp)*I_abcn_m**2)

#            print('I_abcn_m',I_abcn_m [0,0])
#            print(params[it].p_igbt_abcn[:] [0,0])
#            print(params[it].p_diode_abcn[:] [0,0])            
    
    N_switch_sink = params[it].N_switch_sink
    p_igbt_total  = 2*np.sum(params[it].p_igbt_abcn)
    p_diode_total = 2*np.sum(params[it].p_diode_abcn)            
                        
    params[it].T_j_igbt_abcn[:]   = params[it].T_sink + (Rth_c_igbt + Rth_j_igbt )*(params[it].p_igbt_abcn[:])
#            params[it].T_j_diode_abcn  = params[it].T_sink + (Rth_c_diode+ Rth_j_diode)*(params[it].p_diode_abcn)
#            print(params[it].T_j_igbt_abcn[:] )
    
    T_sink =  params[it].x[3:4,0]
    #print(T_sink[0])
    params[it].f[3:4,0] = 1.0/Cth_sink*(T_a + Rth_sink/N_switch_sink*(p_igbt_total + p_diode_total)-T_sink) # angle from frequency           
    params[it].m[:] = m 
    
    params[it].T_sink =  params[it].x[3,0]  
    
    
