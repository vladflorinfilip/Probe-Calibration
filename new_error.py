# This function takes two sets of data and finds the error plots

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from stencils import interpol
from stencils import set_axes
from scipy.interpolate import LinearNDInterpolator
from stencils import closest
import math

# Function to get indecies for given angle
def ind(angle,Iota,Tau,yes =1):
        
    if yes == 1:
    # Set window angles
        
        # Yaw
        yaw_angles = Iota[:,0].tolist()
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
        pitch_angles = Tau[0,:].tolist()
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


    return max_yaw, min_yaw, max_pitch, min_pitch

# MAIN ERROR FUNCTION
# Calculates erros for yaw, pitch, static and stagnation coefficients
# for two dataset of the same length
def error(c1,c2,type,angle = 30):
    # REFERENCE is c1
    # TEST is c2

    # Initialise dynamic head for nondimensionalisation
    rho = np.mean(c2['Pa'][0,0])/(np.mean(c2['Ta'][0,0])*287)
    dh = rho * 0.5 * 40**2

    # Calculate mean pressure
    P_mean = 0.25* (c2['P_raw'][0,0][:,:,0,11] + c2['P_raw'][0,0][:,:,0,12] + c2['P_raw'][0,0][:,:,0,13] + c2['P_raw'][0,0][:,:,0,15])

    # Yaw is row and pitch is collumns

    # Interpolate Tau and Iota for the reference
    cartcoord = list(zip(c1['Tau'][0,0].flatten(), c1['Iota'][0,0].flatten()))
    Iota_Reference = np.linspace(np.min(c1['Iota'][0,0]), np.max(c1['Iota'][0,0]),100)
    Tau_Reference = np.linspace(np.min(c1['Tau'][0,0]), np.max(c1['Tau'][0,0]),100)
    Tau, Iota = np.meshgrid(Tau_Reference, Iota_Reference)  # 2D grid for interpolation
    interp = LinearNDInterpolator(cartcoord, c1['C_Alpha'][0,0].flatten())
    C_Alpha_Ref = interp(Tau, Iota)
    interp = LinearNDInterpolator(cartcoord, c1['C_Beta'][0,0].flatten())
    C_Beta_Ref = interp(Tau, Iota)
    interp = LinearNDInterpolator(cartcoord,c1['C_P'][0,0].flatten())
    C_P_Ref = interp(Tau, Iota)
    interp = LinearNDInterpolator(cartcoord, c1['C_Po'][0,0].flatten())
    C_Po_Ref = interp(Tau, Iota)

    # Initialise error vectors
    error_yaw = np.ones((len(Iota[:,0]),len(Iota[0,:])))
    error_pitch = np.ones((len(Iota[:,0]),len(Iota[0,:])))
    error_stat = np.ones((len(Iota[:,0]),len(Iota[0,:])))
    error_stag = np.ones((len(Iota[:,0]),len(Iota[0,:])))

    # Interpolate Tau and Iota for the test
    Iota_Test = np.linspace(np.min(c2['Iota'][0,0]), np.max(c2['Iota'][0,0]),100)
    Tau_Test = np.linspace(np.min(c2['Tau'][0,0]), np.max(c2['Tau'][0,0]),100)
    Tau_T, Iota_T = np.meshgrid(Tau_Test, Iota_Test)  # 2D grid for interpolation
    cartcoord_T = list(zip(c2['Tau'][0,0].flatten(), c2['Iota'][0,0].flatten()))
    interp = LinearNDInterpolator(cartcoord_T, c2['C_Alpha'][0,0].flatten())
    C_Alpha_Test = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['C_Beta'][0,0].flatten())
    C_Beta_Test = interp(Tau_T, Iota_T)

    # Interpolate Mean, Centre, Static and Total Pressures TEST
    interp = LinearNDInterpolator(cartcoord_T, P_mean.flatten())
    P_mean_int = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['P_raw'][0,0][:,:,0,1].flatten())
    P_T = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['P_raw'][0,0][:,:,0,0].flatten())
    Po_T = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['P_raw'][0,0][:,:,0,11].flatten())
    Pcentre = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['P_raw'][0,0][:,:,0,12].flatten())
    Ptop = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['P_raw'][0,0][:,:,0,13].flatten())
    Pbottom = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['P_raw'][0,0][:,:,0,14].flatten())
    Pright = interp(Tau_T, Iota_T)
    interp = LinearNDInterpolator(cartcoord_T, c2['P_raw'][0,0][:,:,0,15].flatten())
    Pleft = interp(Tau_T, Iota_T)

    for row in range(len(C_Alpha_Test[:,0])):
        for col in range(len(C_Beta_Test[0,:])):
            C_yaw = C_Alpha_Test[row,col]
            C_pitch = C_Beta_Test[row,col]

            # Find intersection point
            C1 = abs(C_Alpha_Ref - C_yaw)
            C2 = abs(C_Beta_Ref - C_pitch)
            C = C1 + C2
            # Find minimum
            index_row, index_col = np.unravel_index(C.argmin(), C.shape)
            
            yaw = Iota[index_row,index_col]
            pitch = Tau[index_row,index_col]

            error_yaw[row,col] = - Iota_T[row,col] + yaw
            error_pitch[row,col] = - Tau_T[row,col] + pitch

            # Calculate stagnation pressure error from interpolated coefficient
            C_stag = C_Po_Ref[index_row,index_col]
            if type == 0:
                Po = C_stag*(Pcentre[row,col] - P_mean_int[row,col]) + Pcentre[row,col]
            elif type == 1:
                P_avg_1 = min(Ptop[row,col],Pbottom[row,col],Pright[row,col],Pleft[row,col])
                Po = C_stag*(Pcentre[row,col] - P_avg_1) + Pcentre[row,col]
            elif type == 2:
                P_avg_2 = 0.5 * (min(Ptop[row,col],Pbottom[row,col]) + min(Pright[row,col],Pleft[row,col]))
                Po = C_stag*(Pcentre[row,col] - P_avg_2) + Pcentre[row,col]
            elif type == 3:
                P = sorted([Ptop[row,col,0,12],Pbottom[row,col],Pleft[row,col],Pright[row,col]])
                P_h = 0.5 * (P[3]+P[2])
                P_l = 0.5 * (P[1]+P[0])
                P_max = 0.666 * c2['P_raw'][0,0][row,col,0,11] + 0.334 * P_h
                Po = C_stag*(P_max - P_l) + c2['P_raw'][0,0][:,:,0,11][row,col]
            

            # Calculate static pressure error from interpolated coefficient
            C_stat = C_P_Ref[index_row,index_col]
            if type == 0:
                P = Po - C_stat * (Pcentre[row,col] - P_mean[row,col])
            elif type == 1:
                P_avg_1 = min(Ptop[row,col],Pbottom[row,col],Pright[row,col],Pleft[row,col])
                P = Po - C_stat * (Pcentre[row,col] - P_avg_1)
            elif type == 2:
                P_avg_2 = 0.5 * (min(Ptop[row,col],Pbottom[row,col]) + min(Pright[row,col],Pleft[row,col]))
                P = Po - C_stat * (Pcentre[row,col] - P_avg_2)
            elif type == 3:
                P = sorted([Pright[row,col],Pleft[row,col],Ptop[row,col],Pbottom[row,col]])
                P_h = 0.5 * (P[3]+P[2])
                P_l = 0.5 * (P[1]+P[0])
                P_max = 0.666 * Pcentre[row,col] + 0.334 * P_h
                P = Po - C_stag*(P_max - P_l) 
            error_stat[row,col] = abs(P - P_T[row,col])/dh * 100
            error_stag[row,col] = abs(Po - Po_T[row,col])/dh * 100
            
    # Window adjustmenst
    max_yaw, min_yaw, max_pitch, min_pitch = ind(angle,Iota_T,Tau_T)

    # PITCH Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Pitch Angle Error (\xb0)',angle,angle)
    a1 = ax.contourf(Tau_T[min_yaw:max_yaw,min_pitch:max_pitch],Iota_T[min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_pitch[min_yaw:max_yaw,min_pitch:max_pitch],30, cmap='hot')
    fig.colorbar(a1)

    # YAW Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Yaw Angle Error (\xb0)',angle,angle)
    a2 = ax.contourf(Tau_T[min_yaw:max_yaw,min_pitch:max_pitch],Iota_T[min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_yaw[min_yaw:max_yaw,min_pitch:max_pitch],30, cmap='hot')
    fig.colorbar(a2)

    # Static Pressure Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Static Pressure Error (%)',angle,angle)
    a3 = ax.contourf(Tau_T[min_yaw:max_yaw,min_pitch:max_pitch],Iota_T[min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_stat[min_yaw:max_yaw,min_pitch:max_pitch], 30, cmap='hot')
    fig.colorbar(a3)

    # Stagnation Pressure Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Stagnation Pressure Error (%)',angle,angle)
    a4 = ax.contourf(Tau_T[min_yaw:max_yaw,min_pitch:max_pitch],Iota_T[min_yaw:max_yaw,min_pitch:max_pitch] \
                , error_stag[min_yaw:max_yaw,min_pitch:max_pitch], 30, cmap='hot')
    fig.colorbar(a4)

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