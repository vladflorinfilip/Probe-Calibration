# This function takes two sets of data and finds the error plots

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from stencils import interpol
from stencils import set_axes
from stencils import closest

# Function to get indecies for given angle
def ind(angle,c1,yes):

    if yes == 1:
    # Set window angles
        
        # Yaw
        yaw_angles = c1['Iota'][0,0][:,0].tolist()
        k = closest(yaw_angles,angle)
        if k <= angle:
            max_yaw = yaw_angles.index(k) + 2
        else:
            max_yaw = yaw_angles.index(k) + 1


        k = closest(yaw_angles,-angle) 
        if k >= -angle:
            min_yaw = yaw_angles.index(k) - 1
        else:
            min_yaw = yaw_angles.index(k)

        # Pitch
        pitch_angles = c1['Tau'][0,0][0,:].tolist()
        k = closest(pitch_angles,angle)  
        if k <= angle:
            max_pitch = pitch_angles.index(k) + 2
        else:
            max_pitch = pitch_angles.index(k) + 1
        k = closest(pitch_angles,-angle)
        if k >= -angle:
            min_pitch = pitch_angles.index(k) - 1
        else:
            min_pitch = pitch_angles.index(k)

    else: 
        max_yaw = np.size(c1['Iota'][0,0][:,0]-1)
        min_yaw = 0
        max_pitch = np.size(c1['Tau'][0,0][0,:]-1)
        min_pitch = 0

    return max_yaw, min_yaw, max_pitch, min_pitch

# Error function
# Calculates erros for yaw, pitch, static and stagnation coefficients
# for two dataset of the same length
def plot_error(c1,c2,type,angle=30):
    # REFERENCE is c1
    # TEST is c2

    # Initialise error vectors
    error_yaw = np.ones((len(c2['Iota'][0,0][:,0]),len(c2['Iota'][0,0][0,:])))
    error_pitch = np.ones((len(c2['Tau'][0,0][:,0]),len(c2['Tau'][0,0][0,:])))
    error_stat = np.ones((len(c2['C_P'][0,0][:,0]),len(c2['C_P'][0,0][0,:])))
    error_stag = np.ones((len(c2['C_Po'][0,0][:,0]),len(c2['C_Po'][0,0][0,:])))

    # Initialise dynamic head for nondimensionalisation
    rho = np.mean(c2['Pa'][0,0])/(np.mean(c2['Ta'][0,0])*287)
    dh = rho * 0.5 * 40**2

    # Calculate mean pressure
    P_mean = 0.25* (c2['P_raw'][0,0][:,:,0,11] + c2['P_raw'][0,0][:,:,0,12] + c2['P_raw'][0,0][:,:,0,13] + c2['P_raw'][0,0][:,:,0,15])

    # Yaw is row and pitch is collumns

    # Iterate over all data points of TEST
    # Read TEST yaw and pitch coefficients
    for row in range(len(c2['Iota'][0,0][:,0])):
        for col in range(len(c2['Tau'][0,0][0,:])):
            C_yaw = c2['C_Alpha'][0,0][row,col]
            C_pitch = c2['C_Beta'][0,0][row,col]

            # Iterate over the domain of c2, REFERENCE
            # Find upper and lower values for TEST pitch and yaw coefficinets
            # Set initial minimum 
            minimum = 1000

            # Find closest point
            for ref_row in range(len(c1['Iota'][0,0][:,0])):
                for ref_col in range(len(c2['Tau'][0,0][0,:])):
                    current = np.hypot(c1['C_Alpha'][0,0][ref_row,ref_col] - C_yaw, c1['C_Beta'][0,0][ref_row,ref_col] - C_pitch)
                    if current < minimum:
                            index_row_1 = ref_row
                            index_col_1 = ref_col
                            minimum = current

            # Find lower/upper limits
            if index_row_1 == len(c2['Iota'][0,0][:,0]) - 1: 
                index_row_2 = index_row_1 - 1
            elif index_row_1 == 0:
                index_row_2 = index_row_1 + 1
            elif (c1['C_Alpha'][0,0][index_row_1+1,index_col_1] < C_yaw < c1['C_Alpha'][0,0][index_row_1,index_col_1]) or \
                 (c1['C_Alpha'][0,0][index_row_1+1,index_col_1] > C_yaw > c1['C_Alpha'][0,0][index_row_1,index_col_1]) :
                index_row_2 = index_row_1 + 1
            else:
                index_row_2 = index_row_1 - 1 

            if index_col_1 == len(c2['Tau'][0,0][0,:]) - 1: 
                index_col_2 = index_col_1 - 1
            elif index_col_1 == 0:
                index_col_2 = index_col_1 + 1
            elif (c1['C_Beta'][0,0][index_row_1,index_col_1+1] < C_pitch < c1['C_Beta'][0,0][index_row_1,index_col_1]) or \
                 (c1['C_Beta'][0,0][index_row_1,index_col_1+1] > C_pitch > c1['C_Beta'][0,0][index_row_1,index_col_1]) :
                index_col_2 = index_col_1 + 1
            else:
                index_col_2 = index_col_1 - 1 

            # YAW Interpolation
            x = [c1['C_Alpha'][0,0][index_row_2,index_col_1],c1['C_Alpha'][0,0][index_row_1,index_col_1]]
            y = [c1['Iota'][0,0][index_row_2,index_col_1],c1['Iota'][0,0][index_row_1,index_col_1]]
            x_new = C_yaw
            yaw = interpol(x_new, x, y)

            # PITCH Interpolation
            x = [c1['C_Beta'][0,0][index_row_1,index_col_2],c1['C_Beta'][0,0][index_row_1,index_col_1]]
            y = [c1['Tau'][0,0][index_row_1,index_col_2],c1['Tau'][0,0][index_row_1,index_col_1]]
            x_new = C_pitch
            pitch = interpol(x_new, x, y)

            # Stagnation Pressure Interpolation
            x = [c1['Iota'][0,0][index_row_2,index_col_1],c1['Iota'][0,0][index_row_1,index_col_1]]
            y = [c1['C_Po'][0,0][index_row_2,index_col_1],c1['C_Po'][0,0][index_row_1,index_col_1]]
            x_new = yaw
            CP_1 = interpol(x_new, x, y)

            x = [c1['Iota'][0,0][index_row_2,index_col_2],c1['Iota'][0,0][index_row_1,index_col_2]]
            y = [c1['C_Po'][0,0][index_row_2,index_col_2],c1['C_Po'][0,0][index_row_1,index_col_2]]
            CP_2 = interpol(x_new, x, y)

            x = [c1['Tau'][0,0][index_row_1,index_col_1],c1['Tau'][0,0][index_row_1,index_col_2]]
            y = [CP_1,CP_2]
            x_new = pitch
            C_stag = interpol(x_new, x, y)

            # Calculate stagnation pressure error from interpolated coefficient
            if type == 0:
                Po_error = C_stag*(c2['P_raw'][0,0][:,:,0,11][row,col] - P_mean[row,col]) + c2['P_raw'][0,0][:,:,0,11][row,col]
            elif type == 1:
                P_avg_1 = min(c2['P_raw'][0,0][:,:,0,12][row,col],c2['P_raw'][0,0][:,:,0,13][row,col],c2['P_raw'][0,0][:,:,0,14][row,col],c2['P_raw'][0,0][:,:,0,15][row,col])
                Po_error = C_stag*(c2['P_raw'][0,0][:,:,0,11][row,col] - P_avg_1) + c2['P_raw'][0,0][:,:,0,11][row,col]
            elif type == 2:
                P_avg_2 = 0.5 * (min(c2['P_raw'][0,0][:,:,0,12][row,col],c2['P_raw'][0,0][:,:,0,13][row,col]) + min(c2['P_raw'][0,0][:,:,0,14][row,col],c2['P_raw'][0,0][:,:,0,15][row,col]))
                Po_error = C_stag*(c2['P_raw'][0,0][:,:,0,11][row,col] - P_avg_2) + c2['P_raw'][0,0][:,:,0,11][row,col]
            elif type == 3:
                P = sorted([c2['P_raw'][0,0][row,col,0,12],c2['P_raw'][0,0][row,col,0,13],c2['P_raw'][0,0][row,col,0,14],c2['P_raw'][0,0][row,col,0,15]])
                P_h = 0.5 * (P[3]+P[2])
                P_l = 0.5 * (P[1]+P[0])
                P_max = 0.666 * c2['P_raw'][0,0][row,col,0,11] + 0.334 * P_h
                Po_error = C_stag*(P_max - P_l) + c2['P_raw'][0,0][:,:,0,11][row,col]

            # Static Pressure Interpolation
            x = [c1['Iota'][0,0][index_row_2,index_col_1],c1['Iota'][0,0][index_row_1,index_col_1]]
            y = [c1['C_P'][0,0][index_row_2,index_col_1],c1['C_P'][0,0][index_row_1,index_col_1]]
            x_new = yaw
            CP_1 = interpol(x_new, x, y)

            x = [c1['Iota'][0,0][index_row_2,index_col_2],c1['Iota'][0,0][index_row_1,index_col_2]]
            y = [c1['C_P'][0,0][index_row_2,index_col_2],c1['C_P'][0,0][index_row_1,index_col_2]]
            CP_2 = interpol(x_new, x, y)

            x = [c1['Tau'][0,0][index_row_1,index_col_1],c1['Tau'][0,0][index_row_1,index_col_2]]
            y = [CP_1,CP_2]
            x_new = pitch
            C_stat = interpol(x_new, x, y)

            # Calculate static pressure error from interpolated coefficient
            if type == 0:
                P_error = Po_error - C_stat * (c2['P_raw'][0,0][:,:,0,11][row,col] - P_mean[row,col])
            elif type == 1:
                P_avg_1 = min(c2['P_raw'][0,0][:,:,0,12][row,col],c2['P_raw'][0,0][:,:,0,13][row,col],c2['P_raw'][0,0][:,:,0,14][row,col],c2['P_raw'][0,0][:,:,0,15][row,col])
                P_error = Po_error - C_stat * (c2['P_raw'][0,0][:,:,0,11][row,col] - P_avg_1)
            elif type == 2:
                P_avg_2 = 0.5 * (min(c2['P_raw'][0,0][:,:,0,12][row,col],c2['P_raw'][0,0][:,:,0,13][row,col]) + min(c2['P_raw'][0,0][:,:,0,14][row,col],c2['P_raw'][0,0][:,:,0,15][row,col]))
                P_error = P_avg_2 - C_stat * (c2['P_raw'][0,0][:,:,0,11][row,col] - P_avg_2)
            elif type == 3:
                P = sorted([c2['P_raw'][0,0][row,col,0,12],c2['P_raw'][0,0][row,col,0,13],c2['P_raw'][0,0][row,col,0,14],c2['P_raw'][0,0][row,col,0,15]])
                P_h = 0.5 * (P[3]+P[2])
                P_l = 0.5 * (P[1]+P[0])
                P_max = 0.666 * c2['P_raw'][0,0][row,col,0,11] + 0.334 * P_h
                P_error = Po_error - C_stat*(P_max - P_l) 


            # Feed calculated errors for yaw and pitch
            error_yaw[row,col] = yaw - c2['Iota'][0,0][row,col]
            error_pitch[row,col] = pitch - c2['Tau'][0,0][row,col]
            error_stat[row,col] = abs(P_error - c2['P_raw'][0,0][:,:,0,1][row,col])/dh * 100
            error_stag[row,col] = abs(Po_error - c2['P_raw'][0,0][:,:,0,0][row,col])/dh * 100
            

    # Set Window Size
    ylim1 = min(max(c1['Iota'][0,0][:,0]),abs(min(c1['Iota'][0,0][:,0])))
    xlim1 = min(max(c1['Tau'][0,0][0,:]),abs(min(c1['Tau'][0,0][0,:])))
    ylim2 = min(max(c2['Iota'][0,0][:,0]),abs(min(c2['Iota'][0,0][:,0])))
    xlim2 = min(max(c2['Tau'][0,0][0,:]),abs(min(c2['Tau'][0,0][0,:])))
    ylim = min(ylim1,ylim2)
    xlim = min(xlim1,xlim2)

    ylim = angle
    xlim = angle

    # Window adjustmenst for 30 degrees
    max_yaw, min_yaw, max_pitch, min_pitch = ind(angle,c2,1)

    # PITCH Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Pitch Angle Error (\xb0)', ylim, xlim)
    a1 = ax.contourf(c2['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c2['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_pitch[min_yaw:max_yaw,min_pitch:max_pitch], levels = 30, cmap='hot')
    cbar = fig.colorbar(a1)
    cbar.ax.tick_params(axis='y', labelsize=20)

    # YAW Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Yaw Angle Error (\xb0)', ylim, xlim)
    a2 = ax.contourf(c2['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c2['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_yaw[min_yaw:max_yaw,min_pitch:max_pitch], 30, cmap='hot')
    cbar = fig.colorbar(a2)
    cbar.ax.tick_params(axis='y', labelsize=20)

    # Static Pressure Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Static Pressure Error (%)', ylim, xlim)
    a3 = ax.contourf(c2['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c2['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_stat[min_yaw:max_yaw,min_pitch:max_pitch], 30, cmap='hot')
    cbar = fig.colorbar(a3)
    cbar.ax.tick_params(axis='y', labelsize=20)

    # Stagnation Pressure Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Stagnation Pressure Error (%)', ylim, xlim)
    a4 = ax.contourf(c2['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c2['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_stag[min_yaw:max_yaw,min_pitch:max_pitch], 30, cmap='hot')
    cbar = fig.colorbar(a4)
    cbar.ax.tick_params(axis='y', labelsize=20)

    # RMSE calculations
    rms_pitch = np.sqrt(sum(sum(error_pitch[min_yaw:max_yaw,min_pitch:max_pitch]**2))\
                        /np.size(error_pitch[min_yaw:max_yaw,min_pitch:max_pitch]))
    print('RMSE for Pitch Error is {} \xb0'.format(rms_pitch))
    rms_yaw = np.sqrt(sum(sum(error_yaw[min_yaw:max_yaw,min_pitch:max_pitch]**2))\
                        /np.size(error_yaw[min_yaw:max_yaw,min_pitch:max_pitch]))
    print('RMSE for Yaw Error is {} \xb0'.format(rms_yaw))
    rms_stat = np.sqrt(sum(sum(error_stat[min_yaw:max_yaw,min_pitch:max_pitch]**2))\
                        /np.size(error_stat[min_yaw:max_yaw,min_pitch:max_pitch]))
    print('RMSE for Static Error is {} %'.format(rms_stat))
    rms_stag = np.sqrt(sum(sum(error_stag[min_yaw:max_yaw,min_pitch:max_pitch]**2))\
                        /np.size(error_stag[min_yaw:max_yaw,min_pitch:max_pitch]))
    print('RMSE for Stagnation Error is {} %'.format(rms_stag))

    # Mode, mean and standard deviation
    mean_pitch = np.mean(error_pitch[min_yaw:max_yaw,min_pitch:max_pitch])
    mean_yaw = np.mean(error_yaw[min_yaw:max_yaw,min_pitch:max_pitch])
    mean_stat = np.mean(error_stat[min_yaw:max_yaw,min_pitch:max_pitch])
    mean_stag = np.mean(error_stag[min_yaw:max_yaw,min_pitch:max_pitch])

    mode_pitch = np.median(error_pitch[min_yaw:max_yaw,min_pitch:max_pitch])
    mode_yaw = np.median(error_yaw[min_yaw:max_yaw,min_pitch:max_pitch])
    mode_stat = np.median(error_stat[min_yaw:max_yaw,min_pitch:max_pitch])
    mode_stag = np.median(error_stag[min_yaw:max_yaw,min_pitch:max_pitch])

    std_pitch = np.std(error_pitch[min_yaw:max_yaw,min_pitch:max_pitch])
    std_yaw = np.std(error_yaw[min_yaw:max_yaw,min_pitch:max_pitch])
    std_stat = np.std(error_stat[min_yaw:max_yaw,min_pitch:max_pitch])
    std_stag = np.std(error_stag[min_yaw:max_yaw,min_pitch:max_pitch])

    print('Pitch')
    print('mean = {}, mode = {}, std = {}'.format(mean_pitch,mode_pitch,std_pitch))
    print('Yaw')
    print('mean = {}, mode = {}, std = {}'.format(mean_yaw,mode_yaw,std_yaw))
    print('Static')
    print('mean = {}, mode = {}, std = {}'.format(mean_stat,mode_stat,std_stat))
    print('Stagnation')
    print('mean = {}, mode = {}, std = {}'.format(mean_stag,mode_stag,std_stag))

    plt.show()