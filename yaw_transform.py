import numpy as np
from stencils import interpol
from math import isclose

# THIS FUNCTION TAKES ONE CALIBRATIONS AND SHIFTS THE YAW COEFFICIENT TO BE ZERO AT ZERO YAW
def yaw_trans(c):

    # Finds minimum yaw coefficient by inspecting map at zero pitch 
    index = np.argmin(abs(c['C_Alpha'][0,0][:,int(len(c['C_Alpha'][0,0][0,:])/2)]))
    
    interp_check = 1
    if c['C_Alpha'][0,0][index,int(len(c['C_Alpha'][0,0][0,:])/2)]*c['C_Alpha'][0,0][index+1,int(len(c['C_Alpha'][0,0][0,:])/2)] < 0:
        index_1 = index + 1
    elif isclose(c['C_Alpha'][0,0][index,int(len(c['C_Alpha'][0,0][0,:])/2)],0.0, abs_tol = 1e-6): 
        interp_check = 0
    else: 
        index_1 = index - 1
    
    if interp_check == 1: 
        x = [c['C_Alpha'][0,0][index_1,int(len(c['C_Alpha'][0,0][0,:])/2)],c['C_Alpha'][0,0][index,int(len(c['C_Alpha'][0,0][0,:])/2)]]
        y = [c['Iota'][0,0][index_1,int(len(c['C_Alpha'][0,0][0,:])/2)],c['Iota'][0,0][index,int(len(c['C_Alpha'][0,0][0,:])/2)]]
        x_new = 0
        yaw = interpol(x_new, x, y)
    else:
        yaw = c['Iota'][0,0][index,int(len(c['C_Alpha'][0,0][0,:])/2)]

    c['Iota'][0,0] = c['Iota'][0,0] - yaw

    return c
