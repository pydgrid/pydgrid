import numpy as np
import numba
class system(object):

    def __init__(self,json_file=None):

        self.N_x = 4
        self.N_y = 9
        dt_list = []
        struct_list = []
        dt_list += [('N_x',np.int32)]
        dt_list += [('N_y',np.int32)]
        struct_list += [4]
        struct_list += [9]
        dt_list += [('x',np.float64,(4,1))]
        dt_list += [('y',np.float64,(9,1))]
        dt_list += [('u',np.float64,(2,1))]
        struct_list += [np.zeros((4,1))]
        struct_list += [np.zeros((9,1))]
        struct_list += [np.zeros((2,1))]
        dt_list += [('f',np.float64,(4,1))]
        dt_list += [('g',np.float64,(9,1))]
        struct_list += [np.zeros((4,1))]
        struct_list += [np.zeros((9,1))]
        dt_list += [('F_x',np.float64,(4,4))]
        dt_list += [('F_y',np.float64,(4,9))]
        dt_list += [('G_x',np.float64,(9,4))]
        dt_list += [('G_y',np.float64,(9,9))]
        struct_list += [np.zeros((4,4))]
        struct_list += [np.zeros((4,9))]
        struct_list += [np.zeros((9,4))]
        struct_list += [np.zeros((9,9))]

        dt_list += [('T1q0',np.float64)]
        dt_list += [('X_d',np.float64)]
        dt_list += [('X_l',np.float64)]
        dt_list += [('G_t_inf',np.float64)]
        dt_list += [('Omega_b',np.float64)]
        dt_list += [('G_t0',np.float64)]
        dt_list += [('V_inf',np.float64)]
        dt_list += [('R_a',np.float64)]
        dt_list += [('X1q',np.float64)]
        dt_list += [('T1d0',np.float64)]
        dt_list += [('H',np.float64)]
        dt_list += [('B_t_inf',np.float64)]
        dt_list += [('theta_inf',np.float64)]
        dt_list += [('D',np.float64)]
        dt_list += [('X1d',np.float64)]
        dt_list += [('X_q',np.float64)]
        dt_list += [('B_t0',np.float64)]

        struct_list += [1.000000] # T1q0
        struct_list += [1.810000] # X_d
        struct_list += [0.150000] # X_l
        struct_list += [0.010000] # G_t_inf
        struct_list += [376.991118] # Omega_b
        struct_list += [0.100000] # G_t0
        struct_list += [0.900810] # V_inf
        struct_list += [0.003000] # R_a
        struct_list += [0.650000] # X1q
        struct_list += [8.000000] # T1d0
        struct_list += [3.500000] # H
        struct_list += [-2.104489] # B_t_inf
        struct_list += [0.000000] # theta_inf
        struct_list += [0.100000] # D
        struct_list += [0.300000] # X1d
        struct_list += [1.760000] # X_q
        struct_list += [0.000000] # B_t0
        self.struct = np.rec.array([struct_list],dtype=dt_list) 

    def ss(self,xi):

        x = xi[0:self.N_x]
        y = xi[self.N_x:(self.N_x+self.N_y)]
        self.struct['x'] = x
        self.struct['y'] = y
        update(self.struct,0,0)

        lam = np.vstack((self.struct['f'],self.struct['g']))
        return lam


@numba.jit(nopython=True, cache=True)
def update(struct,call,item):

    delta = struct[item]['x'][0,0]
    omega = struct[item]['x'][1,0]
    e1q = struct[item]['x'][2,0]
    e1d = struct[item]['x'][3,0]

    i_d = struct[item]['y'][0,0]
    i_q = struct[item]['y'][1,0]
    p_e = struct[item]['y'][2,0]
    v_d = struct[item]['y'][3,0]
    v_q = struct[item]['y'][4,0]
    p_m = struct[item]['y'][5,0]
    v_f = struct[item]['y'][6,0]
    theta_t = struct[item]['y'][7,0]
    Q_t = struct[item]['y'][8,0]

    P_t = struct[item]['u'][0,0]
    V_t = struct[item]['u'][1,0]

    T1q0 = struct[item]['T1q0']
    X_d = struct[item]['X_d']
    X_l = struct[item]['X_l']
    G_t_inf = struct[item]['G_t_inf']
    Omega_b = struct[item]['Omega_b']
    G_t0 = struct[item]['G_t0']
    V_inf = struct[item]['V_inf']
    R_a = struct[item]['R_a']
    X1q = struct[item]['X1q']
    T1d0 = struct[item]['T1d0']
    H = struct[item]['H']
    B_t_inf = struct[item]['B_t_inf']
    theta_inf = struct[item]['theta_inf']
    D = struct[item]['D']
    X1d = struct[item]['X1d']
    X_q = struct[item]['X_q']
    B_t0 = struct[item]['B_t0']

    ddelta = Omega_b*(omega - 1)
    domega = (-D*(omega - 1) - p_e + p_m)/(2*H)
    de1q = (-e1q - i_d*(-X1d + X_d) + v_f)/T1d0
    de1d = (-e1d + i_q*(-X1q + X_q))/T1q0

    struct[item]['f'][0,0] = ddelta 
    struct[item]['f'][1,0] = domega 
    struct[item]['f'][2,0] = de1q 
    struct[item]['f'][3,0] = de1d 




    g_0 = R_a*i_q - e1q + i_d*(X1d - X_l) + v_q
    g_1 = R_a*i_d - e1d - i_q*(X1q - X_l) + v_d
    g_2 = -i_d*(R_a*i_d + v_d) - i_q*(R_a*i_q + v_q) + p_e
    g_3 = -V_t*np.sin(delta - theta_t) + v_d
    g_4 = -V_t*np.cos(delta - theta_t) + v_q
    g_5 = -P_t + i_d*v_d + i_q*v_q
    g_6 = -Q_t + i_d*v_q - i_q*v_d
    g_7 = -P_t - V_inf*V_t*(-B_t_inf*np.sin(theta_inf - theta_t) + G_t_inf*np.cos(theta_inf - theta_t)) + V_t**2*(G_t0 + G_t_inf)
    g_8 = -Q_t - V_inf*V_t*(-B_t_inf*np.cos(theta_inf - theta_t) - G_t_inf*np.sin(theta_inf - theta_t)) - V_t**2*(B_t0 + B_t_inf)

    struct[item]['g'][0,0] = g_0 
    struct[item]['g'][1,0] = g_1 
    struct[item]['g'][2,0] = g_2 
    struct[item]['g'][3,0] = g_3 
    struct[item]['g'][4,0] = g_4 
    struct[item]['g'][5,0] = g_5 
    struct[item]['g'][6,0] = g_6 
    struct[item]['g'][7,0] = g_7 
    struct[item]['g'][8,0] = g_8 


    struct[item]['F_x'][0,1] = Omega_b 
    struct[item]['F_x'][1,1] = -D/(2*H) 
    struct[item]['F_x'][2,2] = -1/T1d0 
    struct[item]['F_x'][3,3] = -1/T1q0 

    struct[item]['F_y'][1,2] = -1/(2*H) 
    struct[item]['F_y'][1,5] = 1/(2*H) 
    struct[item]['F_y'][2,0] = (X1d - X_d)/T1d0 
    struct[item]['F_y'][2,6] = 1/T1d0 
    struct[item]['F_y'][3,1] = (-X1q + X_q)/T1q0 

    struct[item]['G_x'][0,2] = -1 
    struct[item]['G_x'][1,3] = -1 
    struct[item]['G_x'][3,0] = -V_t*np.cos(delta - theta_t) 
    struct[item]['G_x'][4,0] = V_t*np.sin(delta - theta_t) 

    struct[item]['G_y'][0,0] = X1d - X_l 
    struct[item]['G_y'][0,1] = R_a 
    struct[item]['G_y'][0,4] = 1 
    struct[item]['G_y'][1,0] = R_a 
    struct[item]['G_y'][1,1] = -X1q + X_l 
    struct[item]['G_y'][1,3] = 1 
    struct[item]['G_y'][2,0] = -2*R_a*i_d - v_d 
    struct[item]['G_y'][2,1] = -2*R_a*i_q - v_q 
    struct[item]['G_y'][2,2] = 1 
    struct[item]['G_y'][2,3] = -i_d 
    struct[item]['G_y'][2,4] = -i_q 
    struct[item]['G_y'][3,3] = 1 
    struct[item]['G_y'][3,7] = V_t*np.cos(delta - theta_t) 
    struct[item]['G_y'][4,4] = 1 
    struct[item]['G_y'][4,7] = -V_t*np.sin(delta - theta_t) 
    struct[item]['G_y'][5,0] = v_d 
    struct[item]['G_y'][5,1] = v_q 
    struct[item]['G_y'][5,3] = i_d 
    struct[item]['G_y'][5,4] = i_q 
    struct[item]['G_y'][6,0] = v_q 
    struct[item]['G_y'][6,1] = -v_d 
    struct[item]['G_y'][6,3] = -i_q 
    struct[item]['G_y'][6,4] = i_d 
    struct[item]['G_y'][6,8] = -1 
    struct[item]['G_y'][7,7] = -V_inf*V_t*(B_t_inf*np.cos(theta_inf - theta_t) + G_t_inf*np.sin(theta_inf - theta_t)) 
    struct[item]['G_y'][8,7] = -V_inf*V_t*(-B_t_inf*np.sin(theta_inf - theta_t) + G_t_inf*np.cos(theta_inf - theta_t)) 
    struct[item]['G_y'][8,8] = -1 
