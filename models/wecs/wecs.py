#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 08:59:45 2017

@author: jmmauricio
"""


import numpy as np
import numba
import matplotlib.pyplot as plt
import sympy as sym
#plt.style.use('presentation')

# [1] T. Demiray, F. Milano, and G. Andersson, 
# “Dynamic phasor modeling of the doubly-fed induction generator under unbalanced conditions,” 2007 IEEE Lausanne POWERTECH, Proc., no. 2, pp. 1049–1054, 2007.

@numba.jit(nopython=True, cache=True)
def dfim_alg_ctrl1(struct,i,m):
    '''
    Doubly Fed Induction Machine in with neglected dynamics and
    rotor side converter and control level 1 already implemented.
    i_rd = i_rd_ref and i_rq = i_rq_ref without dynamics 
    '''

    x_idx = struct[i]['dfim_idx']
    #psi_dr = float(struct[i]['x'][x_idx+0,0])
    #psi_qr = float(struct[i]['x'][x_idx+1,0])
    
    L_m = struct[i]['L_m']
    L_r = struct[i]['L_r']
    L_s = struct[i]['L_s']
    R_r = struct[i]['R_r']
    R_s = struct[i]['R_s']
    N_pp = struct[i]['N_pp']
    
    Dt  = struct[i]['Dt']
    
    i_dr_ref = struct[i]['i_dr_ref'] 
    i_qr_ref = struct[i]['i_qr_ref'] 
    
    i_dr = i_dr_ref
    i_qr = i_qr_ref

    v_ds = struct[i]['v_ds']
    v_qs = struct[i]['v_qs']
    
    omega_r = struct[i]['omega_r']
    omega_s = struct[i]['omega_s']
    
    sigma = (omega_s - omega_r)/omega_s

    den = R_s**2 + omega_s**2*(L_m + L_s)**2
    i_qs = (-L_m*R_s*i_dr*omega_s - L_m*i_qr*omega_s**2*(L_m + L_s) + R_s*v_qs - omega_s*v_ds*(L_m + L_s))/den
    i_ds = ( L_m*R_s*i_qr*omega_s - L_m*i_dr*omega_s**2*(L_m + L_s) + R_s*v_ds + omega_s*v_qs*(L_m + L_s))/den

    v_qr = R_r*i_qr + omega_s*sigma*(L_m*i_dr + L_m*i_ds + L_r*i_dr)
    v_dr = R_r*i_dr - omega_s*sigma*(L_m*i_qr + L_m*i_qs + L_r*i_qr)
    psi_dr = L_m*i_dr + L_m*i_ds + L_r*i_dr
    psi_qs = (R_s*i_ds - v_ds)/omega_s
    psi_ds = (-R_s*i_qs + v_qs)/omega_s
    psi_qr = L_m*i_qr + L_m*i_qs + L_r*i_qr

    tau_e  = 3.0/2.0*N_pp*(psi_qr*i_dr - psi_dr*i_qr)
   
    struct[i]['v_dr'] = v_dr
    struct[i]['v_qr'] = v_qr
    
    struct[i]['i_ds'] = i_ds
    struct[i]['i_qs'] = i_qs
    struct[i]['i_dr'] = i_dr
    struct[i]['i_qr'] = i_qr
 
    struct[i]['psi_ds'] = psi_ds
    struct[i]['psi_qs'] = psi_qs
    struct[i]['psi_dr'] = psi_dr
    struct[i]['psi_qr'] = psi_qr
    
    struct[i]['tau_e'] = tau_e
    struct[i]['sigma'] = sigma
    
    struct[i]['p_s'] = 3.0/2.0*(v_ds*i_ds + v_qs*i_qs)
    struct[i]['q_s'] = 3.0/2.0*(v_ds*i_qs - v_qs*i_ds)

    struct[i]['p_r'] = 3.0/2.0*(v_dr*i_dr + v_qr*i_qr)
    struct[i]['q_r'] = 3.0/2.0*(v_dr*i_qr - v_qr*i_dr)
    
    return tau_e


@numba.jit(nopython=True, cache=True)
def wecs_mech_1(struct,i,m):

    x_idx = struct[i]['mech_idx']
    omega_t = struct[i]['x'][x_idx,0]  # rad/s
    tau_t   = struct[i]['tau_t']
    tau_r   = struct[i]['tau_r']
       
    J_t  = struct[i]['J_t']
    N_tr = struct[i]['N_tr']
    Dt   = struct[i]['Dt']

    domega_t = 1.0/J_t*(tau_t - N_tr*tau_r)

    omega_r = N_tr*omega_t 
    
    struct[i]['f'][x_idx,0] = domega_t

    struct[i]['omega_r'] = omega_r
    struct[i]['omega_t'] = omega_t

    return omega_t


@numba.jit(nopython=True, cache=True)
def dfim_ctrl2(struct,i,m):
    '''
    Control level 2 for DFIM for stator active and reactive power.
    
    '''

    x_idx = struct[i]['ctrl2r_idx']
    xi_p_s = float(struct[i]['x'][x_idx+0,0])
    xi_q_s = float(struct[i]['x'][x_idx+1,0])    

    K_r_p = struct[i]['K_r_p']
    K_r_i = struct[i]['K_r_i']  
    
    p_s_ref = struct[i]['p_s_ref']
    q_s_ref = struct[i]['q_s_ref']  

    p_s = struct[i]['p_s']
    q_s = struct[i]['q_s']  
    
    S_b = struct[i]['S_b']
    
    omega_r = struct[i]['omega_r']
    omega_s = struct[i]['omega_s']  
    R_r = struct[i]['R_r']

    I_b = S_b/(np.sqrt(3)*690.0)
    sigma = (omega_s - omega_r)/omega_s
    
    error_p_s = (p_s_ref - p_s)/S_b
    error_q_s = (q_s_ref - q_s)/S_b 
    dxi_p_s = error_p_s
    dxi_q_s = error_q_s
    

    
    struct[i]['f'][x_idx+0,0] = dxi_p_s
    struct[i]['f'][x_idx+1,0] = dxi_q_s   

    struct[i]['i_dr_ref'] = -I_b*(K_r_p*error_p_s + K_r_i*xi_p_s) 
    struct[i]['i_qr_ref'] = -I_b*(K_r_p*error_q_s + K_r_i*xi_q_s)
    


    return struct[0]['i_dr_ref'],struct[0]['i_qr_ref']


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
            numbers += (d[item],)
            dtypes += [(item,np.float64,d[item].shape)]
    return np.array([numbers],dtype=dtypes)



Omega_b = 2.0*np.pi*50.0
S_b = 2.0e6
U_b = 690.0
Z_b = U_b**2/S_b
#nu_w =np.linspace(0.1,15,N)
H = 2.0
N_pp = 2
N_tr = 20
# H = 0.5*J*Omega_t_n**2/S_b
S_b = 2.0e6
Omega_t_n = Omega_b/N_pp/N_tr
J_t = 2*H*S_b/Omega_t_n**2


#Z_b = 1.0
#Omega_b = 1.0
d =dict(S_b = S_b,
        Omega_b = Omega_b,
        R_r = 0.01*Z_b,
        R_s = 0.01*Z_b,
        L_r = 0.08*Z_b/Omega_b,
        L_s = 0.1*Z_b/Omega_b,
        L_m = 3.0*Z_b/Omega_b,
        N_pp = N_pp,
        psi_ds = 0.0,
        psi_qs = 0.0,
        p_s = 0.0,
        q_s = 0.0,
        p_r = 0.0,
        q_r = 0.0,
        psi_dr = 0.0,
        psi_qr = 0.0,
        p_s_ref = 0.0,
        q_s_ref = 0.0,
        i_ds   = 0.0,
        i_qs   = 0.0,
        i_dr   = 0.0,
        i_qr   = 0.0,
        i_dr_ref   = 0.0,
        i_qr_ref   = 0.0,
        v_ds   = 0.0,
        v_qs   = 0.0,
        v_dr   = 0.0,
        v_qr   = 0.0,
        omega_r   = Omega_b/N_pp,
        omega_s   = Omega_b/N_pp,
        sigma   = 0.0,
        tau_e   = 0.0,        
        x = np.zeros((3,1)),
        f = np.zeros((3,1)),   
        Dt = 0.0,
        J_t = J_t,  
        omega_t = 0.0,  
        tau_t = 0.0,  
        tau_r = 0.0, 
        N_tr = N_tr, 
        K_r_p = 0.02,
        K_r_i = 20.0,
        dfim_idx = 0,
        mech_idx = 0,
        ctrl2r_idx = 1
        )


struct = d2np(d)
struct = np.hstack((struct[0],np.copy(struct[0])))

#wecs_mech_1(struct,0)


dfim_alg_ctrl1(struct,0,0)
dfim_ctrl2(struct,0,0)
dfim_alg_ctrl1(struct,1,0)
dfim_ctrl2(struct,1,0)
print(struct[0]['p_s']/1e6,struct[0]['q_s']/1e6,struct[0]['tau_e'])
print(struct[1]['p_s']/1e6,struct[0]['q_s']/1e6,struct[0]['tau_e'])



