
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 13:04:45 2017

@author: jmmauricio
"""

import numpy as np 


def new_line_code(data,line_code,line,Freq):

    Z = []
    Y = np.array([])

    alpha = np.exp(2.0/3*np.pi*1j)
    A_0a =  np.array([[1, 1, 1],
                        [1, alpha**2, alpha],
                        [1, alpha, alpha**2]])

    A_a0 = 1/3* np.array([[1, 1, 1],
                            [1, alpha, alpha**2],
                            [1, alpha**2, alpha]])
                  
    line_data = data['line_codes'][line_code]
    if 'X1' in line_data:  data_type='ZR1X1'
    if 'C_1_muF' in line_data:  data_type='PIR1X1C1'
    if 'R' in line_data:  data_type='ZRX'  
    if 'X' in line_data:  data_type='ZRX'      
    if 'B_mu' in line_data:  data_type='PIRXC'
    if 'B1_mu' in line_data:  data_type='PIR1X1B1mu'  
    if 'Rph' in line_data:  data_type='ZRphXph'
    if 'Rn' in line_data:  data_type='ZRphXphRnXn'  
    if 'rho_20_m' in line_data:  data_type='ZrhoX'  
    if 'GMR' in line_data:  data_type='GMR'  
    if 'u90_pf08' in line_data:  data_type='RX90pf'  # like in manufacturer catalog
    #if 'u70_pf08' in line_data:  data_type='RX70pf'  # like in manufacturer catalog
    
    if data_type in ['ZR1X1', 'ZRX', 'ZRphXph','ZrhoX' ,'RX90pf'  ]:
        line['type'] = 'z'
    if data_type in ['PIR1X1C1', 'PIRXC','PIR1X1B1mu'  ]:
        line['type'] = 'pi'                    

    lenght_convertion = 1.0
    if "unit" in data['line_codes'][line_code]: 
        if  data['line_codes'][line_code]['unit']  == 'miles': lenght_convertion = 1.0/1.60934
    if "units" in data['line_codes'][line_code]: 
        if  data['line_codes'][line_code]['units'] == 'miles': lenght_convertion = 1.0/1.60934

    if data_type=='GMR':
        line['type'] = 'z'

        if 'type' in data['line_codes'][line_code]:
            line['type'] = data['line_codes'][line_code]['type']
        else:
            line['type'] = 'z'

        pos_x = data['line_codes'][line_code]['pos_x']
        pos_y = data['line_codes'][line_code]['pos_y']
        GMR   = data['line_codes'][line_code]['GMR']
        diam_c = 0.0
        R_cond = data['line_codes'][line_code]['R_cond']
        if 'rho_gnd' in data['line_codes'][line_code]:
            rho_gnd = data['line_codes'][line_code]['rho_gnd']
        else:
            rho_gnd = 100.0

        if 'freq' in data['line_codes'][line_code]:
            freq = data['line_codes'][line_code]['freq']
        else:
            freq = Freq


        Z = geom2z(pos_x,pos_y,GMR,diam_c,R_cond,rho_gnd,freq)


    if data_type=='ZR1X1':
        line['type'] = 'z'
        Z_1 = line_data['R1'] + 1j*line_data['X1']
        Z_2 = Z_1
        if 'X0' in line_data:
            Z_0 = line_data['R0'] + 1j*line_data['X0'] 
        else:
            Z_0 = 3*Z_1
        Z_012 = np.array([[Z_0,0,0],[0,Z_1,0],[0,0,Z_2]])
        Z = (A_a0 @ Z_012 @ A_0a)*lenght_convertion

    if data_type=='PIR1X1C1':
        line['type'] = 'pi'
        Z_1 = line_data['R1'] + 1j*line_data['X1']
        Z_2 = Z_1
        if 'X0' in line_data:
            Z_0 = line_data['R0'] + 1j*line_data['X0'] 
        else:
            Z_0 = 3*Z_1
        Z_012 = np.array([[Z_0,0,0],[0,Z_1,0],[0,0,Z_2]])
        Z = (A_a0 @ Z_012 @ A_0a)*lenght_convertion
        C_km = line_data['C_1_muF']*1e-6 
        B_1 = -1j*2*np.pi*Freq*C_km
        B_2 = B_1
        if 'C_0_muF' in line_data:
            B_0 =  -1j*2*np.pi*Freq*line_data['C_0_muF']*1e-6
        else:
            B_0 =  3.0*B_1                  

        Y_012 = np.array([[B_0,0,0],[0,B_1,0],[0,0,B_2]])
        Y = (A_a0 @ Y_012 @ A_0a)*lenght_convertion
        
    if data_type=='PIR1X1B1mu':
        line['type'] = 'pi'
        Z_1 = line_data['R1'] + 1j*line_data['X1']
        Z_2 = Z_1
        if 'X0' in line_data:
            Z_0 = line_data['R0'] + 1j*line_data['X0'] 
        else:
            Z_0 = 3*Z_1
            
        B_1 = line_data['B1_mu'] /1.0e6
        B_2 = B_1
        if 'B0_mu' in line_data:
            B_0 = line_data['B0_mu']/1.0e6
        else:
            B_0 = B_1
            
        Z_012 = np.array([[Z_0,0,0],[0,Z_1,0],[0,0,Z_2]])
        Z = (A_a0 @ Z_012 @ A_0a)*lenght_convertion
    
        Y_012 = np.array([[B_0,0,0],[0,B_1,0],[0,0,B_2]])
        Y = (A_a0 @ Y_012 @ A_0a)*lenght_convertion
        
        
    if data_type=='ZRX':
        line['type'] = 'z'
        R = np.array(data['line_codes'][line_code]['R'])
        X = np.array(data['line_codes'][line_code]['X'])
        Z = (R + 1j*X)*lenght_convertion

    if data_type=='PIRXC':
        
        line['type'] = 'pi'

        R = np.array(data['line_codes'][line_code]['R'])
        X = np.array(data['line_codes'][line_code]['X'])

        Z = (R + 1j*X)*lenght_convertion              
        Y = -1j*np.array(data['line_codes'][line_code]['B_mu'])*1e-6*lenght_convertion


    if data_type == 'ZRphXphRnXn':
        line['type'] = 'z'
        R_ph = np.array(data['line_codes'][line_code]['Rph'])*lenght_convertion
        X_ph = np.array(data['line_codes'][line_code]['Xph'])*lenght_convertion
        R_n = np.array(data['line_codes'][line_code]['Rn'])*lenght_convertion
        X_n = np.array(data['line_codes'][line_code]['Xn'])*lenght_convertion
        Z = np.zeros((4,4),dtype=np.complex128)
        Z[0,0] = R_ph+1j*X_ph
        Z[1,1] = R_ph+1j*X_ph
        Z[2,2] = R_ph+1j*X_ph
        Z[3,3] = R_n+1j*X_n

    if data_type == 'ZrhoX':
        line['type'] = 'z'
        rho_20 = np.array(data['line_codes'][line_code]['rho_20_m'])*1000.0
        alpha = np.array(data['line_codes'][line_code]['alpha'])
        X_ph = np.array(data['line_codes'][line_code]['Xph'])
        T_deg = np.array(data['line_codes'][line_code]['T_deg'])
        section = np.array(data['line_codes'][line_code]['section'])
        
        R_ph_20  = rho_20/section  # resistance per km at 20ºC
        DT = T_deg-20.0                      # temperature increment
        R_ph  = R_ph_20*(1.0+alpha*DT) # resistance per km at  90ºC
        R_n = R_ph
        X_n = X_ph
        Z = np.zeros((4,4),dtype=np.complex128)
        Z[0,0] = (R_ph+1j*X_ph)*lenght_convertion
        Z[1,1] = (R_ph+1j*X_ph)*lenght_convertion
        Z[2,2] = (R_ph+1j*X_ph)*lenght_convertion
        Z[3,3] = (R_n+1j*X_n)*lenght_convertion
                   

    if data_type == 'RX90pf':
        
        line['type'] = 'z'
        
        u90_pf08 = np.array(data['line_codes'][line_code]['u90_pf08'])
        u90_pf10 = np.array(data['line_codes'][line_code]['u90_pf10'])
        
        if 'T_deg' in data['line_codes'][line_code]: 
            T_deg = np.array(data['line_codes'][line_code]['T_deg'])
        else: T_deg = 90.0
        
        if 'alpha' in  data['line_codes'][line_code]: 
            alpha = np.array(data['line_codes'][line_code]['alpha'])
        else: alpha = 0.004

        # u = sqrt(3) * (r*cos(phi) + x*sin(phi))

        r90 = u90_pf10/np.sqrt(3)
        x90 = (u90_pf08/np.sqrt(3) - 0.8*r90)/0.6
        
        DT = T_deg-90.0 
        
        R_ph  = r90*(1.0+alpha*DT) # resistamce per km at  T_deg
        X_ph  = x90  

        R_n = R_ph
        X_n = X_ph
        Z = np.zeros((4,4),dtype=np.complex128)
        Z[0,0] = R_ph+1j*X_ph
        Z[1,1] = R_ph+1j*X_ph
        Z[2,2] = R_ph+1j*X_ph
        Z[3,3] = R_n+1j*X_n
           


    return Z,Y


def geom2z(pos_x,pos_y,GMR,diam_c,R,rho_gnd = 100.0,freq = 50.0):
    N_conductors = len(pos_x)
    R_earth =9.869e-4/1000.0*freq
    k_1 = 2e-4/1000.0 
    k_2 = 658.4 
    D_e = k_2*np.sqrt(rho_gnd/freq)


    Z = np.zeros((N_conductors,N_conductors))+0j

    for irow in range(N_conductors):
        for icol in range(N_conductors): 
            if irow == icol:
                Z[irow,icol] = R[irow]+ R_earth + 1j*2*np.pi*freq*k_1*np.log(D_e/GMR[irow])
            else:
                D_ij = ((pos_x[irow]-pos_x[icol])**2 + (pos_y[irow]-pos_y[icol])**2)**0.5
                Z[irow,icol] =  R_earth + 1j*2*np.pi*freq*k_1*np.log(D_e/D_ij)

    Z_km = Z*1000
    return Z_km



def get_line_codes():

    return {
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

def m4_to_seq(data,code):
    
    alpha = np.exp(2.0/3*np.pi*1j)
    A_0a =  np.array([[1, 1, 1],
                        [1, alpha**2, alpha],
                        [1, alpha, alpha**2]])

    A_a0 = 1/3* np.array([[1, 1, 1],
                            [1, alpha, alpha**2],
                            [1, alpha**2, alpha]])
    
    R = np.array(data["line_codes"][code]['R'])
    X = np.array(data["line_codes"][code]['X'])
    Z = R + 1j*X
    Z_pp = Z[0:3,0:3]
    Z_pn = Z[0:3,3].reshape(3,1)
    Z_np = Z[3,0:3].reshape(1,3)
    Z_nn = Z[3,3].reshape(1,1)
    Z_abc = Z_pp - Z_pn@np.linalg.inv(Z_nn)@Z_np
    Z_012 = A_0a@Z_abc@A_a0

    return Z_012










