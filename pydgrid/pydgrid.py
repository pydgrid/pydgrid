# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 13:04:45 2017

@author: jmmauricio
"""

import numpy as np 
import os
import numba
import string
numba.caching.config.CACHE_DIR = '/home/jmmauricio/Documents'
import multiprocessing

import json
import time
from pydgrid.pf import pf_eval,set_load_factor,time_serie
import time
from scipy import sparse
from scipy.sparse import linalg as sla


class grid(object):
    '''   
    P+N : 1
    3P  : 2
    3P+N: 3
    '''
    
    
    def __init__(self):
        
        self.Freq = 50.0
        self.s_radio_scale = 0.01
        self.s_radio_max = 20
        self.s_radio_min = 1
        self.pf_solver = 1
        
        self.line_codes_lib = {
              'OH1':{'Z': [[0.540 + 0.777j, 0.049 + 0.505j, 0.049 + 0.462j, 0.049 + 0.436j],
                         [0.049 + 0.505j, 0.540 + 0.777j, 0.049 + 0.505j, 0.049 + 0.462j],
                         [0.049 + 0.462j, 0.049 + 0.505j, 0.540 + 0.777j, 0.049 + 0.505j],
                         [0.049 + 0.436j, 0.049 + 0.462j, 0.049 + 0.505j, 0.540 + 0.777j]]},
              'OH2':{'Z': [[1.369 + 0.812j, 0.049 + 0.505j, 0.049 + 0.462j, 0.049 + 0.436j], 
                         [0.049 + 0.505j, 1.369 + 0.812j, 0.049 + 0.505j, 0.049 + 0.462j], 
                         [0.049 + 0.462j, 0.049 + 0.505j, 1.369 + 0.812j, 0.049 + 0.505j], 
                         [0.049 + 0.436j, 0.049 + 0.462j, 0.049 + 0.505j, 1.369 + 0.812j]]},
              'OH3':{'Z': [[2.065 + 0.825j, 0.049 + 0.505j, 0.049 + 0.462j, 0.049 + 0.436j], 
                         [0.049 + 0.505j, 2.065 + 0.825j, 0.049 + 0.505j, 0.049 + 0.462j], 
                         [0.049 + 0.462j, 0.049 + 0.505j, 2.065 + 0.825j, 0.049 + 0.505j], 
                         [0.049 + 0.436j, 0.049 + 0.462j, 0.049 + 0.505j, 2.065 + 0.825j]]}, 
              'UG1':{'Z': [[0.211 + 0.747j, 0.049 + 0.673j, 0.049 + 0.651j, 0.049 + 0.673j], 
                         [0.049 + 0.673j, 0.211 + 0.747j, 0.049 + 0.673j, 0.049 + 0.651j], 
                         [0.049 + 0.651j, 0.049 + 0.673j, 0.211 + 0.747j, 0.049 + 0.673j], 
                         [0.049 + 0.673j, 0.049 + 0.651j, 0.049 + 0.673j, 0.211 + 0.747j]]},
         'UG1_luna':{'Z': [[0.211 + 0.747j, 0.049 +0.6657j, 0.049 +0.6657j, 0.049 +0.6657j], 
                         [0.049 +0.6657j, 0.211 + 0.747j, 0.049 +0.6657j, 0.049 +0.6657j], 
                         [0.049 +0.6657j, 0.049 +0.6657j, 0.211 + 0.747j, 0.049 +0.6657j], 
                         [0.049 +0.6657j, 0.049 +0.6657j, 0.049 +0.6657j, 0.211 + 0.747j]]},
              'UG2':{'Z': [[0.314 + 0.762j, 0.049 + 0.687j,0.049 + 0.665j, 0.049 + 0.687j], 
                         [0.049 + 0.687j, 0.314 + 0.762j, 0.049 + 0.687j, 0.049 + 0.665j], 
                         [0.049 + 0.665j, 0.049 + 0.687j, 0.314 + 0.762j, 0.049 + 0.687j], 
                         [0.049 + 0.687j, 0.049 + 0.665j, 0.049 + 0.687j, 0.314 + 0.762j]]}, 
              'UG3':{'Z': [[0.871 + 0.797j, 0.049 + 0.719j, 0.049 + 0.697j, 0.049 + 0.719j], 
                         [0.049 + 0.719j, 0.871 + 0.797j, 0.049 + 0.719j, 0.049 + 0.697j], 
                         [0.049 + 0.697j, 0.049 + 0.719j, 0.871 + 0.797j, 0.049 + 0.719j], 
                         [0.049 + 0.719j, 0.049 + 0.697j, 0.049 + 0.719j, 0.871 + 0.797j]]},
              'EQU':{'Z': [[0.871 + 0.797j, 0.049 + 0.719j, 0.049 + 0.719j, 0.049 + 0.719j], 
                         [0.049 + 0.719j, 0.871 + 0.797j, 0.049 + 0.719j, 0.049 + 0.719j], 
                         [0.049 + 0.719j, 0.049 + 0.719j, 0.871 + 0.797j, 0.049 + 0.719j], 
                         [0.049 + 0.719j, 0.049 + 0.719j, 0.049 + 0.719j, 0.871 + 0.797j]]},
              'TR1':{'Z': [[0.0032+0.0128j, 0.000j, 0.000j, 0.000j], 
                         [0.000j, 0.0032+0.0128j, 0.000j, 0.000j], 
                         [0.000j, 0.000j, 0.0032+0.0128j, 0.000j],  
                         [0.000j, 0.000j, 0.000j, 0.0032+0.0128j]]},
              'PN1':{'Z': [[0.314 + 0.762j, 0.049 + 0.687j], 
                         [0.049 + 0.687j, 0.314 + 0.762j]]},
              'NN1':{'Z': [[0.871 + 0.797j, 0.049 + 0.719j, 0.049 + 0.719j], 
                         [0.049 + 0.719j, 0.871 + 0.797j, 0.049 + 0.719j], 
                         [0.049 + 0.719j, 0.049 + 0.719j, 0.871 + 0.797j]]},
              'UG1w3':{'Z': [
                          [ 0.28700247+0.16535143j,  0.12115403+0.11008501j,0.12500247+0.06935143j],
                          [ 0.12115403+0.11008501j,  0.27947509+0.20221853j,0.12115403+0.11008501j],
                          [ 0.12500247+0.06935143j,  0.12115403+0.11008501j,0.28700247+0.16535143j]]},
              'UG3w3':{'Z': [
                          [ 1.15225232+0.45874501j, 0.32098424+0.39046333j, 0.33025232+0.35874501j],
                          [ 0.32098424+0.39046333j, 1.13401861+0.4779049j, 0.32098424+0.39046333j],
                          [ 0.33025232+0.35874501j,  0.32098424+0.39046333j,1.15225232+0.45874501j]]}                       
              }



    def read(self,data_input): 
        debug = True
        
        alpha = np.exp(2.0/3*np.pi*1j)
        A_0a =  np.array([[1, 1, 1],
                          [1, alpha**2, alpha],
                          [1, alpha, alpha**2]])
    
        A_a0 = 1/3* np.array([[1, 1, 1],
                              [1, alpha, alpha**2],
                              [1, alpha**2, alpha]])
                  
                  
        
        if type(data_input) == str:
            json_file = data_input
            self.json_file = json_file
            self.json_data = open(json_file).read().replace("'",'"')
            data = json.loads(self.json_data)
        elif type(data_input) == dict:
            data = data_input
            self.data = data
        
        
        flog = open('log.txt','w')
        
        # power flow options
        self.max_iter = 20
        
        # run options
        self.N_steps = 1000
        self.Dt = 10.0e-3
        self.Dt_out = 0.01
        
        if 'transformers' in data:
            transformers = data['transformers']
            self.transformers = transformers
        else:
            transformers = []
            self.transformers = transformers
        if debug==True: flog.write('{:d} transformer to read \n'.format(len(transformers)))
            
        if 'line_codes' in data:
            line_codes_data = data['line_codes']
            self.line_codes = line_codes_data
            
        if 'loads' in data:
            loads = data['loads']
            self.loads = loads
        else:
            loads = []                        

        if 'grid_feeders' in data:
            grid_feeders = data['grid_feeders']
            self.grid_feeders = grid_feeders
        else:
            grid_feeders = []   

        if 'lines' in data:
            lines = data['lines']
            self.lines = lines
        else:
            lines = []   
            
        if 'grid_formers' in data:
            grid_formers = data['grid_formers']
            self.grid_formers = grid_formers
        else:
            grid_formers = []          
        
        
        buses = data['buses']

        if 'shunts' in data:
            shunts = data['shunts']
            self.shunts = shunts
        else:
            shunts = []
            
        if 'groundings' in data:
            groundings = data['groundings']
            self.groundings = groundings
        else:
            groundings = []
            
        self.lines = lines
        self.buses = buses
        
        N_nodes_default = 4
        nodes = []
        A_n_cols = 0
        it_col = 0
        grid_formers_nodes = []

        node_sorter = []
        N_v_known = 0
        N_nz_nodes = 0  # number on non zero current nodes
        
        
        ## Grid formers (known voltages)
        V_known_list = []
        N_gformers = 0
        gformer_nodes_list = []
        gformer_bus_nodes_list = []
        gformer_voltages_list = []
        gformer_id_list = []
        gformer_v_abcn_list = []
        gformer_i_abcn_list = []
        
        for grid_former in grid_formers:
            grid_former_nodes = []
            gformer_nodes = np.zeros((4,), dtype=np.int32)
            gformer_bus_nodes = np.zeros((4,), dtype=np.int32) # every grid former considers 4 nodes per bus here
            gformer_voltages = np.zeros((4,), dtype=np.complex128) # every grid former considers 4 nodes per bus here
            gformer_v_abcn = np.zeros((4,), dtype=np.complex128) # every grid former considers 4 nodes per bus here
            gformer_i_abcn = np.zeros((4,), dtype=np.complex128) # every grid former considers 4 nodes per bus here
            if not 'bus_nodes' in grid_former:   # if nodes are not declared, default nodes are created
                grid_former.update({'bus_nodes': list(range(1,N_nodes_default+1))})
            inode = 0
            for item in  grid_former['bus_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node = '{:s}.{:s}'.format(grid_former['bus'], str(item))
                if not node in nodes: 
                    nodes +=[node]
                grid_former_nodes += [N_v_known]
                gformer_nodes[inode] = N_v_known
                N_v_known += 1
                gformer_bus_nodes[inode] = item
                inode += 1
            inode = 0
            for volt,ang in  zip(grid_former['kV'],grid_former['deg']): # known voltages list is created 
                v = 1000.0*volt*np.exp(1j*np.deg2rad(ang))
                V_known_list += [v]
                gformer_voltages[inode] = v
                inode += 1
            grid_formers_nodes += [grid_former_nodes]    # global nodes for each vsources update  
            N_gformers += 1
            if "id" in grid_former:       
                gformer_id_list += [grid_former["id"]]
            else:
                gformer_id_list += ['{:s}.{:s}'.format('gformer',grid_former['bus'])]
            gformer_nodes_list += [gformer_nodes]
            gformer_bus_nodes_list += [gformer_bus_nodes]
            gformer_voltages_list += [gformer_voltages]
            gformer_v_abcn_list += [gformer_v_abcn]
            gformer_i_abcn_list += [gformer_i_abcn]
        V_known = np.array(V_known_list).reshape(len(V_known_list),1) # known voltages list numpy array
        self.grid_formers_nodes = grid_formers_nodes
        self.N_gformers = N_gformers     
        self.gformer_nodes = np.array(gformer_nodes_list)
        self.gformer_bus_nodes = np.array(gformer_bus_nodes_list)
        self.gformer_voltages = np.array(gformer_voltages_list)
        self.gformer_i_abcn    = np.array(gformer_i_abcn_list)
        self.gformer_v_abcn    = np.array(gformer_v_abcn_list)
        self.gformer_id    = gformer_id_list


                  
                  
        N_nz_nodes += N_v_known
        
        ## Known currents
        S_known_list = []
        pq_3pn_int_list = []
        pq_3pn_list = []
        pq_3p_int_list = []
        pq_3p_list = []
        pq_1pn_int_list = []
        pq_1pn_list = []
        pq_1p_int_list = []
        pq_1p_list = []
        it_node_i = 0
        
        ### Loads
        for load in loads:
            if not 'bus_nodes' in load:   # if nodes are not declared, default nodes are created
                if load['type']=='3P':
                    load.update({'bus_nodes': list(range(1,3+1))})
                if load['type']=='3P+N':
                    load.update({'bus_nodes': list(range(1,N_nodes_default+1))})
            for item in  load['bus_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node = '{:s}.{:s}'.format(load['bus'], str(item))
                if not node in nodes: nodes +=[node] 
                
            if load['type'] == '3P+N':
                pq_3pn_int_list += [list(it_node_i + np.array([0,1,2,3]))]
                it_node_i += 4
                if 'kVA' in load:
                    if type(load['kVA']) == float:
                        S = -1000.0*load['kVA']*np.exp(1j*np.arccos(load['pf'])*np.sign(load['pf']))
                        pq_3pn_list += [[S/3,S/3,S/3]]
                    if type(load['kVA']) == list:
                        pq = []
                        for s,fp in zip(load['kVA'],load['pf']):                            
                            pq += [-1000.0*s*np.exp(1j*np.arccos(fp)*np.sign(fp))]
                        pq_3pn_list += [pq]
                                               
            if load['type'] == '3P':
                pq_3p_int_list += [list(it_node_i + np.array([0,1,2]))]
                it_node_i += 3
                if 'kVA' in load:
                    S_va = -1000.0*load['kVA']
                    phi = np.arccos(load['pf'])
                    if type(load['kVA']) == float:
                        pq_3p_list += [[S_va*np.exp(1j*phi*np.sign(load['pf']))]]

            if load['type'] == '1P+N':
                node_j = '{:s}.{:s}'.format(load['bus'],str(load['bus_nodes'][0]))
                if not node_j in nodes: nodes +=[node_j]
                node_k = '{:s}.{:s}'.format(load['bus'],str(load['bus_nodes'][1]))
                if not node_k in nodes: nodes +=[node_k]
                pq_1pn_int_list += [np.array([nodes.index(node_j),nodes.index(node_k)])-N_v_known]
                it_node_i += 2
                if 'kVA' in load:
                    S_va = -1000.0*load['kVA']
                    phi = np.arccos(load['pf'])
                    pq_1pn_list += [[S_va*np.exp(1j*phi*np.sign(load['pf']))]]
                if 'kW' in load:
                    S_va = -1000.0*load['kW']/load['pf']
                    phi = np.arccos(load['pf'])
                    pq_1pn_list += [[S_va*np.exp(1j*phi*np.sign(load['pf']))]]
        
            if load['type'] == '1P':
                pq_1p_int_list += [[it_node_i ]]
                it_node_i += 1
                if 'kVA' in load:
                    S_va = -1000.0*load['kVA']
                    phi = np.arccos(load['pf'])
                    pq_1p_list += [[S_va*np.exp(1j*phi*np.sign(load['pf']))]]
                if 'kW' in load:
                    S_va = -1000.0*load['kW']/load['pf']
                    phi = np.arccos(load['pf'])
                    pq_1p_list += [[S_va*np.exp(1j*phi*np.sign(load['pf']))]]

        
        N_pq_3p = len(pq_3p_list)
        N_pq_3pn = len(pq_3pn_list)
        N_pq_1p = len(pq_1p_list)
        N_pq_1pn = len(pq_1pn_list)
        N_nz_nodes += it_node_i                               
#            for kVA,fp in  zip(load['kVA'],load['pf']): # known complex power list 
#                S_known_list += [1000.0*kVA*np.exp(1j*np.arccos(fp)*np.sign(fp))]
        pq_3pn_int = np.array(pq_3pn_int_list) # known complex power list to numpy array
        pq_3pn = np.array(pq_3pn_list) # known complex power list to numpy array
        pq_3p_int = np.array(pq_3p_int_list) # known complex power list to numpy array
        pq_3p = np.array(pq_3p_list) # known complex power list to numpy array
        pq_1pn_int = np.array(pq_1pn_int_list) # known complex power list to numpy array
        pq_1pn = np.array(pq_1pn_list) # known complex power list to numpy array
        pq_1p_int = np.array(pq_1p_int_list) # known complex power list to numpy array
        pq_1p = np.array(pq_1p_list) # known complex power list to numpy array


        ### Grid feeders
        N_gfeeds = 0 
        gfeed_nodes_list = []
        gfeed_bus_nodes_list = []
        gfeed_currents_list = []
        gfeed_powers_list = []
        gfeed_id_list = []
        gfeed_i_abcn_list = []
        for grid_feeder in grid_feeders:
            N_gfeeds += 1   
            gfeed_nodes = np.zeros((4,), dtype=np.int32) # every grid feeder considers 4 nodes per bus here
            gfeed_bus_nodes = np.zeros((4,), dtype=np.int32) # every grid feeder considers 4 nodes per bus here
            gfeed_currents = np.zeros((4,), dtype=np.complex128) # every grid feeder considers 4 nodes per bus here
            gfeed_powers = np.zeros((4,), dtype=np.complex128) # every grid feeder considers 4 nodes per bus here
            gfeed_i_abcn = np.zeros((4,), dtype=np.complex128) # every grid feeder considers 4 nodes per bus here

            gf_node_it = 0
            for node in grid_feeder['bus_nodes']:              
                node_str = '{:s}.{:s}'.format(grid_feeder['bus'],str(node))
                if not node_str in nodes: nodes +=[node_str]
                gfeed_bus_nodes[gf_node_it] = nodes.index(node_str)
                gf_node_it += 1
                it_node_i += 1
            if 'kW' in grid_feeder:
                gf_it = 0
                if type(grid_feeder['kW']) == float:
                    for i in range(3):
                        kW = grid_feeder['kW']
                        kvar = grid_feeder['kvar']
                        gfeed_powers[gf_it] = 1000.0*(kW+1j*kvar)/3
                        gf_it += 1
                else:                     
        
                    for kW,kvar in zip(grid_feeder['kW'],grid_feeder['kvar']):              
                        gfeed_powers[gf_it] = 1000.0*(kW+1j*kvar)
                        gf_it += 1
            if 'kA' in grid_feeder:
                gf_it = 0
                for kA,phi_deg in zip(grid_feeder['kA'],grid_feeder['phi_deg']):              
                    gfeed_currents[gf_it] = 1000.0*kA*np.exp(1j*np.deg2rad(phi_deg))
                    gf_it += 1                
            gfeed_bus_nodes_list += [gfeed_bus_nodes]
            gfeed_currents_list += [gfeed_currents]
            gfeed_powers_list += [gfeed_powers]
            gfeed_i_abcn_list += [gfeed_i_abcn]
            if "id" in grid_feeder:       
                gfeed_id_list += [grid_feeder["id"]]
            else:
                gfeed_id_list += ['{:s}.{:s}'.format('gfeeder',grid_feeder['bus'])]
                
            
        self.N_gfeeds = N_gfeeds          
        self.gfeed_bus_nodes = np.array(gfeed_bus_nodes_list)-N_v_known
        self.gfeed_currents  = np.array(gfeed_currents_list)
        self.gfeed_powers    = np.array(gfeed_powers_list)
        self.gfeed_i_abcn    = np.array(gfeed_i_abcn_list)
        self.gfeed_id    = gfeed_id_list
        
        N_nz_nodes += it_node_i 


        ### Transformers to nodes
        t_0 = time.time()
        for trafo in transformers:
            flog.write('Transformer {:s} read  \n'.format(trafo['connection']))
            
            if  'conductors_1' in trafo:
                N_nodes_primary_default = trafo['conductors_1']
            if  'conductors_2' in trafo:
                N_nodes_secondary_default = trafo['conductors_2']   
            if  'conductors_j' in trafo:
                N_nodes_primary_default = trafo['conductors_j']
            if  'conductors_k' in trafo:
                N_nodes_secondary_default = trafo['conductors_k'] 
                
            N_trafo_nodes = N_nodes_primary_default+N_nodes_secondary_default
                
            A_n_cols += N_trafo_nodes
            if not 'bus_j_nodes' in trafo:   # if nodes are not declared, default nodes are created
                trafo.update({'bus_j_nodes': list(range(1,N_nodes_primary_default+1))})
            if not 'bus_k_nodes' in trafo:   # if nodes are not declared, default nodes are created
                trafo.update({'bus_k_nodes': list(range(1,N_nodes_secondary_default+1))})

            for item in  trafo['bus_j_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node_j = '{:s}.{:s}'.format(trafo['bus_j'], str(item))
                if not node_j in nodes: nodes +=[node_j]
            for item in  trafo['bus_k_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node_k = '{:s}.{:s}'.format(trafo['bus_k'], str(item))
                if not node_k in nodes: nodes +=[node_k]

        flog.write('Transformers read in: {:2.3f} s'.format(time.time()-t_0)) 
        t_0 = time.time()
                
        ### Lines to nodes
        for line in lines:
            ''' data type:
                * global_library: GLOBAL
                * user
                    - line without shunt, R1 and X1: ZR1X1
                    - line with shunt, R1, X1, C1: PIR1X1C1                    
                    - line without shunt, primitives: ZRX
                    - line with shunt, primitives: PIRXC   
            '''
            line['type'] = 'z'
            line_code = line['code']
            data_type='ZR1X1'
            if line_code in self.line_codes_lib: data_type='GLOBAL'
            if not  data_type=='GLOBAL':
                line_data = data['line_codes'][line_code]
                if 'X1' in line_data:  data_type='ZR1X1'
                if 'C_1_muF' in line_data:  data_type='PIR1X1C1'
                if 'R' in line_data:  data_type='ZRX'  
                if 'X' in line_data:  data_type='ZRX'      
                if 'B_mu' in line_data:  data_type='PIRXC'  
                if 'Rph' in line_data:  data_type='ZRphXph'
                if 'Rn' in line_data:  data_type='ZRphXphRnXn'  
                
                if data_type=='ZR1X1':
                    line['type'] = 'z'
                    Z_1 = line_data['R1'] + 1j*line_data['X1']
                    Z_2 = Z_1
                    if 'X0' in line_data:
                        Z_0 = line_data['R0'] + 1j*line_data['X0'] 
                    else:
                        Z_0 = 3*Z_1
                    Z_012 = np.array([[Z_0,0,0],[0,Z_1,0],[0,0,Z_2]])
                    Z = A_a0 @ Z_012 @ A_0a
                    self.line_codes_lib.update({line_code:{'Z':Z.tolist()}})
                    
                if data_type=='PIR1X1C1':
                    line['type'] = 'pi'
                    Z_1 = line_data['R1'] + 1j*line_data['X1']
                    Z_2 = Z_1
                    if 'X0' in line_data:
                        Z_0 = line_data['R0'] + 1j*line_data['X0'] 
                    else:
                        Z_0 = 3*Z_1
                    Z_012 = np.array([[Z_0,0,0],[0,Z_1,0],[0,0,Z_2]])
                    Z = A_a0 @ Z_012 @ A_0a
                    
                    B_1 = 2*np.pi*self.Freq*line_data['C_1_muF']*1e-6
                    B_2 = B_1
                    if 'C_0_muF' in line_data:
                        B_0 =  2*np.pi*self.Freq*line_data['C_0_muF']*1e-6
                    else:
                        B_0 =  3.0*B_1                  

                    Y_012 = np.array([[B_0,0,0],[0,B_1,0],[0,0,B_2]])
                    Y = A_a0 @ Y_012 @ A_0a
                    
                    self.line_codes_lib.update({line_code:{'Z':Z.tolist()}})
                    self.line_codes_lib[line_code].update({'Y':Y.tolist()})

                if data_type=='ZRX':
                    line['type'] = 'z'
                    R = np.array(data['line_codes'][line_code]['R'])
                    X = np.array(data['line_codes'][line_code]['X'])
                    Z = R + 1j*X
                    self.line_codes_lib.update({line_code:{'Z':Z.tolist()}})

                if data_type=='PIRXC':
                    line['type'] = 'pi'
                    R = np.array(data['line_codes'][line_code]['R'])
                    X = np.array(data['line_codes'][line_code]['X'])
                    Z = R + 1j*X
                    self.line_codes_lib.update({line_code:{'Z':Z.tolist()}})
                    
                    Y = 1j*np.array(data['line_codes'][line_code]['B_mu'])*1e-6
                    self.line_codes_lib[line_code].update({'Y':Y.tolist()})
                    

                if data_type == 'ZRphXphRnXn':
                    line['type'] = 'z'
                    R_ph = np.array(data['line_codes'][line_code]['Rph'])
                    X_ph = np.array(data['line_codes'][line_code]['Xph'])
                    R_n = np.array(data['line_codes'][line_code]['Rn'])
                    X_n = np.array(data['line_codes'][line_code]['Xn'])
                    Z = np.zeros((4,4),dtype=np.complex128)
                    Z[0,0] = R_ph+1j*X_ph
                    Z[1,1] = R_ph+1j*X_ph
                    Z[2,2] = R_ph+1j*X_ph
                    Z[3,3] = R_n+1j*X_n
                    self.line_codes_lib.update({line_code:{'Z':Z.tolist()}})

                      
                
            N_conductors = len(self.line_codes_lib[line['code']]['Z'])
            if line['type'] == 'z':
                A_n_cols += N_conductors
            if line['type'] == 'pi':
                A_n_cols += 3*N_conductors                
            
            if not 'bus_j_nodes' in line:   # if nodes are not declared, default nodes are created
                line.update({'bus_j_nodes': list(range(1,N_conductors+1))})
            if not 'bus_k_nodes' in line:   # if nodes are not declared, default nodes are created
                line.update({'bus_k_nodes': list(range(1,N_conductors+1))})

            for item in  line['bus_j_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node_j = '{:s}.{:s}'.format(line['bus_j'], str(item))
                if not node_j in nodes: nodes +=[node_j]
            for item in  line['bus_k_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node_k = '{:s}.{:s}'.format(line['bus_k'], str(item))
                if not node_k in nodes: nodes +=[node_k]

        N_nodes = len(nodes)

        ### Shunts (no new nodes, only aditionals columns in A matriz)
        for shunt in shunts:
            A_n_cols += 1        
        
        ### Groundings (no new nodes, only aditionals columns in A matriz)
        for grounding in groundings:
            A_n_cols += grounding['conductors']       
       
        ## Y primitive
        #A = np.zeros((N_nodes,A_n_cols)) # incidence matrix (dense)
        A_sp = sparse.lil_matrix((N_nodes, A_n_cols), dtype=np.float32) # incidence matrix (sparse)
        it_col = 0  # column in incidence matrix
        
        
        ### Transformers to Y primitive
        t_0 = time.time()
        Y_trafos_prims =  []
        for trafo in transformers:
            S_n = trafo['S_n_kVA']*1000.0
            if 'U_1_kV' in trafo:
                U_jn = trafo['U_1_kV']*1000.0
            if 'U_2_kV' in trafo:
                U_kn = trafo['U_2_kV']*1000.0
            if 'U_j_kV' in trafo:
                U_jn = trafo['U_j_kV']*1000.0
            if 'U_k_kV' in trafo:
                U_kn = trafo['U_k_kV']*1000.0
            Z_cc_pu = trafo['R_cc_pu'] +1j*trafo['X_cc_pu']
            connection = trafo['connection']
            
            Y_trafo_prim = trafo_yprim(S_n,U_jn,U_kn,Z_cc_pu,connection=connection)
            Y_trafos_prims +=  [Y_trafo_prim]

            for item in  trafo['bus_j_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node_j = '{:s}.{:s}'.format(trafo['bus_j'], str(item))
                row = nodes.index(node_j)
                col = it_col
                A_sp[row,col] = 1
                #A[row,col] = 1
                it_col +=1  
    
            for item in  trafo['bus_k_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                node_k = '{:s}.{:s}'.format(trafo['bus_k'], str(item))
                row = nodes.index(node_k)
                col = it_col
                A_sp[row,col] = 1
                #A[row,col] = 1
                it_col +=1 
 
        Y_trafos_primitive = diag_2d(Y_trafos_prims)        # dense
        Y_trafos_primitive = diag_2dsparse(Y_trafos_prims)  # sparse
        N_trafos_len = Y_trafos_primitive.shape[0]
        
        ### Lines to Y primitive       
        Z_line_list =  []
        for line in lines:
            if line['type'] == 'z':
                for item in  line['bus_j_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                    node_j = '{:s}.{:s}'.format(line['bus_j'], str(item))
                    row = nodes.index(node_j)
                    col = it_col
                    A_sp[row,col] = 1
                    #A[row,col] = 1
                    #it_col +=1   
        
                #for item in  line['bus_k_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                    node_k = '{:s}.{:s}'.format(line['bus_k'], str(item))
                    row = nodes.index(node_k)
                    col = it_col
                    A_sp[row,col] = -1
                    #A[row,col] = -1
                    it_col +=1   
                Z = line['m']*0.001*np.array(self.line_codes_lib[line['code']]['Z'])
                Z_line_list += [line['m']*0.001*np.array(self.line_codes_lib[line['code']]['Z'])]   # Line code to list of Z lines

            if line['type'] == 'pi':
                for item in  line['bus_j_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                    node_j = '{:s}.{:s}'.format(line['bus_j'], str(item))
                    row = nodes.index(node_j)
                    col = it_col
                    A_sp[row,col] = 1
                    #A[row,col] = 1
                    #it_col +=1   
        
                #for item in  line['bus_k_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                    node_k = '{:s}.{:s}'.format(line['bus_k'], str(item))
                    row = nodes.index(node_k)
                    col = it_col
                    A_sp[row,col] = -1
                    #A[row,col] = -1
                    it_col +=1   

                for item in  line['bus_j_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                    node_j = '{:s}.{:s}'.format(line['bus_j'], str(item))
                    row = nodes.index(node_j)
                    col = it_col
                    A_sp[row,col] = 1
                    #A[row,col] = 1
                    it_col +=1  

                for item in  line['bus_k_nodes']: # the list of nodes '[<bus>.<node>.<node>...]' is created 
                    node_k = '{:s}.{:s}'.format(line['bus_k'], str(item))
                    row = nodes.index(node_k)
                    col = it_col
                    A_sp[row,col] = 1
                    #A[row,col] = 1
                    it_col +=1  
                    
                    
                Z = line['m']*0.001*np.array(self.line_codes_lib[line['code']]['Z'])
                Y = np.array(self.line_codes_lib[line['code']]['Y'])
     
                Z_line_list += [Z,line['m']*0.001*np.linalg.inv(Y/2),line['m']*0.001*np.linalg.inv(Y/2)]   # Line code to list of Z lines
                
                
        ### shunt elements       
        for shunt in shunts:
            node_j_str = str(shunt['bus_nodes'][0])
            node_j = '{:s}.{:s}'.format(shunt['bus'], node_j_str)
            row_j = nodes.index(node_j)           
            col = it_col
            A_sp[row_j,col] = 1
            
            node_k_str = str(shunt['bus_nodes'][1])
            if not node_k_str == '0': # when connected to ground
                node_k = '{:s}.{:s}'.format(shunt['bus'], str(shunt['bus_nodes'][1]))
                row_k = nodes.index(node_k)            
                A_sp[row_k,col] = -1
                
            it_col +=1  
            Z_line_list += [np.array(shunt['R'] + 1j*shunt['X']).reshape((1,1))]   # Line code to list of Z lines
                
        ### grounding elements       
        for grounding in groundings:
            N_conductors = grounding['conductors']
            for it in [1,2,3]:
                node_j = '{:s}.{:s}'.format(grounding['bus'], str(it))
                row_j = nodes.index(node_j)           
                col = it_col
                A_sp[row_j,col] = 1
                it_col +=1
                
            Z_gnd = grounding['Z_gnd']
            Y_gnd = 1.0/Z_gnd 
            Z_m = 1/1000.0e3
            Y_full = -Y_gnd/3+Y_gnd
            Y_gnd1 = Y_gnd
            Y_gnd2 = Y_gnd*3
            Y_abcn = np.array([[  Y_full+Z_m,  Y_full,  Y_full, -Y_gnd1],
                               [  Y_full,  Y_full+Z_m,  Y_full, -Y_gnd1],
                               [  Y_full,  Y_full,  Y_full+Z_m, -Y_gnd1],
                               [ -Y_gnd1, -Y_gnd1, -Y_gnd1,  Y_gnd2]])
            Y_pp = Y_abcn[0:3,0:3]
            Y_pn = Y_abcn[0:3,3:4]
            Y_np = Y_abcn[3:4,0:3]
            Y_nn = Y_abcn[3:4,3:4]
            Y_abc = Y_pp - Y_pn @ np.linalg.inv(Y_nn) @ Y_np
            Z_abc = np.linalg.inv(Y_abc)
            Z_line_list += [Z_abc] 
 

                
        Y_lines_primitive = diag_2d_inv(Z_line_list)        # dense
        Y_lines_primitive = diag_2dsparse_inv(Z_line_list)  # sparse
        
        N_lines_len  = Y_lines_primitive.shape[0]
        
        ### Full  Y primitive         
        N_prim = N_trafos_len + N_lines_len
       
          
       
        #### sparse
        Y_primitive_sp = sparse.lil_matrix((N_prim,N_prim),dtype=np.complex128)
        
      
        Y_primitive_sp[N_trafos_len:N_prim,N_trafos_len:N_prim] = Y_lines_primitive     

        
        if N_trafos_len>0:
            Y_primitive_sp[0:N_trafos_len,0:N_trafos_len] = Y_trafos_primitive

        A_v = A_sp[0:N_v_known,:].toarray()
        N_nodes_i = N_nodes-N_v_known
        A_i = A_sp[N_v_known:(N_v_known+N_nodes_i),:] 

        self.A = A_sp
        self.nodes = nodes
        self.N_nodes = len(nodes)
        self.N_nodes_i = N_nodes_i
        self.N_nodes_v = self.N_nodes  - N_nodes_i
        self.A_v = A_v
        self.A_i = A_i

#        self.Y = A.T @ Y_primitive @ A (dense)
        self.Y = A_sp @ Y_primitive_sp @ A_sp.T        
        self.Y_primitive = Y_primitive_sp.toarray()
        self.Y_ii = A_i @ Y_primitive_sp @ A_i.T
        self.Y_iv = A_i @ Y_primitive_sp @ A_v.T
        self.Y_vv = A_v @ Y_primitive_sp @ A_v.T
        self.Y_vi = A_v @ Y_primitive_sp @ A_i.T

        flog.write('Ys calc {:2.3f}\n'.format(time.time()-t_0))
        t_0 = time.time()
        
        #self.inv_Y_ii = sparse.linalg.inv()
        self.inv_Y_ii = inv_splu(sparse.csc_matrix(self.Y_ii))        
        flog.write('inv_Y_ii {:2.3f}\n'.format(time.time()-t_0))
        
        self.N_pq_3pn = N_pq_3pn
        self.pq_3pn_int = pq_3pn_int
        self.pq_3pn = pq_3pn
        self.N_pq_3p = N_pq_3p
        self.pq_3p_int = pq_3p_int
        self.pq_3p = pq_3p
        self.N_pq_1p = N_pq_1p
        self.pq_1p_int = pq_1p_int
        self.pq_1p = pq_1p
        self.N_pq_1pn = N_pq_1pn
        self.pq_1pn_int = pq_1pn_int
        self.pq_1pn = pq_1pn
        self.V_known = V_known
        
        self.I_node = np.vstack((np.zeros((self.N_nodes_v,1)),
                                 np.zeros((self.N_nodes_i,1))))+0j

        self.A_n_cols = A_n_cols
        self.Y_primitive_sp = Y_primitive_sp
        self.A_sp = A_sp
        
        self.N_nz_nodes = N_nz_nodes
 
        node_sorter = []
        node_1_sorter = []
        node_2_sorter = []
        node_3_sorter = []
        for bus in self.buses:
            N_nodes = 0
            for node in range(10):
                bus_node = '{:s}.{:s}'.format(str(bus['bus']),str(node))
                if bus_node in self.nodes:
                    node_idx = self.nodes.index(bus_node) 
                    node_sorter += [node_idx]
                    if node == 1:
                        node_1_sorter += [node_idx]
                    if node == 2:
                        node_2_sorter += [node_idx]
                    if node == 3:
                        node_3_sorter += [node_idx]                        
                    N_nodes += 1
                bus.update({'N_nodes':N_nodes})
        self.node_sorter = node_sorter
        self.node_1_sorter = node_1_sorter
        self.node_2_sorter = node_2_sorter
        self.node_3_sorter = node_3_sorter
        flog.close() 
        
        self.set_pf()



    def set_pf(self):
        
        N_i = self.N_nodes_i
        N_v = self.N_nodes_v 
        
        V_unknown_0 = np.zeros((self.N_nodes_i,1),dtype=np.complex128) 

        
        
#        for it in range(int(self.N_nodes_i/4)): # change if not 4 wires
#            
#            V_unknown_0[4*it+0] = self.V_known[0]
#            V_unknown_0[4*it+1] = self.V_known[1]
#            V_unknown_0[4*it+2] = self.V_known[2]
#            V_unknown_0[4*it+3] = 0.0
#        
        buses_in_data_file = [item['bus'] for item in self.buses]
        it = 0
        for node in self.nodes[N_v:]:
            bus,node = node.split('.')
            self.theta_0 = np.deg2rad(0.0)
            
            V_m_nom = self.buses[buses_in_data_file.index(bus)]['U_kV']*1000.0/np.sqrt(3)
            if node == '1': 
                V_unknown_0[it] = V_m_nom*np.exp(1j*(self.theta_0))
            if node == '2': 
                V_unknown_0[it] = V_m_nom*np.exp(1j*(self.theta_0-2.0/3.0*np.pi))
            if node == '3': 
                V_unknown_0[it] = V_m_nom*np.exp(1j*(self.theta_0-4.0/3.0*np.pi))
            if node == '4': 
                V_unknown_0[it] = 0.0
                
            it+=1
            
            
            
        self.V_node = np.vstack((self.V_known,V_unknown_0 ))
        
        if self.pq_3pn_int.shape[0] == 0:
            self.pq_3pn_int = np.array([[0,0,0,0]])
            self.pq_3pn = np.array([[0,0,0]])
            
        if self.pq_3p_int.shape[0] == 0:
            self.pq_3p_int = np.array([[0,0,0]])
            self.pq_3p = np.array([[0,0,0]])
            
        if self.pq_1p_int.shape[0] == 0:
            self.pq_1p_int = np.array([[0]])
            self.pq_1p = np.array([[0]])

        if self.pq_1pn_int.shape[0] == 0:
            self.pq_1pn_int = np.array([[0]])
            self.pq_1pn = np.array([[0]])
            
        if self.gfeed_bus_nodes.shape[0] == 0:
            self.gfeed_bus_nodes = np.array([[0]])
            self.gfeed_currents = np.array([[0]])
            self.gfeed_powers = np.array([[0]])            
            self.gfeed_i_abcn = np.array([[0]])            


        yii = LUstruct(self.Y_ii)[0]
            
        dt_pf = np.dtype([
                  ('pf_solver',np.int32),
                  ('Y_vv',np.complex128,(N_v,N_v)),('Y_iv',np.complex128,(N_i,N_v)),
                  ('inv_Y_ii',np.complex128,(N_i,N_i)),('Y_ii',np.complex128,(N_i,N_i)),
                  ('I_node',np.complex128,(N_v+N_i,1)),('V_node',np.complex128,(N_v+N_i,1)),
                  ('N_gformers',np.int32),('gformer_nodes',np.int32,self.gformer_nodes.shape),('gformers_bus_nodes',np.int32,self.gformer_bus_nodes.shape),
                  ('gform_voltages',np.complex128,self.gformer_voltages.shape),('gform_v_abcn',np.complex128,self.gformer_v_abcn.shape), ('gform_i_abcn',np.complex128,self.gformer_i_abcn.shape),
                  ('N_gfeeds',np.int32),('gfeed_bus_nodes',np.int32,self.gfeed_bus_nodes.shape),
                  ('gfeed_currents',np.complex128,self.gfeed_currents.shape),('gfeed_powers',np.complex128,self.gfeed_powers.shape),('gfeed_i_abcn',np.complex128,self.gfeed_i_abcn.shape),                  
                  ('N_pq_1p',np.int32),('pq_1p_int',np.int32,self.pq_1p_int.shape),('pq_1p',np.complex128,self.pq_1p.shape),('pq_1p_0',np.complex128,self.pq_1p.shape),                  
                  ('N_pq_1pn',np.int32),('pq_1pn_int',np.int32,self.pq_1pn_int.shape),('pq_1pn',np.complex128,self.pq_1pn.shape),('pq_1pn_0',np.complex128,self.pq_1pn.shape),
                  ('N_pq_3p',np.int32),('pq_3p_int',np.int32,self.pq_3p_int.shape),('pq_3p',np.complex128,self.pq_3p.shape),('pq_3p_0',np.complex128,self.pq_3p.shape),
                  ('N_pq_3pn',np.int32),('pq_3pn_int',np.int32,self.pq_3pn_int.shape),('pq_3pn',np.complex128,self.pq_3pn.shape),('pq_3pn_0',np.complex128,self.pq_3pn.shape),
                  ('N_nodes_v',np.int32),('N_nodes_i',np.int32),('iters',np.int32),('N_nz_nodes',np.int32),
                  ('L_indptr',np.int32,yii['L_indptr'].shape), ('L_indices',np.int32,yii['L_indices'].shape), ('L_data',np.complex128,yii['L_data'].shape),
                  ('U_indptr',np.int32,yii['U_indptr'].shape), ('U_indices',np.int32,yii['U_indices'].shape), ('U_data',np.complex128,yii['U_data'].shape),
                  ('perm_r',np.int32, yii['perm_r'].shape),('perm_c',np.int32, yii['perm_c'].shape)] )    


        params_pf = np.rec.array([(
                                self.pf_solver,
                                self.Y_vv,self.Y_iv,
                                self.inv_Y_ii,self.Y_ii.toarray(), 
                                self.I_node,self.V_node,
                                self.N_gformers, self.gformer_nodes, self.gformer_bus_nodes, self.gformer_voltages, self.gformer_v_abcn, self.gformer_i_abcn,
                                self.N_gfeeds, self.gfeed_bus_nodes,self.gfeed_currents,self.gfeed_powers,self.gfeed_i_abcn,
                                self.N_pq_1p, self.pq_1p_int,self.pq_1p,np.copy(self.pq_1p),
                                self.N_pq_1pn, self.pq_1pn_int,self.pq_1pn,np.copy(self.pq_1pn),
                                self.N_pq_3p, self.pq_3p_int,self.pq_3p,np.copy(self.pq_3p),
                                self.N_pq_3pn, self.pq_3pn_int,self.pq_3pn,np.copy(self.pq_3pn),
                                self.N_nodes_v,self.N_nodes_i,0,self.N_nz_nodes,
                                yii['L_indptr'], yii['L_indices'], yii['L_data'],
                                yii['U_indptr'], yii['U_indices'], yii['U_data'],    
                                yii['perm_r'],yii['perm_c'])],
                                dtype=dt_pf)
        self.params_pf = params_pf 
            
    def pf(self):      
        self.params_pf.pf_solver = self.pf_solver
        V_node,I_node = pf_eval(self.params_pf) 

        self.V_node = V_node
        self.I_node = I_node 

        
    def read_loads_shapes(self,json_file):        
        self.json_file = json_file
        self.json_data = open(json_file).read().replace("'",'"')
        data = json.loads(self.json_data)
        self.load_shapes = data

        ts_list = []
        shapes_list = []
        N_loads = 0
        for load in self.loads:
            shape_id = load['shape']
            
            if 'csv_file' in self.load_shapes[shape_id]:
                fname = self.load_shapes[shape_id]['csv_file']
                skiprows = self.load_shapes[shape_id]['header_rows']
                usecol = a2n(self.load_shapes[shape_id]['t_s_column'])
                t_s = np.loadtxt(fname,skiprows=skiprows,delimiter=',',usecols=usecol)
                ts_list += [t_s]
                usecol = a2n(self.load_shapes[shape_id]['shape_column'])
                shape = np.loadtxt(fname, skiprows=skiprows,delimiter=',', usecols=usecol)                
                shapes_list += [shape]       
                N_times = len(shape)
            else:
                ts_list += [np.array(self.load_shapes[shape_id]['t_s'])]
                shapes_list += [np.array(self.load_shapes[shape_id]['shape'])]
                N_times = len(self.load_shapes[shape_id]['shape'])
            
            N_loads += 1   

        N_times_max = 0
        for item in ts_list:
            if len(item) > N_times_max: N_times_max = len(item)

        ts_array = np.zeros((N_times_max,N_loads))
        shapes_array = np.zeros((N_times_max,N_loads)) 
        
        itcol = 0
        for item_t_s,item_load in zip(ts_list,shapes_list):
            idx = N_times_max - len(item_t_s)
            ts_array[idx:,itcol] = item_t_s
            shapes_array[idx:,itcol] = item_load
            itcol += 1
    
        dtype = np.dtype([('time',np.float64,(N_times_max,N_loads)),
                          ('shapes',np.float64,(N_times_max,N_loads)),
                          ('N_loads',np.int32), ('N_times',np.int32)])
        self.params_lshapes = np.rec.array([(ts_array,
                                             shapes_array,
                                       N_loads, N_times_max)],dtype=dtype) 
       
    def read_perturbations(self):
        
        buses_names = [item['bus'] for item in self.loads]
        p = self.data['perturbations']
        N_perturbations = len(p)
        
        load_new_values_list = []
        perturbations_int = []
        perturbations_times_list = []
        perturbations_types_list = []
        
        for it in range(N_perturbations):
            if self.data['perturbations'][it]['type'] == 'load_new_value':
                load_new_values_list += [np.hstack((np.array(p[it]['kw_abc'])*1000.0+np.array(p[it]['kvar_abc'])*1000.0j,np.array([0.0])))] 
                perturbations_times_list += [p[it]['time']]
                perturbations_types_list += [[1]]
                perturbations_int += [buses_names.index(p[it]['bus'])]
                
        self.N_perturbations = N_perturbations  
        
        if self.N_perturbations>0:
            self.load_new_values = np.array(load_new_values_list)
            self.perturbations_int = np.array(perturbations_int).reshape(N_perturbations,1)
            self.perturbations_times = np.array(perturbations_times_list).reshape(N_perturbations,1)     
            self.perturbations_types = np.array(perturbations_types_list).reshape(N_perturbations,1)
        
        
    def run(self):

            self.read_perturbations()
            
            if 'secondary' in self.data:
                secondary_obj = secondary(self.json_file)
            
            if 'vsc' in self.data: vsc_objs = vsc(self.json_file)
            if 'vsc_former' in self.data: vsc_former_objs = vsc_former(self.json_file)
            
            params_secondary = secondary_obj.params_secondary
            self.params_secondary = params_secondary           
            
            params_vsc = vsc_former_objs.params_vsc
            self.params_vsc = params_vsc
            
            self.params_secondary = params_secondary
            
            Dt = self.Dt
            Dt_out = self.Dt_out
            
            N_nodes = self.N_nodes
            N_steps =  self.N_steps
            N_outs = int(N_steps*Dt/Dt_out)
                   
            dt_run = np.dtype([('N_steps', 'int32'),
                               ('Dt',np.float64),
                               ('Dt_out',np.float64),
                               ('T', np.float64,(N_outs,1)),
                               ('T_j_igbt_abcn', np.complex128,(N_outs,4*len(self.params_vsc))),
                               ('T_sink', np.complex128,(N_outs,len(self.params_vsc))),
                               ('out_cplx_i', np.complex128,(N_outs,N_nodes)),
                               ('out_cplx_v', np.complex128,(N_outs,N_nodes)),
                               ('N_outs', 'int32'),
                               ('perturbations_int', 'int32', (self.N_perturbations,1)),
                               ('perturbations_types', 'int32', (self.N_perturbations,1)),
                               ('perturbations_times', np.float64, (self.N_perturbations,1)),
                               ('perturbations_cplx', np.complex128,(self.N_perturbations,4)),
                               ])  
               
            params_run = np.rec.array([(N_steps,
                                        Dt,
                                        Dt_out,
                                        np.zeros((N_outs,1)), # T
                                        np.zeros((N_outs,4*len(self.params_vsc))), # T_j_igbt_abcn
                                        np.zeros((N_outs,len(self.params_vsc))), # T_sink
                                        np.zeros((N_outs,N_nodes)),
                                        np.zeros((N_outs,N_nodes)),                                       
                                        N_outs,
                                        self.perturbations_int,
                                        self.perturbations_types,
                                        self.perturbations_times,
                                        self.load_new_values,                                   
                                        )],dtype=dt_run)    
                  
            self.params_run = params_run
            
            run_eval(params_run,self.params_pf,params_vsc,params_secondary)
                        
    def snapshot(self,t, units='s'):     
        set_load_factor(t,self.params_pf,self.params_lshapes,ig=0)
        V_node,I_node = pf_eval(self.params_pf) 

        self.V_node = V_node
        self.I_node = I_node 

    def timeserie(self,t_ini,t_end,Dt, units='s'):  
        N_cpu = 8
        jobs = []
        for i in range(8):
            p = multiprocessing.Process(target=time_serie,args=(t_ini,t_end,Dt,self.params_pf,self.params_lshapes))
            jobs.append(p)
            p.start()
        self.jobs = jobs
 

#        self.T = T
#        self.Iters = Iters
#        self.V_nodes = V_nodes
#        self.I_nodes = I_nodes 
        

    def get_v(self):
        '''
		Compute phase-neutral and phase-phase voltages from power flow solution and put values 
		in buses dictionary.		
        '''
		
        V_sorted = []
        I_sorted = []
        S_sorted = []
        start_node = 0
        self.V_results = self.V_node
        self.I_results = self.I_node
        
        V_sorted = self.V_node[self.node_sorter]
        I_sorted = self.I_node[self.node_sorter]   
        
        nodes2string = ['v_an','v_bn','v_cn','v_gn']
        for bus in self.buses:
            N_nodes = bus['N_nodes'] 
#            for node in range(5):
#                bus_node = '{:s}.{:s}'.format(str(bus['bus']),str(node))
#                if bus_node in self.nodes:
#                    V = self.V_results[self.nodes.index(bus_node)][0]
#                    V_sorted += [V]
#                    nodes_in_bus += [node]
#            for node in range(5):
#                bus_node = '{:s}.{:s}'.format(str(bus['bus']),str(node))
#                if bus_node in self.nodes:
#                    I = self.I_results[self.nodes.index(bus_node)][0]
#                    I_sorted += [I]
            if N_nodes==3:   # if 3 phases
                v_ag = V_sorted[start_node+0,0]
                v_bg = V_sorted[start_node+1,0]
                v_cg = V_sorted[start_node+2,0]

                i_a = I_sorted[start_node+0,0]
                i_b = I_sorted[start_node+1,0]
                i_c = I_sorted[start_node+2,0]
                
                s_a = (v_ag)*np.conj(i_a)
                s_b = (v_bg)*np.conj(i_b)
                s_c = (v_cg)*np.conj(i_c)
                
                start_node += 3
                bus.update({'v_an':np.abs(v_ag),
                            'v_bn':np.abs(v_bg),
                            'v_cn':np.abs(v_cg),
                            'v_ng':0.0})
                bus.update({'deg_an':np.angle(v_ag, deg=True),
                            'deg_bn':np.angle(v_bg, deg=True),
                            'deg_cn':np.angle(v_cg, deg=True),
                            'deg_ng':np.angle(0, deg=True)})
                bus.update({'v_ab':np.abs(v_ag-v_bg),
                            'v_bc':np.abs(v_bg-v_cg),
                            'v_ca':np.abs(v_cg-v_ag)})
                bus.update({'p_a':s_a.real,
                            'p_b':s_b.real,
                            'p_c':s_c.real})
                bus.update({'q_a':s_a.imag,
                            'q_b':s_b.imag,
                            'q_c':s_c.imag})
            if N_nodes==4:   # if 3 phases + neutral
                v_ag = V_sorted[start_node+0,0]
                v_bg = V_sorted[start_node+1,0]
                v_cg = V_sorted[start_node+2,0]
                v_ng = V_sorted[start_node+3,0]
                i_a = I_sorted[start_node+0,0]
                i_b = I_sorted[start_node+1,0]
                i_c = I_sorted[start_node+2,0]
                i_n = I_sorted[start_node+3,0]  
                
                v_an = v_ag-v_ng
                v_bn = v_bg-v_ng                
                v_cn = v_cg-v_ng
                
                s_a = (v_an)*np.conj(i_a)
                s_b = (v_bn)*np.conj(i_b)
                s_c = (v_cn)*np.conj(i_c)
                bus.update({'v_an':np.abs(v_an),
                            'v_bn':np.abs(v_bn),
                            'v_cn':np.abs(v_cn),
                            'v_ng':np.abs(v_ng)})
                bus.update({'deg_an':np.angle(v_ag-v_ng, deg=True),
                            'deg_bn':np.angle(v_bg-v_ng, deg=True),
                            'deg_cn':np.angle(v_cg-v_ng, deg=True),
                            'deg_ng':np.angle(v_ng, deg=True)})
                bus.update({'v_ab':np.abs(v_ag-v_bg),
                            'v_bc':np.abs(v_bg-v_cg),
                            'v_ca':np.abs(v_cg-v_ag)})
                bus.update({'p_a':s_a.real,
                            'p_b':s_b.real,
                            'p_c':s_c.real})
                bus.update({'q_a':s_a.imag,
                            'q_b':s_b.imag,
                            'q_c':s_c.imag})
    
                start_node += 4
        self.V = np.array(V_sorted).reshape(len(V_sorted),1) 
        return 0 #self.V              
        
    def get_i(self):
        '''
		Compute line currents from power flow solution and put values 
		in transformers and lines dictionaries.		
        '''
       
        I_lines = self.Y_primitive_sp @ self.A_sp.T @ self.V_results
                
        it_single_line = 0
        for trafo in self.transformers:
            
            if 'conductors_j' in trafo: 
                cond_1 = trafo['conductors_j']
            else:
                cond_1 = trafo['conductors_1']
            if 'conductors_k' in trafo: 
                cond_2 = trafo['conductors_k']
            else:
                cond_2 = trafo['conductors_2']  
            
            I_1a = (I_lines[it_single_line,0])
            I_1b = (I_lines[it_single_line+1,0])
            I_1c = (I_lines[it_single_line+2,0])
            I_1n = (I_lines[it_single_line+3,0])
            
            I_2a = (I_lines[it_single_line+cond_1+0,0])
            I_2b = (I_lines[it_single_line+cond_1+1,0])
            I_2c = (I_lines[it_single_line+cond_1+2,0])
            I_2n = (I_lines[it_single_line+cond_1+3,0])
            
            #I_n = (I_lines[it_single_line+3,0])
            if cond_1 <=3:
                I_1n = I_1a+I_1b+I_1c
            if cond_2 <=3:
                I_2n = I_2a+I_2b+I_2c
                
            it_single_line += cond_1 + cond_2
            trafo.update({'i_1a_m':np.abs(I_1a)})
            trafo.update({'i_1b_m':np.abs(I_1b)})
            trafo.update({'i_1c_m':np.abs(I_1c)})
            trafo.update({'i_1n_m':np.abs(I_1n)})
            trafo.update({'i_2a_m':np.abs(I_2a)})
            trafo.update({'i_2b_m':np.abs(I_2b)})
            trafo.update({'i_2c_m':np.abs(I_2c)})
            trafo.update({'i_2n_m':np.abs(I_2n)})
            trafo.update({'deg_1a':np.angle(I_1a, deg=True)})
            trafo.update({'deg_1b':np.angle(I_1b, deg=True)})
            trafo.update({'deg_1c':np.angle(I_1c, deg=True)})
            trafo.update({'deg_1n':np.angle(I_1n, deg=True)})
            trafo.update({'deg_2a':np.angle(I_2a, deg=True)})
            trafo.update({'deg_2b':np.angle(I_2b, deg=True)})
            trafo.update({'deg_2c':np.angle(I_2c, deg=True)})
            trafo.update({'deg_2n':np.angle(I_2n, deg=True)})
                        
        self.I_lines = I_lines
        for line in self.lines:
            N_conductors = len(line['bus_j_nodes'])
            if N_conductors == 3:
                I_a = (I_lines[it_single_line,0])
                I_b = (I_lines[it_single_line+1,0])
                I_c = (I_lines[it_single_line+2,0])
                #I_n = (I_lines[it_single_line+3,0])
                I_n = I_a+I_b+I_c
                it_single_line += N_conductors
                line.update({'i_a_m':np.abs(I_a)})
                line.update({'i_b_m':np.abs(I_b)})
                line.update({'i_c_m':np.abs(I_c)})
                line.update({'i_n_m':np.abs(I_n)})
                line.update({'deg_a':np.angle(I_a, deg=True)})
                line.update({'deg_b':np.angle(I_b, deg=True)})
                line.update({'deg_c':np.angle(I_c, deg=True)})
                line.update({'deg_n':np.angle(I_n, deg=True)})
            if N_conductors == 4:
                I_a = (I_lines[it_single_line,0])
                I_b = (I_lines[it_single_line+1,0])
                I_c = (I_lines[it_single_line+2,0])
                I_n = (I_lines[it_single_line+3,0])
                it_single_line += N_conductors
                line.update({'i_a_m':np.abs(I_a)})
                line.update({'i_b_m':np.abs(I_b)})
                line.update({'i_c_m':np.abs(I_c)})
                line.update({'i_n_m':np.abs(I_n)})
                line.update({'deg_a':np.angle(I_a, deg=True)})
                line.update({'deg_b':np.angle(I_b, deg=True)})
                line.update({'deg_c':np.angle(I_c, deg=True)})
                line.update({'deg_n':np.angle(I_n, deg=True)})                                   


    def bokeh_tools(self):

        
        self.bus_tooltip = '''
            <div>
            bus_id = @bus_id 
            <table border="1">
                <tr>
                <td>v<sub>an</sub> =  @v_an  &ang; @deg_an V </td> <td> S<sub>a</sub> = @p_a + j@q_a </td>
                </tr>
                      <tr>
                      <td> </td> <td>v<sub>ab</sub>= @v_ab V</td>
                      </tr>
                <tr>
                <td>v<sub>bn</sub> = @v_bn &ang; @deg_bn V </td><td> S<sub>b</sub> = @p_b + j@q_b </td>
                </tr>
                      <tr>
                      <td> </td><td>v<sub>bc</sub>= @v_bc V</td>
                      </tr>
                <tr>
                <td>v<sub>cn</sub>  = @v_cn &ang; @deg_cn V </td>  <td>S<sub>c</sub> = @p_c + j@q_c </td>
                </tr> 
                    <tr>
                     <td> </td> <td>v<sub>ca</sub>= @v_ca V</td>
                    </tr>
               <tr>
                <td>v<sub>ng</sub>    = @v_ng &ang; @deg_ng V</td>  <td>S<sub>abc</sub> = @p_abc + j@q_abc </td>
              </tr>
            </table>
            </div>
            '''
            
        x = [item['pos_x'] for item in self.buses]
        y = [item['pos_y'] for item in self.buses]
        bus_id = [item['bus'] for item in self.buses]
        v_an = ['{:2.2f}'.format(float(item['v_an'])) for item in self.buses]
        v_bn = ['{:2.2f}'.format(float(item['v_bn'])) for item in self.buses]
        v_cn = ['{:2.2f}'.format(float(item['v_cn'])) for item in self.buses]
        v_ng = ['{:2.2f}'.format(float(item['v_ng'])) for item in self.buses]
        sqrt3=np.sqrt(3)
        v_an_pu = ['{:2.4f}'.format(float(item['v_an'])/float(item['U_kV'])/1000.0*sqrt3) for item in self.buses]
        v_bn_pu = ['{:2.4f}'.format(float(item['v_bn'])/float(item['U_kV'])/1000.0*sqrt3) for item in self.buses]
        v_cn_pu = ['{:2.4f}'.format(float(item['v_cn'])/float(item['U_kV'])/1000.0*sqrt3) for item in self.buses]
        v_ng_pu = ['{:2.4f}'.format(float(item['v_ng'])/float(item['U_kV'])/1000.0*sqrt3) for item in self.buses]
        
        deg_an = ['{:2.2f}'.format(float(item['deg_an'])) for item in self.buses]
        deg_bn = ['{:2.2f}'.format(float(item['deg_bn'])) for item in self.buses]
        deg_cn = ['{:2.2f}'.format(float(item['deg_cn'])) for item in self.buses]
        deg_ng = ['{:2.2f}'.format(float(item['deg_ng'])) for item in self.buses]
        v_ab = [item['v_ab'] for item in self.buses]
        v_bc = [item['v_bc'] for item in self.buses]
        v_ca = [item['v_ca'] for item in self.buses]
        
        p_a = ['{:2.2f}'.format(float(item['p_a']/1000)) for item in self.buses]
        p_b = ['{:2.2f}'.format(float(item['p_b']/1000)) for item in self.buses]
        p_c = ['{:2.2f}'.format(float(item['p_c']/1000)) for item in self.buses]
        q_a = ['{:2.2f}'.format(float(item['q_a']/1000)) for item in self.buses]
        q_b = ['{:2.2f}'.format(float(item['q_b']/1000)) for item in self.buses]
        q_c = ['{:2.2f}'.format(float(item['q_c']/1000)) for item in self.buses]   
        p_abc = ['{:2.2f}'.format(float((item['p_a'] +item['p_b']+item['p_c'])/1000)) for item in self.buses] 
        q_abc = ['{:2.2f}'.format(float((item['q_a'] +item['q_b']+item['q_c'])/1000)) for item in self.buses]
        s_radio = []
        s_color = []
        
        for item in self.buses:
            p_total = item['p_a'] + item['p_b'] + item['p_c']
            q_total = item['q_a'] + item['q_b'] + item['q_c']            
            s_total = np.abs(p_total + 1j*q_total)
            scale = self.s_radio_scale
            s_scaled = abs(np.sqrt(s_total))*scale
            if s_scaled<self.s_radio_min :
                s_scaled = self.s_radio_min 
            if s_scaled>self.s_radio_max:
                s_scaled = self.s_radio_max
            s_radio += [s_scaled]
            if p_total>0.0:
                s_color += ['red']
            if p_total<0.0:
                s_color += ['green']
            if p_total==0.0:
                s_color += ['blue']
                                
                
        self.bus_data = dict(x=x, y=y, bus_id=bus_id,
                             v_an=v_an, v_bn=v_bn, v_cn=v_cn, v_ng=v_ng, 
                             v_an_pu=v_an_pu, v_bn_pu=v_bn_pu, v_cn_pu=v_cn_pu, 
                             deg_an=deg_an, deg_bn=deg_bn, deg_cn=deg_cn, 
                             deg_ng=deg_ng,v_ab=v_ab,v_bc=v_bc,v_ca=v_ca,
                             p_a=p_a,p_b=p_b,p_c=p_c,
                             q_a=q_a,q_b=q_b,q_c=q_c,
                             p_abc=p_abc,q_abc=q_abc,
                             s_radio=s_radio, s_color=s_color)
        
        self.line_tooltip = '''
            <div>
            line id = @line_id 
            <table border="1">
                <tr>
                <td>I<sub>a</sub> =  @i_a_m &ang; @deg_a </td>
                </tr>
                <tr>
                <td>I<sub>b</sub> =  @i_b_m &ang; @deg_b </td>
                </tr>
                <tr>
                <td>I<sub>c</sub> =  @i_c_m &ang; @deg_c </td>
                </tr>
                <tr>
                <td>I<sub>n</sub> =  @i_n_m &ang; @deg_n </td>
                </tr>
            </table>            
            </div>
            '''
            
        bus_id_to_x = dict(zip(bus_id,x))
        bus_id_to_y = dict(zip(bus_id,y))
        
        x_j = [bus_id_to_x[item['bus_j']] for item in self.lines]
        y_j = [bus_id_to_y[item['bus_j']] for item in self.lines]
        x_k = [bus_id_to_x[item['bus_k']] for item in self.lines]
        y_k = [bus_id_to_y[item['bus_k']] for item in self.lines]
        
        x_s = []
        y_s = []
        for line in self.lines:
            x_s += [[ bus_id_to_x[line['bus_j']] , bus_id_to_x[line['bus_k']]]]
            y_s += [[ bus_id_to_y[line['bus_j']] , bus_id_to_y[line['bus_k']]]]
            
        i_a_m = [item['i_a_m'] for item in self.lines]
        i_b_m = [item['i_b_m'] for item in self.lines]
        i_c_m = [item['i_c_m'] for item in self.lines]
        i_n_m = [item['i_n_m'] for item in self.lines]
        
        deg_a = [item['deg_a'] for item in self.lines]
        deg_b = [item['deg_b'] for item in self.lines]
        deg_c = [item['deg_c'] for item in self.lines]
        deg_n = [item['deg_n'] for item in self.lines]        
        line_id = ['{:s}-{:s}'.format(item['bus_j'],item['bus_k']) for item in self.lines]
#        self.line_data = dict(x_j=x_j, x_k=x_k, y_j=y_j, y_k=y_k, line_id=line_id,
#                             i_a_m=i_a_m)
        self.line_data = dict(x_s=x_s, y_s=y_s, line_id=line_id,
                             i_a_m=i_a_m, i_b_m=i_b_m, i_c_m=i_c_m, i_n_m=i_n_m,
                             deg_a=deg_a, deg_b=deg_b, deg_c=deg_c, deg_n=deg_n)


        
        self.transformer_tooltip = '''
            <div>
            line id = @trafo_id  
            <table border="5">
                <tr >
                    <td>I<sub>1a</sub> =  @i_1a_m &ang; @deg_1a </td>
                    <td>I<sub>2a</sub> =  @i_2a_m &ang; @deg_2a </td>
                </tr>
                <tr>
                    <td >I<sub>1b</sub> =  @i_1b_m &ang; @deg_1b </td>
                    <td >I<sub>2b</sub> =  @i_2b_m &ang; @deg_2b </td>
                </tr>
                <tr>
                    <td >I<sub>1c</sub> =  @i_1c_m &ang; @deg_1c </td>
                    <td >I<sub>2c</sub> =  @i_2c_m &ang; @deg_2c </td>
                </tr>
                <tr>
                    <td >I<sub>1n</sub> =  @i_1n_m &ang; @deg_1n </td>
                    <td >I<sub>2n</sub> =  @i_2n_m &ang; @deg_2n </td>
                </tr>
            </table>            
            </div>
            '''
            
        bus_id_to_x = dict(zip(bus_id,x))
        bus_id_to_y = dict(zip(bus_id,y))
        
        x_j = [bus_id_to_x[item['bus_j']] for item in self.transformers]
        y_j = [bus_id_to_y[item['bus_j']] for item in self.transformers]
        x_k = [bus_id_to_x[item['bus_k']] for item in self.transformers]
        y_k = [bus_id_to_y[item['bus_k']] for item in self.transformers]
        
        x_s = []
        y_s = []
        for line in self.transformers:
            x_s += [[ bus_id_to_x[line['bus_j']] , bus_id_to_x[line['bus_k']]]]
            y_s += [[ bus_id_to_y[line['bus_j']] , bus_id_to_y[line['bus_k']]]]
            
        i_1a_m = [item['i_1a_m'] for item in self.transformers]
        i_1b_m = [item['i_1b_m'] for item in self.transformers]
        i_1c_m = [item['i_1c_m'] for item in self.transformers]
        i_1n_m = [item['i_1n_m'] for item in self.transformers]

        i_2a_m = [item['i_2a_m'] for item in self.transformers]
        i_2b_m = [item['i_2b_m'] for item in self.transformers]
        i_2c_m = [item['i_2c_m'] for item in self.transformers]
        i_2n_m = [item['i_2n_m'] for item in self.transformers]
        
        deg_1a = [item['deg_1a'] for item in self.transformers]
        deg_1b = [item['deg_1b'] for item in self.transformers]
        deg_1c = [item['deg_1c'] for item in self.transformers]
        deg_1n = [item['deg_1n'] for item in self.transformers]    
        
        deg_2a = [item['deg_2a'] for item in self.transformers]
        deg_2b = [item['deg_2b'] for item in self.transformers]
        deg_2c = [item['deg_2c'] for item in self.transformers]
        deg_2n = [item['deg_2n'] for item in self.transformers]  
        
        trafo_id = ['{:s}-{:s}'.format(item['bus_j'],item['bus_k']) for item in self.transformers]
#        self.line_data = dict(x_j=x_j, x_k=x_k, y_j=y_j, y_k=y_k, line_id=line_id,
#                             i_a_m=i_a_m)
        self.transformer_data = dict(x_s=x_s, y_s=y_s, trafo_id=trafo_id,
                                     i_1a_m=i_1a_m, i_1b_m=i_1b_m, i_1c_m=i_1c_m, i_1n_m=i_1n_m,
                                     deg_1a=deg_1a, deg_1b=deg_1b, deg_1c=deg_1c, deg_1n=deg_1n,
                                     i_2a_m=i_2a_m, i_2b_m=i_2b_m, i_2c_m=i_2c_m, i_2n_m=i_2n_m,
                                     deg_2a=deg_2a, deg_2b=deg_2b, deg_2c=deg_2c, deg_2n=deg_2n)
        
        return self.bus_data


def LUstruct(A_sp):
    LU_sp = sla.splu(sparse.csc_matrix(A_sp))
    L_sp = LU_sp.L
    U_sp = LU_sp.U

    N = LU_sp.shape[0]
    Pr = sparse.lil_matrix((N, N))
    Pr[LU_sp.perm_r, np.arange(N)] = 1
    Pc = sparse.lil_matrix((N, N))
    Pc[np.arange(N), LU_sp.perm_c] = 1
    
    L_csr = sparse.csr_matrix(L_sp)
    U_csr = sparse.csr_matrix(U_sp)
    perm_r = (Pr @ LU_sp.perm_r @ Pr.T).astype(np.int32)
    
    struct = np.rec.array([(L_csr.indptr,
                            L_csr.indices,
                            L_csr.data,
                            U_csr.indptr,
                            U_csr.indices,
                            U_csr.data,
                            perm_r,
                            LU_sp.perm_c)],
                   dtype=[
                         ('L_indptr',np.int32,L_csr.indptr.shape),
                         ('L_indices',np.int32,L_csr.indices.shape),
                         ('L_data',np.complex128,L_csr.data.shape),
                         ('U_indptr',np.int32,U_csr.indptr.shape),
                         ('U_indices',np.int32,U_csr.indices.shape),
                         ('U_data',np.complex128,U_csr.data.shape),
                         ('perm_r',np.int32, LU_sp.perm_r.shape),
                         ('perm_c',np.int32, LU_sp.perm_c.shape)                         
                     ])
    return struct


def diag_2d_inv(Z_line_list):

    N_cols = 0

    for Z_line in Z_line_list:
        N_cols += Z_line.shape[1]

    Y_lines = np.zeros((N_cols,N_cols))+0j

    it = 0
    for Z_line in Z_line_list:
        Y_line = np.linalg.inv(Z_line)
        N = Y_line.shape[0] 
        Y_lines[it:(it+N),it:(it+N)] = Y_line
        it += N

    return Y_lines

def diag_2dsparse_inv(Z_line_list):

    N_cols = 0

    for Z_line in Z_line_list:
        N_cols += Z_line.shape[1]

    Y_lines = sparse.lil_matrix((N_cols,N_cols),dtype=np.complex128)

    it = 0
    for Z_line in Z_line_list:
        Y_line = np.linalg.inv(Z_line)
        N = Y_line.shape[0] 
        Y_lines[it:(it+N),it:(it+N)] = Y_line
        it += N

    return Y_lines

def diag_2dsparse(Y_prim_list):

    N_cols = 0

    for Y_prim in Y_prim_list:
        N_cols += Y_prim.shape[1]

    Y_prims = sparse.lil_matrix((N_cols,N_cols),dtype=np.complex128)

    it = 0
    for Y_prim in Y_prim_list:
        N = Y_prim.shape[0] 
        Y_prims[it:(it+N),it:(it+N)] = Y_prim
        it += N

    return Y_prims

def diag_2d(Y_prim_list):

    N_cols = 0

    for Y_prim in Y_prim_list:
        N_cols += Y_prim.shape[1]

    Y_prims = np.zeros((N_cols,N_cols),dtype=np.complex128)

    it = 0
    for Y_prim in Y_prim_list:
        N = Y_prim.shape[0] 
        Y_prims[it:(it+N),it:(it+N)] = Y_prim
        it += N

    return Y_prims

def inv_splu(A_sparse):
    N = A_sparse.shape[0]
    lu = sla.splu(A_sparse)
    return lu.solve(np.eye(N,dtype=np.complex128))
    #return np.linalg.inv(A_sparse.toarray())

def n2a(n,b=string.ascii_uppercase):
   d, m = divmod(n,len(b))
   return n2a(d-1,b)+b[m] if d else b[m]

def a2n(column):
    num_column = 0
    for it in range(len(column)):
        num_column += ord(column[it])-65+26*it
    return num_column

def trafo_yprim(S_n,U_1n,U_2n,Z_cc,connection='Dyg11'):
    '''
    Trafo primitive as developed in: (in the paper Ynd11)
    R. C. Dugan and S. Santoso, “An example of 3-phase transformer modeling for distribution system analysis,” 
    2003 IEEE PES Transm. Distrib. Conf. Expo. (IEEE Cat. No.03CH37495), vol. 3, pp. 1028–1032, 2003. 
    
    '''

    if connection=='Dyn1':
        z_a = Z_cc*1.0**2/S_n
        z_b = Z_cc*1.0**2/S_n
        z_c = Z_cc*1.0**2/S_n
        U_1 = U_1n
        U_2 = U_2n/np.sqrt(3)
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             
        N_a = np.array([[ 1/U_1,     0],
                         [-1/U_1,     0],
                         [     0, 1/U_2],
                         [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((7,12))

        A_trafo[0,0] = 1.0
        A_trafo[0,9] = 1.0
        A_trafo[1,1] = 1.0
        A_trafo[1,4] = 1.0
        A_trafo[2,5] = 1.0
        A_trafo[2,8] = 1.0

        A_trafo[3,2] = 1.0
        A_trafo[4,6] = 1.0
        A_trafo[5,10] = 1.0
        
        A_trafo[6,3] = 1.0
        A_trafo[6,7] = 1.0
        A_trafo[6,11] = 1.0


    if connection=='Dyn5':
        z_a = Z_cc*1.0**2/S_n
        z_b = Z_cc*1.0**2/S_n
        z_c = Z_cc*1.0**2/S_n
        U_1 = U_1n
        U_2 = U_2n/np.sqrt(3)
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             
        N_a = np.array([[ 1/U_1,     0],
                         [-1/U_1,     0],
                         [     0, 1/U_2],
                         [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((7,12))

        A_trafo[0,1] = 1.0
        A_trafo[0,4] = 1.0
        A_trafo[1,5] = 1.0
        A_trafo[1,8] = 1.0
        A_trafo[2,0] = 1.0
        A_trafo[2,9] = 1.0

        A_trafo[3,2] = 1.0
        A_trafo[4,6] = 1.0
        A_trafo[5,10] = 1.0
        
        A_trafo[6,3] = 1.0
        A_trafo[6,7] = 1.0
        A_trafo[6,11] = 1.0


    if connection=='Dyn11':
        z_a = Z_cc*1.0**2/S_n*3
        z_b = Z_cc*1.0**2/S_n*3
        z_c = Z_cc*1.0**2/S_n*3
        U_1 = U_1n
        U_2 = U_2n/np.sqrt(3)
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             
        N_a = np.array([[ 1/U_1,     0],
                         [-1/U_1,     0],
                         [     0, 1/U_2],
                         [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((7,12))

        A_trafo[0,1] = 1.0
        A_trafo[0,4] = 1.0
        A_trafo[1,5] = 1.0
        A_trafo[1,8] = 1.0
        A_trafo[2,0] = 1.0
        A_trafo[2,9] = 1.0

        A_trafo[3,3] = 1.0
        A_trafo[4,7] = 1.0
        A_trafo[5,11] = 1.0
        
        A_trafo[6,2] = 1.0
        A_trafo[6,6] = 1.0
        A_trafo[6,10] = 1.0


    if connection=='Ygd5_3w':
        z_a = Z_cc*1.0**2/S_n
        z_b = Z_cc*1.0**2/S_n
        z_c = Z_cc*1.0**2/S_n
        U_1 = U_1n #
        U_2 = U_2n*np.sqrt(3)
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             
        N_a = np.array([[ 1/U_1,     0],
                         [-1/U_1,     0],
                         [     0, 1/U_2],
                         [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((6,12))

        A_trafo[0,0] = 1.0
        A_trafo[1,4] = 1.0
        A_trafo[2,8] = 1.0
        
        A_trafo[3,3]  = 1.0
        A_trafo[3,6]  = 1.0
        A_trafo[4,7]  = 1.0
        A_trafo[4,10] = 1.0
        A_trafo[5,2]  = 1.0
        A_trafo[5,11] = 1.0

    if connection=='Ygd1_3w':
        z_a = Z_cc*1.0**2/S_n
        z_b = Z_cc*1.0**2/S_n
        z_c = Z_cc*1.0**2/S_n
        U_1 = U_1n #
        U_2 = U_2n*np.sqrt(3)
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             
        N_a = np.array([[ 1/U_1,     0],
                         [-1/U_1,     0],
                         [     0, 1/U_2],
                         [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((6,12))

        A_trafo[0,0] = 1.0
        A_trafo[1,4] = 1.0
        A_trafo[2,8] = 1.0
        
        A_trafo[3,2]  = 1.0
        A_trafo[3,11]  = 1.0
        A_trafo[4,3]  = 1.0
        A_trafo[4,6] = 1.0
        A_trafo[5,7]  = 1.0
        A_trafo[5,10] = 1.0

    if connection=='Ygd11_3w':
        z_a = Z_cc*1.0**2/S_n
        z_b = Z_cc*1.0**2/S_n
        z_c = Z_cc*1.0**2/S_n
        U_1 = U_1n #
        U_2 = U_2n*np.sqrt(3)
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             
        N_a = np.array([[ 1/U_1,     0],
                         [-1/U_1,     0],
                         [     0, 1/U_2],
                         [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((6,12))

        A_trafo[0,1] = 1.0
        A_trafo[1,5] = 1.0
        A_trafo[2,9] = 1.0
        
        A_trafo[3,3]  = 1.0
        A_trafo[3,6]  = 1.0
        A_trafo[4,7]  = 1.0
        A_trafo[4,10] = 1.0
        A_trafo[5,2]  = 1.0
        A_trafo[5,11] = 1.0

    if connection=='ZigZag':
        z_a = Z_cc*1.0**2/S_n*3
        z_b = Z_cc*1.0**2/S_n*3
        z_c = Z_cc*1.0**2/S_n*3
        U_1 = U_1n #
        U_2 = U_2n
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             


        
        N = np.zeros((12,6))
        N[0,0] =  1.0/U_1
        N[1,0] = -1.0/U_1
        N[6,0] = -1.0/U_1
        N[7,0] =  1.0/U_1

        N[4,2]  =  1.0/U_1
        N[5,2]  = -1.0/U_1
        N[10,2] = -1.0/U_1
        N[11,2] =  1.0/U_1

        N[8,4] =  1.0/U_1
        N[9,4] = -1.0/U_1
        N[2,4] = -1.0/U_1
        N[3,4] =  1.0/U_1
        
        
        N[2,1] =  1.0/U_2
        N[3,1] = -1.0/U_2
    
        N[6,3] =  1.0/U_2
        N[7,3] = -1.0/U_2  

        N[10,5] =  1.0/U_2
        N[11,5] = -1.0/U_2 
        
        #          0  1  2  3  4  5
        # 0 Iw1a   1                   Ia1 0
        # 1 Iw2a  -1                   Ia2 1
        # 2 Iw3a      2                Ib1 2
        # 3 Iw4a     -2                Ib2 3
        # 4 Iw1b         1             Ic1 4
        # 5 Iw2b        -1             Ic2 5
        # 6 Iw3b            2
        # 7 Iw4b           -2
        # 8 Iw1c               1
        # 9 Iw2c              -1
        #10 Iw3c                  2
        #11 Iw4c                 -2
        
        #          0  1  2  3  4  5
        # 0 Iw1a   1                   Ia1 0
        # 1 Iw2a  -1                   Ia2 1
        # 2 Iw3a      2       -1       Ib1 2
        # 3 Iw4a     -2       -1       Ib2 3
        # 4 Iw1b         1             Ic1 4
        # 5 Iw2b        -1             Ic2 5
        # 6 Iw3b  -1        2
        # 7 Iw4b  -1       -2
        # 8 Iw1c               1 
        # 9 Iw2c              -1
        #10 Iw3c        -1        2
        #11 Iw4c        -1       -2
        
        
        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((7,12))

        A_trafo[0,0] = 1.0
        A_trafo[1,4] = 1.0
        A_trafo[2,8] = 1.0         
        
        A_trafo[6,3]  = 1.0
        A_trafo[6,7]  = 1.0
        A_trafo[6,11] = 1.0
        

        
    if connection=='Dyg11_3w':
        z_a = Z_cc*1.0**2/S_n
        z_b = Z_cc*1.0**2/S_n
        z_c = Z_cc*1.0**2/S_n
        U_1 = U_1n
        U_2 = U_2n/np.sqrt(3)
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])                             
        N_a = np.array([[ 1/U_1,     0],
                         [-1/U_1,     0],
                         [     0, 1/U_2],
                         [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
    
        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((6,12))

        A_trafo[0,1] = 1.0
        A_trafo[0,4] = 1.0
        A_trafo[1,5] = 1.0
        A_trafo[1,8] = 1.0
        A_trafo[2,0] = 1.0
        A_trafo[2,9] = 1.0

        A_trafo[3,3] = 1.0
        A_trafo[4,7] = 1.0
        A_trafo[5,11] = 1.0
        
#    if connection=='Dyg11_3w':
#        z_a = Z_cc*1.0**2/S_n
#        z_b = Z_cc*1.0**2/S_n
#        z_c = Z_cc*1.0**2/S_n
#        U_1 = U_1n/np.sqrt(3)
#        U_2 = U_2n
#        Z_B = np.array([[z_a, 0.0, 0.0],
#                        [0.0, z_b, 0.0],
#                        [0.0, 0.0, z_c],])                             
#        N_a = np.array([[ 1/U_1,     0],
#                         [-1/U_1,     0],
#                         [     0, 1/U_2],
#                         [     0,-1/U_2]])           
#        N_row_a = np.hstack((N_a,np.zeros((4,4))))
#        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
#        N_row_c = np.hstack((np.zeros((4,4)),N_a))
#        
#        N = np.vstack((N_row_a,N_row_b,N_row_c))
#
#        B = np.array([[ 1, 0, 0],
#                      [-1, 0, 0],
#                      [ 0, 1, 0],
#                      [ 0,-1, 0],
#                      [ 0, 0, 1],
#                      [ 0, 0,-1]])
#    
#        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
#        Y_w = N @ Y_1 @ N.T
#        A_trafo = np.zeros((6,12))
#
#        A_trafo[0,1] = 1.0
#        A_trafo[0,4] = 1.0
#        A_trafo[1,5] = 1.0
#        A_trafo[1,8] = 1.0
#        A_trafo[2,0] = 1.0
#        A_trafo[2,9] = 1.0
#
#        A_trafo[3,3] = 1.0
#        A_trafo[4,7] = 1.0
#        A_trafo[5,11] = 1.0
               
    if connection=='Ynd11':
        z_a = Z_cc*1.0**2/S_n
        z_b = Z_cc*1.0**2/S_n
        z_c = Z_cc*1.0**2/S_n
        U_1 = U_1n/np.sqrt(3)
        U_2 = U_2n
        Z_B = np.array([[z_a, 0.0, 0.0],
                        [0.0, z_b, 0.0],
                        [0.0, 0.0, z_c],])   

        B = np.array([[ 1, 0, 0],
                      [-1, 0, 0],
                      [ 0, 1, 0],
                      [ 0,-1, 0],
                      [ 0, 0, 1],
                      [ 0, 0,-1]])
                          
        N_a = np.array([[ 1/U_1,     0],
                        [-1/U_1,     0],
                        [     0, 1/U_2],
                        [     0,-1/U_2]])           
        N_row_a = np.hstack((N_a,np.zeros((4,4))))
        N_row_b = np.hstack((np.zeros((4,2)),N_a,np.zeros((4,2))))
        N_row_c = np.hstack((np.zeros((4,4)),N_a))
        
        N = np.vstack((N_row_a,N_row_b,N_row_c))

        Y_1 = B @ np.linalg.inv(Z_B) @ B.T
        Y_w = N @ Y_1 @ N.T
        A_trafo = np.zeros((7,12))
        A_trafo[0,0] = 1.0
        A_trafo[1,4] = 1.0
        A_trafo[2,8] = 1.0
        
        A_trafo[3,1] = 1.0
        A_trafo[3,5] = 1.0
        A_trafo[3,9] = 1.0
        
        A_trafo[4,2] = 1.0
        A_trafo[4,11] = 1.0
        A_trafo[5,3] = 1.0
        A_trafo[5,6] = 1.0
        A_trafo[6,7] = 1.0
        A_trafo[6,10] = 1.0
        
        
    Y_prim = A_trafo @ Y_w @ A_trafo.T
    
    return Y_prim


class opendss(object):
    
    def __init__(self):
        
        pass

    def pyss2opendss(self):
        
        string = ''
        for item in sys.loads:
            string += 'New Load.L_{:s} '.format(item['bus'])
            string += 'Phases=3 Bus1={:s} kV=0.231 kVA={:2.3f} PF={:2.2f}'.format(item['bus'],item['kVA'],item['pf'])    
            string += '\n' 
        for item in sys.lines:
            # New Line.LINE1 Bus1=1 Bus2=2 
            string += 'New Line.LINE_{:s}_{:s} Bus1={:s} Bus2={:s} '.format(item['bus_j'],item['bus_k'],item['bus_j'],item['bus_k'])
            string += 'phases=3 Linecode={:s} Length={:f} Units=m'.format(item['code'],item['m'])    
            string += '\n'         
        for item in line_codes:
            #New LineCode.UG3  nphases=3  BaseFreq=50 
            #~ rmatrix = (1.152 | 0.321   1.134 | 0.33 0.321 1.152)
            #~ xmatrix = (0.458  | 0.39 0.477   | 0.359 0.390 0.458)
            #~ units=km 
            string += 'New LineCode.{:s} '.format(item)
            Z_list = line_codes[item]
            N_conductors = len(Z_list)
            string += 'nphases={:d}  BaseFreq=50 \n'.format(N_conductors) 
            Z = np.array(Z_list)
            R = Z.real
            X = Z.imag
            string += '~ rmatrix = ('
            for it in range(N_conductors):
                row = R[it,0:it+1]
                for item_col in row:
                    string += '{:f} '.format(item_col)
                if it == N_conductors-1:
                    string += ')\n'
                else:
                    string += '| '
            string += '~ xmatrix = ('
            for it in range(N_conductors):
                row = X[it,0:it+1]
                for item_col in row:
                    string += '{:f} '.format(item_col)
                if it == N_conductors-1:
                    string += ')\n'
                else:
                    string += '| '                
            string += '~ units=km \n'
        return string
            
    def read_v_results(self, file):
        
        fobj = open(file)
        
        lines = fobj.readlines()
               
        for line in lines:
            print(line[5:6])
            
        return string        
    

   


def abcn2abc(Z_abcn):
    '''
    From the primitive impedance matrix, the phase impedance matrix 
    can be obtained from Kron reduction:
    
    '''
    Z_pp = Z_abcn[0:3,0:3] 
    Z_pn = Z_abcn[0:3,3:]
    Z_np = Z_abcn[3:, 0:3]
    Z_nn = Z_abcn[3:,3:]
    Z_abc = Z_pp - Z_pn @ np.linalg.inv(Z_nn) @ Z_np
    return Z_abc
    

   
def opendss2pydgrid(self,files_dict):
    
    
    return files_dict  

if __name__ == "__main__":
    import time 
    test ='cigre_lv'

    if test=='luna_1': 
        sys1 = grid()
        t_0 = time.time()
        sys1.read('../examples/luna/luna_1_4w.json')  # Load data
        sys1.pf()
        sys1.get_v()
        sys1.get_i()
        print('iters: ', sys1.params_pf['iters'])
        
    if test=='cigre_lv': 
        sys1 = grid()
        t_0 = time.time()
        sys1.read('../examples/cigre/cigre_europe_residential.json')  # Load data
        print('sys1.read()',time.time()-t_0) 
        t_0 = time.time()
        sys1.pf()
        sys1.get_v()
        sys1.get_i()
        print('sys1.pf()',time.time()-t_0) 
        t_0 = time.time()
        print('iters: ', sys1.params_pf['iters'])
        
    if test=='lv_europe_connected_load1': 
        sys1 = pydgrid()
        t_0 = time.time()
        t_0 = time.time()
        sys1.read('lv_europe_connected_load1.json')  # Load data
        print('sys1.read()',time.time()-t_0) 
        t_0 = time.time()
        sys1.pf()
        print('sys1.pf()',time.time()-t_0) 
        t_0 = time.time()

    if test=='bus4_1p_load':
        sys1 = pydgrid()
        sys1.read('bus4_1p_load.json')
        sys1.pf()
        sys1.get_v()
        sys1.get_i()
        #sys1.bokeh_tools()
        
    if test=='lveurope':
        sys1 = pydgrid()
        sys1.read('lv_europe_connected.json')  # Load data
        sys1.pf()
        sys1.get_v()
        sys1.get_i()
        sys1.bokeh_tools()
        
    if test=='trafo':
        S_n = 630.0e3
        U_1n = 400.0
        U_2n = 20.0e3
        Z_cc_pu = 0.01+0.04j
        Y_trafo_prim = trafo_yprim(S_n,U_1n,U_2n,Z_cc_pu,type='Ynd11')
        
        Z_UG3_3w = abcn2abc(np.array(line_codes['UG3'])) 
