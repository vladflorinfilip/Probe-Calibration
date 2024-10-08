import numpy as np
from stencils import interpol

# THIS FUNCTION TAKES ONE CALIBRATIONS AND SHIFTS THE PITCH COEFFICIENT TO BE ZERO AT ZERO PITCH
def pitch_trans(c):

    # Finds minimum yaw coefficient by inspecting map at zero yaw
    index = np.argmin(abs(c['C_Beta'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),:]))
    
    interp_check = 1
    if c['C_Beta'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),index]*c['C_Beta'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),index+1] < 0:
        index_1 = index + 1
    elif c['C_Beta'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),index] == 0: 
        interp_check = 0
    else: 
        index_1 = index - 1
    
    if interp_check == 1: 
        x = [c['C_Beta'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),index_1],c['C_Beta'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),index]]
        y = [c['Tau'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),index_1],c['Tau'][0,0][int(len(c['C_Beta'][0,0][:,0])/2),index]]
        x_new = 0
        pitch = interpol(x_new, x, y)
    else:
        pitch = c['Tau'][0,0][int(len(c['C_Beta'][0,0][:,0])),index]

    c['Tau'][0,0] = c['Tau'][0,0] - pitch
    
    return c

# SIDE HOLE PROBE
def pitch_trans_side(c):

    # Find where side hole is closest (equal) to static pressure

    min = 1000

    for row in range(len(c['P_raw'][0,0][:,0,0,11])):
            for col in range(len(c['P_raw'][0,0][0,:,0,11])):
                
                if min >= abs(c['P_raw'][0,0][row,col,0,13] - c['P_raw'][0,0][row,col,0,1]) :
                    min = abs(c['P_raw'][0,0][row,col,0,13] - c['P_raw'][0,0][row,col,0,1])
                    pitch = c['Tau'][0,0][row,col]
    
    print(pitch)
    print(c['P_raw'][0,0][:,:,0,13])
    
    c['Tau'][0,0] = c['Tau'][0,0] - pitch

    return c