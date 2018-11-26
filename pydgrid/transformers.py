
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 13:04:45 2017

@author: jmmauricio
"""

import numpy as np 
import difflib

def trafo_yprim(S_n,U_1n,U_2n,Z_cc,connection='Dyg11'):
    '''
    Trafo primitive as developed in: (in the paper Ynd11)
    R. C. Dugan and S. Santoso, “An example of 3-phase transformer modeling for distribution system analysis,” 
    2003 IEEE PES Transm. Distrib. Conf. Expo. (IEEE Cat. No.03CH37495), vol. 3, pp. 1028–1032, 2003. 
    
    '''

    connections_list = ['Dyn1', 'Yy_3wires','Dyn5','Dyn11','Ygd5_3w','Ygd1_3w','Ygd11_3w','ZigZag','Dyg11_3w','Ynd11']

    if connection not in connections_list:
        closest_connection = difflib.get_close_matches(connection, connections_list)
        print('Transformer connection "{:s}" not found, did you mean: "{:s}"?'.format(connection,closest_connection[0]))

    if connection=='Dyn1':
        z_a = 3*Z_cc*1.0**2/S_n
        z_b = 3*Z_cc*1.0**2/S_n
        z_c = 3*Z_cc*1.0**2/S_n
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

    if connection=='Yy_3wires':
        z_a = 3*Z_cc*1.0**2/S_n
        z_b = 3*Z_cc*1.0**2/S_n
        z_c = 3*Z_cc*1.0**2/S_n
        U_1 = U_1n/np.sqrt(3)
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
        A_trafo[0,0] = 1.0
        A_trafo[1,4] = 1.0
        A_trafo[2,8] = 1.0
        A_trafo[3,2] = 1.0
        A_trafo[4,6] = 1.0
        A_trafo[5,10] = 1.0


    if connection=='Dyn5':
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
        z_a = 3*Z_cc*1.0**2/S_n
        z_b = 3*Z_cc*1.0**2/S_n
        z_c = 3*Z_cc*1.0**2/S_n
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
        z_a = 3*Z_cc*1.0**2/S_n
        z_b = 3*Z_cc*1.0**2/S_n
        z_c = 3*Z_cc*1.0**2/S_n
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
        z_a = 3*Z_cc*1.0**2/S_n
        z_b = 3*Z_cc*1.0**2/S_n
        z_c = 3*Z_cc*1.0**2/S_n
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
        z_a = 3*Z_cc*1.0**2/S_n
        z_b = 3*Z_cc*1.0**2/S_n
        z_c = 3*Z_cc*1.0**2/S_n
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