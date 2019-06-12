# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 11:22:35 2015

@author: jmmauricio
"""


import numpy as np
import xlrd
import pandas as pd

def losses(i_rms, m, fp, T_a, params):

    a_i = params['a_i']
    b_i = params['b_i']
    c_i = params['c_i']
    d_i = params['d_i']
    e_i = params['e_i']
    a_d = params['a_d']
    b_d = params['b_d']
    c_d = params['c_d']
    d_d = params['d_d']
    e_d = params['e_d']

    R_th_igbt =params['R_th_igbt']
    R_th_diode=params['R_th_diode']
    R_th_igbt_case=params['R_th_igbt_case']
    R_th_diode_case=params['R_th_diode_case']
    R_th_sink =params['R_th_sink']
    
    
    p_igbt  = a_i + (b_i - c_i*m*fp)*i_rms + (d_i - e_i*m*fp)*i_rms*i_rms
    p_diode = a_d + (b_d - c_d*m*fp)*i_rms + (d_d - e_d*m*fp)*i_rms*i_rms
    
    p_switch = p_igbt + p_diode
    
    T_sink       = T_a          + p_switch*R_th_sink;
    T_case_igbt  = T_sink       + p_igbt *R_th_igbt_case; 
    T_case_diode = T_sink       + p_diode*R_th_diode_case;
    T_igbt       = T_case_igbt  + p_igbt *R_th_igbt;
    T_diode      = T_case_diode + p_diode*R_th_diode;
    
    #print(R_th_igbt,R_th_igbt_case,T_case_igbt,T_sink)
    
    powers = dict(p_igbt=p_igbt,
                  p_diode=p_diode)
                  
    temperatures = dict(T_igbt=T_igbt,
                        T_diode=T_diode,
                        T_case_igbt=T_case_igbt,
                        T_case_diode=T_case_diode,
                        T_sink=T_sink,
                        T_igbt_deg=T_igbt-273.15,
                        T_diode_deg=T_diode-273.15,
                        T_sink_deg=T_sink-273.15)    
                        
    return powers, temperatures 
  
def vscthmodel(i_rms, m, fp, T_a, params):

    a_i = params['a_i']
    b_i = params['b_i']
    c_i = params['c_i']
    d_i = params['d_i']
    e_i = params['e_i']
    a_d = params['a_d']
    b_d = params['b_d']
    c_d = params['c_d']
    d_d = params['d_d']
    e_d = params['e_d']


    R_th_igbt_sink=params['R_th_igbt_sink']
    R_th_diode_sink=params['R_th_diode_sink']
    R_th_sink_a =params['R_th_sink_a']
    
    
    p_igbt  = a_i + (b_i - c_i*m*fp)*i_rms + (d_i - e_i*m*fp)*i_rms*i_rms
    p_diode = a_d + (b_d - c_d*m*fp)*i_rms + (d_d - e_d*m*fp)*i_rms*i_rms
    
    p_switch = p_igbt + p_diode
    
    T_sink       = T_a          + p_switch*R_th_sink_a
    T_igbt  = T_sink       + p_igbt *R_th_igbt_sink
    T_diode = T_sink       + p_diode*R_th_diode_sink

    
    #print(R_th_igbt,R_th_igbt_case,T_case_igbt,T_sink)
    
    powers = dict(p_igbt=p_igbt,
                  p_diode=p_diode)
                  
    temperatures = dict(T_igbt=T_igbt,
                        T_diode=T_diode,
                        T_sink=T_sink,
                        T_igbt_deg=T_igbt ,
                        T_diode_deg=T_diode ,
                        T_sink_deg=T_sink)    
                        
    return powers, temperatures   

def man2param_1(man_electric, man_thermal):
    '''
    
    Input
    -----
    
    List of 5 tuples
    
   [
   [i_1,m_1,cosphi_1,p_igbt_1,p_diode_1],
   [i_2,m_1,cosphi_1,p_igbt_2,p_diode_2],
   [i_3,m_1,cosphi_1,p_igbt_3,p_diode_3],
   [i_4,m_2,cosphi_2,p_igbt_4,p_diode_4],
   [i_5,m_2,cosphi_2,p_igbt_5,p_diode_5]
   ]




    '''
    
    k2deg = 273.15
    
    i_1 = man_electric[0][0]
    i_2 = man_electric[1][0]
    i_3 = man_electric[2][0]
    i_4 = man_electric[3][0]
    i_5 = man_electric[4][0]
    
    
    p_igbt_1 = man_electric[0][3]
    p_igbt_2 = man_electric[1][3]
    p_igbt_3 = man_electric[2][3]
    p_igbt_4 = man_electric[3][3]
    p_igbt_5 = man_electric[4][3]
    
    p_diode_1 = man_electric[0][4]
    p_diode_2 = man_electric[1][4]
    p_diode_3 = man_electric[2][4]
    p_diode_4 = man_electric[3][4]
    p_diode_5 = man_electric[4][4]
    
    
    m_1 = man_electric[0][1]
    m_2 = man_electric[1][1]
    m_3 = man_electric[2][1]
    m_4 = man_electric[3][1]
    m_5 = man_electric[4][1]
    
    cosphi_1 = man_electric[0][2]
    cosphi_2 = man_electric[1][2]
    cosphi_3 = man_electric[2][2]
    cosphi_4 = man_electric[3][2]
    cosphi_5 = man_electric[4][2]
    
    alpha_1 = m_1*cosphi_1
    alpha_2 = m_2*cosphi_2
    alpha_3 = m_3*cosphi_3
    alpha_4 = m_4*cosphi_4
    alpha_5 = m_5*cosphi_5
        
    A = np.array(
    [
    [1,  i_1,  -i_1*alpha_1,  i_1**2, -i_1**2*alpha_1],
    [1,  i_2,  -i_2*alpha_2,  i_2**2, -i_2**2*alpha_2],
    [1,  i_3,  -i_3*alpha_3,  i_3**2, -i_3**2*alpha_3],
    [1,  i_4,  -i_4*alpha_4,  i_4**2, -i_4**2*alpha_4],
    [1,  i_5,  -i_5*alpha_5,  i_5**2, -i_5**2*alpha_5]
    ]
    )
    
    print(A)
    
    b_igbt = np.array(
    [
    [p_igbt_1],
    [p_igbt_2],
    [p_igbt_3],
    [p_igbt_4],
    [p_igbt_5]
    ]
    ) 
    
    
    
    x = np.linalg.solve(A, b_igbt)
    
    a_i  = x[0]
    b_i = x[1]
    c_i = x[2]
    d_i = x[3]
    e_i = x[4]
    
    
    b_diode = np.array(
    [
    [p_diode_1],
    [p_diode_2],
    [p_diode_3],
    [p_diode_4],
    [p_diode_5]
    ]
    ) 
    
    
    x = np.linalg.solve(A, b_diode)
    
    a_d   = x[0]
    b_d = x[1]
    c_d = x[2]
    d_d = x[3]
    e_d = x[4]
    
    
    
    points=[
            [1, i_1,m_1,cosphi_1,alpha_1,p_igbt_1,p_diode_1],
            [2, i_2,m_2,cosphi_2,alpha_2,p_igbt_2,p_diode_2],
            [3, i_3,m_3,cosphi_3,alpha_3,p_igbt_3,p_diode_3],
            [4, i_4,m_4,cosphi_4,alpha_4,p_igbt_4,p_diode_4],
            [5, i_5,m_5,cosphi_5,alpha_5,p_igbt_5,p_diode_5]
            ]
    
    
    # man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a+k2deg]]
    idx = 0
    p_igbt   = man_thermal[idx][0]
    p_diode  = man_thermal[idx][1]
    
    T_igbt   = man_thermal[idx][2]
    T_diode  = man_thermal[idx][3]
    T_sink   = man_thermal[idx][4]
    T_a      = man_thermal[idx][5]
    
    p_switch = p_igbt + p_diode   
    
    R_th_igbt_sink = (T_igbt-T_sink)/p_igbt
    
    R_th_sink_a = (T_sink-(T_a))/p_switch
    
    idx = 0
    p_diode = man_thermal[idx][1]
    T_diode  = man_thermal[idx][3]
    T_sink   = man_thermal[idx][4]
    R_th_diode_sink = (T_diode-T_sink)/p_diode
    
#    print(tabulate(points,tablefmt='latex'))
    
    params = dict(
    a_i = a_i,
    b_i = b_i,
    c_i = c_i,
    d_i = d_i,
    e_i = e_i,
    a_d = a_d,
    b_d = b_d,
    c_d = c_d,
    d_d = d_d,
    e_d = e_d,
    R_th_igbt_sink = R_th_igbt_sink,
    R_th_diode_sink = R_th_diode_sink,    
    R_th_sink_a = R_th_sink_a,   
    )
    
    return params 
  

def man2param(man_data, validation=False):
    '''
    
    Input
    -----
    
    List of dictionaries, each dictionary with the following information:
    
     {'i': 29.0,'m':1.0,'cosphi':1.0,'p_i': 27.0,'p_d':6.99,'T_i': 54.0,'T_d': 51.0, 'T_c': 49.0, 'T_s':46.0, 'T_a':40.0 }
   
    'i' : RMS current (A)
    'm' : Modulator peak value (pu)
    'cosphi' : Power factor (-)
    'p_i' : IGBT power loss (W)
    'p_d' : Diode power loss (W)
    'T_i' : IGBT junture temperature (Celcius degrees)
    'T_d' : Diode junture temperature (Celcius degrees)  
    'T_c' : Case temperature (Celcius degrees)  
    'T_s' : Heatsink temperature (Celcius degrees) 
    'T_a' : Ambient temperature (Celcius degrees) 
    'Tau_h' : Sink temperature time constant (s)
    '''
    
    k2deg = 273.15
    
    N = len(man_data)
    A = np.zeros((N,5))
    b_i = np.zeros((N,1))
    b_d = np.zeros((N,1))

    A_th = np.zeros((N,5))    

    R_th_igbt_sink_k = 0.0
    R_th_sink_a_k = 0.0
    R_th_diode_sink_k = 0.0

    k = 0
    k_th = 0.0
    for item in man_data:

        i_k = item['i']
        m_k = item['m']  
        cosphi_k = item['cosphi'] 
        alpha_k = m_k*cosphi_k

        p_i_k = item['p_i']  
        p_d_k = item['p_d']

        A[k,:] = np.array([1,  i_k,  -i_k*alpha_k,  i_k**2, -i_k**2*alpha_k])
        b_i[k,:] = np.array([p_i_k])
        b_d[k,:] = np.array([p_d_k]) 

        k += 1   

        if 'T_i' in item:
            T_i = item['T_i']
            T_d = item['T_d']
            T_c = item['T_c']
            T_s = item['T_s']
            T_a = item['T_a']

            p_switch_k = p_i_k + p_d_k   

            R_th_igbt_sink_k += (T_i-T_s)/p_i_k
            R_th_sink_a_k += (T_s-(T_a))/p_switch_k
            R_th_diode_sink_k += (T_d-T_s)/p_d_k

            k_th += 1.0


    R_th_igbt_sink = R_th_igbt_sink_k/k_th
    R_th_sink_a = R_th_sink_a_k/k_th
    R_th_diode_sink = R_th_diode_sink_k/k_th


   # x_i = np.linalg.solve(A, b_i)
   # x_d = np.linalg.solve(A, b_d)

    x_i = np.linalg.lstsq(A, b_i, rcond=None)[0]
    x_d = np.linalg.lstsq(A, b_d, rcond=None)[0]

    params = dict(
    a_i = x_i[0],
    b_i = x_i[1],
    c_i = x_i[2],
    d_i = x_i[3],
    e_i = x_i[4],
    a_d = x_d[0],
    b_d = x_d[1],
    c_d = x_d[2],
    d_d = x_d[3],
    e_d = x_d[4],
    R_th_igbt_sink = R_th_igbt_sink,
    R_th_diode_sink = R_th_diode_sink,    
    R_th_sink_a = R_th_sink_a,   
    )

    if validation:
        for item in man_data:
            i_rms = item['i']
            m = item['m']  
            cosphi = item['cosphi'] 
            T_a = item['T_a'] 
            powers, temperatures  = vscthmodel(i_rms, m, cosphi, T_a, params)
            p_i_k, p_d_k, T_i_k, T_d_k, T_s_k =  float(item['p_i']),float(item['p_d']),float(item['T_i']),float(item['T_d']),float(item['T_s'])
            p_i, p_d, T_i, T_d, T_s =  float(powers['p_igbt']),float(powers['p_diode']),float(temperatures['T_igbt']),float(temperatures['T_diode']),float(temperatures['T_sink'])
            print(f'{p_i_k:0.2f}, {p_d_k:0.2f}, {T_i_k:0.2f}, {T_d_k:0.2f}, {T_s_k:0.2f}')
            print(f'{p_i:0.2f}, {p_d:0.2f}, {T_i:0.2f}, {T_d:0.2f}, {T_s:0.2f}')
            eps_pi = (p_i_k - p_i)/p_i_k*100.0
            eps_pd = (p_d_k - p_d)/p_d_k*100.0
            eps_ti = (T_i_k - T_i)/T_i_k*100.0
            eps_td = (T_d_k - T_d)/T_d_k*100.0
            eps_ts = (T_s_k - T_s)/T_s_k*100.0
            print(f'{eps_pi:<0.2f}%, {eps_pd:0.2f}%, {eps_ti:0.2f}%, {eps_td:0.2f}%, {eps_ts:0.2f}%')
            print(f'-------------------------------------------------------------------------------')
    return params 

    # powers = dict(p_igbt=p_igbt,
    #               p_diode=p_diode)
                  
    # temperatures = dict(T_igbt=T_igbt,
    #                     T_diode=T_diode,
    #                     T_sink=T_sink,
    #                     T_igbt_deg=T_igbt ,
    #                     T_diode_deg=T_diode ,
    #                     T_sink_deg=T_sink)    

def semisel_xls(file,shs_for_param, shs_for_validate, T_a_deg):
    k2deg = 273.15
    
    wb = xlrd.open_workbook(file)
    man_electric = []
    man_thermal  = []
      
    for sh_num in shs_for_param:        
        sh = wb.sheet_by_index(sh_num)
        
        V_dc  = float(sh.cell_value(0,1).split(' ')[0])
        V_ac  = float(sh.cell_value(1,1).split(' ')[0])
        i_rms = float(sh.cell_value(2,1).split(' ')[0])
        freq  = float(sh.cell_value(4,1).split(' ')[0])
        fp    = float(sh.cell_value(5,1))
        f_sw  = float(sh.cell_value(7,1).split(' ')[0])
        
        p_igbt  = float(sh.cell_value(15,1).split(' ')[0])
        p_diode = float(sh.cell_value(18,1).split(' ')[0])
        T_igbt  = float(sh.cell_value(23,1).split(' ')[0])        
        T_diode = float(sh.cell_value(24,1).split(' ')[0])
        T_sink= float(sh.cell_value(21,1).split(' ')[0])
        
        m = V_ac*np.sqrt(2)/V_dc
        
        man_electric += [[i_rms,m,fp,p_igbt,p_diode]]
        man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
        
        print('{} & {} & {} & {} & {} & {} & {}'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))

    params = man2param(man_electric,man_thermal)

    
    print('\midrule')
    for sh_num in shs_for_validate:        
        sh = wb.sheet_by_index(sh_num)
        
        V_dc  = float(sh.cell_value(0,1).split(' ')[0])
        V_ac  = float(sh.cell_value(1,1).split(' ')[0])
        i_rms = float(sh.cell_value(2,1).split(' ')[0])
        freq  = float(sh.cell_value(4,1).split(' ')[0])
        fp    = float(sh.cell_value(5,1))
        f_sw  = float(sh.cell_value(7,1).split(' ')[0])
        
        p_igbt  = float(sh.cell_value(15,1).split(' ')[0])
        p_diode = float(sh.cell_value(18,1).split(' ')[0])
        T_igbt  = float(sh.cell_value(23,1).split(' ')[0])        
        T_diode = float(sh.cell_value(24,1).split(' ')[0])
        T_sink= float(sh.cell_value(21,1).split(' ')[0])
        
        m = V_ac*np.sqrt(2)/V_dc
        
        pows, temps    = vscthmodel(i_rms, m, fp, T_a_deg, params)


        print('{:2.1f} & {:2.2f} & {:2.1f} & {:2.1f}  & {:2.1f} & {:2.1f}   & {:2.1f} & {:2.1f}  & {:2.1f} & {:2.1f}   & {:2.1f} & {:2.1f} \\\\  '.format(i_rms, 
                                                                                                          fp,
                                                                                                          p_igbt, pows['p_igbt'][0], 
                                                                                                          p_diode, pows['p_diode'][0], 
                                                                                                          T_igbt, temps['T_igbt_deg'][0],
                                                                                                          T_diode, temps['T_diode_deg'][0],
                                                                                                          T_sink, temps['T_sink_deg'][0],



))
        
        
    
    return params
    
  

def imposim_xls(file):
    k2deg = 273.15
    
    wb = xlrd.open_workbook(file)
    man_electric = []
    man_thermal  = []
     
           
    sh = wb.sheet_by_index(0)
    
    V_dc  = float(sh.cell_value(20,3))
    m     = float(sh.cell_value(26,3))

    idx = 9  
    
    T_a_deg = float(sh.cell_value(idx+53,9))  
    
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6))+ 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11)) + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9)) 
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]]
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))
    
    idx = 13  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6))+ 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11))+ 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))   
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]]    
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))

 
    idx = 16  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6)) + 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11))  + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))    
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]] 
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))
        
    sh = wb.sheet_by_index(1)
    m     = float(sh.cell_value(26,3))
       
    idx = 13  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6))    + 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11))   + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]]    
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))

    idx = 16  
    i_rms   = float(sh.cell_value(idx,0))
    m       = float(sh.cell_value(26,3))
    fp      = float(sh.cell_value(27,3))  
    p_igbt  = float(sh.cell_value(idx,6)) + 0.5*float(sh.cell_value(idx,13))  
    p_diode = float(sh.cell_value(idx,11)) + 0.5*float(sh.cell_value(idx,13))  
    T_igbt  = float(sh.cell_value(idx+34,10))
    T_diode = float(sh.cell_value(idx+52,10))   
    T_sink = float(sh.cell_value(idx+52,8)) + float(sh.cell_value(idx+53,9))
    man_electric += [[i_rms,m,fp,p_igbt,p_diode]] 
    man_thermal += [[p_igbt,p_diode,T_igbt+k2deg,T_diode+k2deg,T_sink+k2deg,T_a_deg+k2deg]]
    print('{:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} & {:2.1f} \\\\'.format(i_rms, fp, p_igbt, p_diode, T_igbt, T_diode, T_sink))
    
    
    print(np.array(man_electric))
    params = man2param(man_electric,man_thermal)

def imposim2xls(file):
    k2deg = 273.15
    
    df_1 = pd.read_excel(file, sheetname=0, skiprows=8)
    df_2 = pd.read_excel(file, sheetname=1, skiprows=8)
    print(df_1)

    idx1 = 3
    idx2 = 10
    idx3 = 16
    
    man_electric = [
                   [df_1.i_rms[idx1],df_1.m[idx1],df_1.fp[idx1],df_1.p_igbt[idx1],df_1.p_diode[idx1]],
                   [df_1.i_rms[idx2],df_1.m[idx2],df_1.fp[idx2],df_1.p_igbt[idx2],df_1.p_diode[idx2]],
                   [df_1.i_rms[idx3],df_1.m[idx3],df_1.fp[idx3],df_1.p_igbt[idx3],df_1.p_diode[idx3]],
                   [df_2.i_rms[idx2],df_2.m[idx2],df_2.fp[idx2],df_2.p_igbt[idx2],df_2.p_diode[idx2]],
                   [df_2.i_rms[idx3],df_2.m[idx3],df_2.fp[idx3],df_2.p_igbt[idx3],df_2.p_diode[idx3]],
                   ]    
                    
    man_thermal = [
                  [df_1.p_igbt[idx2],df_1.p_diode[idx2],df_1.T_igbt[idx2]+k2deg,df_1.T_diode[idx2]+k2deg,df_1.T_sink[idx2]+k2deg,df_1.T_a[idx2]+k2deg],
                  ]
    
    params =  man2param(man_electric, man_thermal)
    
    return params
    
    
    
    
if __name__ == '__main__':
    k2deg = 273.15
    file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/ARTICLES/doing/vsc_model/code/semikron_100kva/semikron_SKiiP38GB12E4V1.xls'
#    shs_for_param = [0,2,4,5,6] 
#    shs_for_validate = [7,8,9,10]    
#    T_a_deg = 40.0+k2deg
#    params = semisel_xls(file,shs_for_param, shs_for_validate, T_a_deg)    
#
#    print(params)
    file = '/home/jmmauricio/Documents/public/jmmauricio6/RESEARCH/ARTICLES/doing/vsc_model/code/imposim/imposim_F800R17.xls'
    params = imposim2xls(file)
    print(params)


    
    T_a = 40+ k2deg
    R_th_diode_sink = params['R_th_diode_sink']
    R_th_igbt_sink = params['R_th_igbt_sink']
    R_th_sink_a = params['R_th_sink_a']
    a_d = params['a_d']
    a_i = params['a_i']
    b_d = params['b_d']
    b_i = params['b_i']
    c_d = params['c_d']
    c_i = params['c_i']
    d_d = params['d_d']
    d_i = params['d_i']
    e_d = params['e_d']
    e_i = params['e_i']

    
    i_rms = 520

    m = 400*np.sqrt(2)/800
    fp =  1.0
    p_igbt  = 1.000*(a_i + (b_i - c_i*m*fp)*i_rms + (d_i - e_i*m*fp)*i_rms*i_rms)
    p_diode = 1.000*(a_d + (b_d - c_d*m*fp)*i_rms + (d_d - e_d*m*fp)*i_rms*i_rms)
     
    p_switch = p_igbt + p_diode + i_rms**2*0.000
    
    print('p_igbt',p_igbt)
    print('p_diode',p_diode)
    print('p_switch', p_switch)
    T_sink_0       = T_a    + p_switch*R_th_sink_a;
    T_igbt_0       = T_sink_0 + p_igbt *R_th_igbt_sink;
    T_diode_0      = T_sink_0 + p_diode*R_th_diode_sink;

    print('T_sink_0', T_sink_0-k2deg)
    print('T_igbt_0', T_igbt_0-k2deg)
    print('T_diode_0', T_diode_0-k2deg)
#    
##    C_th_diode= 10
##    C_th_diode_case= 2
##    C_th_igbt= 18
##    C_th_igbt_case= 5
##    C_th_sink= 6000.0
##    R_th_diode= 0.01979045401629802
##    R_th_diode_case= 0.018
##    R_th_igbt= 0.009765625
##    R_th_igbt_case= 0.009
##    R_th_sink= 0.007
##    a_d = 143.48507451
##    a_i = 421.02132341
##    b_d = 0.589627
##    b_i = 0.55708434
##    c_d = 0.18337165
##    c_i =-0.12254324
##    d_d = 0.00026235
##    d_i = 0.00089385
##    e_d = 0.00021407
##    e_i =-0.00041411
##    T_a = 35.0+273
##    params ={'C_th_diode': C_th_diode,
##     'C_th_diode_case': C_th_diode_case,
##     'C_th_igbt': C_th_igbt,
##     'C_th_igbt_case': C_th_igbt_case,
##     'C_th_sink': C_th_sink,
##     'R_th_diode': R_th_diode,
##     'R_th_diode_case': R_th_diode_case,
##     'R_th_igbt': R_th_igbt,
##     'R_th_igbt_case':R_th_igbt_case,
##     'R_th_sink': R_th_sink,
##     'a_d':  a_d,
##     'a_i':  a_i,
##     'b_d':  b_d,
##     'b_i':  b_i,
##     'c_d':  c_d,
##     'c_i':  c_i,
##     'd_d':  d_d,
##     'd_i':  d_i,
##     'e_d':  e_d,
##     'e_i':  e_i,
##     'm':0.85,
##     'fp':0.8,
##     'i_rms':1400,
##      'T_a':35+273.3,       
##            }
##            
##    
##    i_rms = 1500
##    fp = 0.85
##    m = 0.8
##    pows, temps = losses(i_rms, m, fp, T_a, params)
##    print(pows)
##    print(temps)