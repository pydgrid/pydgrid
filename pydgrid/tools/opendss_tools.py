#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 13:04:45 2017

@author: jmmauricio
"""


def opendss2json(files):
        trafos_file = './Feeder_1/Transformers.txt'
        buses_file = './Feeder_1/buscoord.dss'
        linecodes_file = './Feeder_1/LineCode.txt'
        lines_file = './Feeder_1/Lines.txt'        
        loads_file = './Feeder_1/Loads.txt'
        load_shapes_file = './Feeder_1/LoadShapes.txt' 
        line_dict = {}
        
        buses = []
        
        ## Transformers
        
        fobj_trafos = open(trafos_file, 'r')
        trafos_list = [] 
        for trafo in fobj_trafos.readlines():
            item_odss = 'Buses=['
            start_idx = trafo.find(item_odss)
            end_idx = trafo.find(']',start_idx)
            value = trafo[((start_idx+len(item_odss))):end_idx]
            bus_j,bus_k = value.split(' ') 

            item_odss = 'Conns=['
            start_idx = trafo.find(item_odss)
            end_idx = trafo.find(']',start_idx)
            value = trafo[((start_idx+len(item_odss))):end_idx]
            conn_j,conn_k = value.split(' ') 
            
            item_odss = 'kVs=['
            start_idx = trafo.find(item_odss)
            end_idx = trafo.find(']',start_idx)
            value = trafo[((start_idx+len(item_odss))):end_idx]
            U_1_kV,U_2_kV = value.split(' ') 
                       
            item_odss = 'kVAs=['
            start_idx = trafo.find(item_odss)
            end_idx = trafo.find(']',start_idx)
            value = trafo[((start_idx+len(item_odss))):end_idx]
            S_n_kVA,S_n_kVA_2 = value.split(' ')

            item_odss = 'XHL='
            start_idx = trafo.find(item_odss)
            end_idx = trafo.find(']',start_idx)
            value = trafo[((start_idx+len(item_odss))):end_idx]
            X_pu= value
            
            if conn_j == 'Delta' and conn_k == 'Wye':
                connection = 'Dyg11_3w'
                trafo_dict = {"bus_j": bus_j,  "bus_k": bus_k,  "S_n_kVA": float(S_n_kVA), 
                              "U_1_kV":float(U_1_kV), "U_2_kV":float(U_2_kV), "R_cc_pu": float(0.0001), 
                              "X_cc_pu":float(X_pu)/100.0, "connection": "Dyg11_3w", "conductors_1":3, "conductors_2":3 }

   
            if not bus_j in buses:
                buses += [bus_j]
            if not bus_k in buses:
                buses += [bus_k]                
            trafos_list += [trafo_dict]                       
        
        ## Lines
        
        fobj_lines = open(lines_file, 'r')
        
        read_list = [('Bus1','bus_j','str',1),
                     ('Bus2','bus_k','str',1),
                     ('Linecode','code','str',1),
                     ('Length','m','float',1.0),
                     ('phases','N_conductors','int',1)]
        
        lines_list = []
        
        for line in fobj_lines.readlines():
            line_dict = {}
            for item_odss,item_py,tipo,scale in read_list:
                start_idx = line.find(item_odss + '=')
                end_idx = line.find(' ',start_idx)
                
                value = line[((start_idx+len(item_odss))+1):end_idx]
                if tipo=='float':
                    value = float(value)*scale
                if tipo=='int':
                    value = int(value)*scale               
                
                line_dict.update({item_py:value})
            
            bus_j = line_dict['bus_j']
            if not bus_j in buses:
                buses += [bus_j]
            bus_k = line_dict['bus_k']
            if not bus_k in buses:
                buses += [bus_k]                
            
            lines_list += [line_dict]    
            
            
        ## Loads
        loads_list = []
        load_dict = {}
        fobj_loads = open(loads_file, 'r')
        
        read_list = [('Phases','phases','int',1),
                     ('Bus1','bus','str',1),
                     ('kW','kW','float',1),
                     ('PF','fp','float',1.0),
                     ('Daily','shape','str',1)]
        
        load_list = []
        for load in fobj_loads.readlines():
            load_dict = {}
            for item_odss,item_py,tipo,scale in read_list:
                start_idx = load.find(item_odss + '=')
                end_idx = load.find(' ',start_idx)
                
                value = load[((start_idx+len(item_odss))+1):end_idx]
                if tipo=='float':
                    value = float(value)*scale
                if tipo=='int':
                    value = int(value)*scale               
                        
                if item_odss == 'Bus1':
                    if load_dict['phases'] == 1:
                        value,node = value.split('.') 
                        
                        load_dict.update({'bus_nodes':[int(node)],'type':'1P'})
                        
                load_dict.update({item_py:value})
            loads_list += [load_dict]

            bus = load_dict['bus']
            if not bus in buses:
                buses += [bus]

           

        ## Buses
        
        buses_list = []
        buses_array = np.genfromtxt(buses_file, delimiter=',', skip_header=1, dtype=[('nodes','S10'),('pos_x','f8'),('pos_y','f8')])   
          
        for bus in buses:
            idx = np.where(buses_array['nodes']==np.array(bus,dtype='S10'))[0].astype(np.int32)
            print(idx)
            pos_x = buses_array['pos_x'][idx]
            pos_y = buses_array['pos_y'][idx]
            buses_dict = {"bus": bus,  
                          "pos_x": float(pos_x), 
                          "pos_y": float(pos_y), 
                          "units": "m", 'U_kV':0.416}
            buses_list += [buses_dict]                        
            
        ## Line codes
        
        fobj_linecodes = open(linecodes_file, 'r')

        alpha = np.exp(2.0/3*np.pi*1j)
        Asym =  np.array([[1, 1, 1],
                          [1, alpha**2, alpha],
                          [1, alpha, alpha**2]])
        inv_Asym = np.linalg.inv(Asym)

        line_codes = {}
        for linecode in fobj_linecodes.readlines():
            item_odss = 'LineCode.'
            start_idx = linecode.find(item_odss)
            end_idx = linecode.find(' ',start_idx)
            linecode_id = linecode[((start_idx+len(item_odss))):end_idx]
            l = {}
            for item in ['R1','R0','X1','X0','C1','C0']:
                item_odss = item + '='
                start_idx = linecode.find(item_odss)
                end_idx = linecode.find(' ',start_idx)
                value = linecode[((start_idx+len(item_odss))):end_idx]
                l.update({item:float(value)})
            Z_012 = np.array([[l['R0']+1j*l['X0'],0,0],
                              [0,l['R1']+1j*l['X1'],0],
                              [0,0,l['R1']+1j*l['X1']]])
            Z_abc = inv_Asym @ Z_012 @ Asym
            
            line_codes.update({linecode_id:{'R':Z_abc.real.tolist(),
                                            'X':Z_abc.imag.tolist()}})
            json.dumps(line_codes)    
        
        grid_formers_list = [
		{"bus": "SourceBus","bus_nodes": [1, 2, 3], "deg": [0, -120, -240], "kV": [11.547, 11.547, 11.547]}]
        
        from collections import OrderedDict
        

 
    
        # Load Shapes
        fobj_loadshapes = open(load_shapes_file, 'r')    
        
        load_shapes_list = [] 
        for load_shape in fobj_loadshapes.readlines():
            item_odss = 'New Loadshape.'
            start_idx = load_shape.find(item_odss)
            end_idx = load_shape.find(' ',start_idx+4)
            shape_id = load_shape[((start_idx+len(item_odss))):end_idx]

            item_odss = 'npts='
            start_idx = load_shape.find(item_odss)
            end_idx = load_shape.find(' ',start_idx)
            npts = int(load_shape[((start_idx+len(item_odss))):end_idx])

            item_odss = 'interval='
            start_idx = load_shape.find(item_odss)
            end_idx = load_shape.find(' ',start_idx)
            interval = float(load_shape[((start_idx+len(item_odss))):end_idx])
            
            item_odss = 'mult=(file='
            start_idx = load_shape.find(item_odss)
            end_idx = load_shape.find(')',start_idx+4)
            shape_file = load_shape[((start_idx+len(item_odss))):end_idx]
            shape_file = shape_file.replace('\\','/')
            #fobj_shape = open(, 'r') 
            values = np.loadtxt(shape_file)
            t_s = np.linspace(0,npts*interval*3600,npts)
            load_shapes_list += [(shape_id,{'t_s':t_s.tolist(), 'shape':values.tolist()})] #, 't_s':t_s.tolist(), 'shape':values.tolist()}]
        dict_shapes = OrderedDict(load_shapes_list)

        out = json.dumps(dict_shapes) 
        out = out.replace('},','},\n')
        out = out.replace('],','],\n')
        fobj_out = open('load_shapes_list.json','w')
        fobj_out.write(out)
        fobj_out.close()
        
        
 
        data_dict = OrderedDict([('transformers',trafos_list),
                     ('lines',lines_list),
                     ('buses',buses_list),
                     ('grid_formers',grid_formers_list),
                     ('loads',loads_list),
                     ('line_codes',line_codes)])
        out = json.dumps(data_dict) 
        out = out.replace('},','},\n')
        out = out.replace('],','],\n')
        fobj_out = open('out.json','w')
        fobj_out.write(out)
        fobj_out.close()            
            
        json_data = open('out.json').read().replace("'",'"')
        data = json.loads(json_data)