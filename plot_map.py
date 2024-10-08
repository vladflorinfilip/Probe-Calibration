# Import modules
import numpy as np
import matplotlib.pyplot as plt
from stencils import set_axes
from stencils import closest

# Plot contour map for stag/stat pressure  and yaw/pitch coefficients
def plot_cont(c,angle = 30):

    # Window adjustmenst

    ylim = angle
    xlim = angle

    # Window adjustmenst for 30 degrees
    yes = 1
    if yes == 1:
    # Set window angles
        
        # Yaw
        yaw_angles = c['Iota'][0,0][:,0].tolist()
        k = closest(yaw_angles,angle)
        if k <= angle:
            max_yaw = min(len(yaw_angles),yaw_angles.index(k) + 2)
        else:
            max_yaw = yaw_angles.index(k) + 1


        k = closest(yaw_angles,-angle) 
        if k >= -angle:
            min_yaw = max(0,yaw_angles.index(k) - 1)
        else:
            min_yaw = yaw_angles.index(k)

        # Pitch
        pitch_angles = c['Tau'][0,0][0,:].tolist()
        k = closest(pitch_angles,angle)  
        if k <= angle:
            max_pitch = min(len(pitch_angles),pitch_angles.index(k) + 2)
        else:
            max_pitch = pitch_angles.index(k) + 1
        k = closest(pitch_angles,-angle)
        if k >= -angle:
            min_pitch = max(0,pitch_angles.index(k) - 1)
        else:
            min_pitch = pitch_angles.index(k)

    else: 
        max_yaw = np.size(c['Iota'][0,0][:,0]-1)
        min_yaw = 0
        max_pitch = np.size(c['Tau'][0,0][0,:]-1)
        min_pitch = 0
    
    # PITCH Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Pitch Coefficient',ylim,xlim)
    a1 = ax.contourf(c['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , c['C_Beta'][0,0][min_yaw:max_yaw,min_pitch:max_pitch], 30, linewidths=5, cmap='twilight',figuresize = (10,20))
    #ax.contour(c['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
    #            , c['C_Beta'][0,0][min_yaw:max_yaw,min_pitch:max_pitch], levels =[2.125], colors = 'k')
    #ax.plot([-17,-17],[-30,30],'--',color = 'black')
    #ax.plot([-35,24],[15.2,15.2],'--',color = 'black')
    cbar = fig.colorbar(a1)
    cbar.ax.tick_params(axis='y', labelsize=20)

    # YAW Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Yaw Coefficient',ylim,xlim)
    a2 = ax.contourf(c['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , c['C_Alpha'][0,0][min_yaw:max_yaw,min_pitch:max_pitch], 30, linewidths= 5, cmap='twilight',figuresize = (10,20))
    #ax.contour(c['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
    #            , c['C_Alpha'][0,0][min_yaw:max_yaw,min_pitch:max_pitch], levels =[1.876], colors= 'k')
    #ax.plot([-17,-17],[-30,30],'--',color = 'black')
    #ax.plot([-35,24],[15.2,15.2],'--',color = 'black')
    cbar = fig.colorbar(a2)
    cbar.ax.tick_params(axis='y', labelsize=20)

    # Static Pressure Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Static Pressure Coefficient',ylim,xlim)
    a3 = ax.contourf(c['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , c['C_P'][0,0][min_yaw:max_yaw,min_pitch:max_pitch], 30, cmap='twilight',figuresize = (10,20))
    #ax.plot([-17,-17],[-30,30],'--',color = 'black')
    #ax.plot([-35,24],[15.2,15.2],'--',color = 'black')
    cbar = fig.colorbar(a3)
    cbar.ax.tick_params(axis='y', labelsize=20)

    # Stagnation Pressure Error Plot
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Yaw/\xb0','Stagnation Pressure Coefficient',ylim,xlim)
    a4 = ax.contourf(c['Tau'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c['Iota'][0,0][min_yaw:max_yaw,min_pitch:max_pitch] \
                , c['C_Po'][0,0][min_yaw:max_yaw,min_pitch:max_pitch], 30, cmap='twilight',figuresize = (10,20))
    #ax.plot([-17,-17],[-30,30],'--',color = 'black')
    #ax.plot([-35,24],[15.2,15.2],'--',color = 'black')
    cbar = fig.colorbar(a4)
    cbar.ax.tick_params(axis='y', labelsize=20)

    plt.show()