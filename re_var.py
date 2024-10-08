# This function takes two sets of data and finds the error plots

# Import modules
import numpy as np
import matplotlib.pyplot as plt
from stencils import set_axes
from calc_coef import tr_yc

# Plots coefficients variation with yaw and/or pitch
# Adjust argument numbers if needed
def plot_re(c1,c2,c3):

    # Plot yaw coefficient variations with Reynolds
    # At 0 pitch
    coef1 = tr_yc(c1,12)
    coef3 = tr_yc(c2,12)
    coef2 = tr_yc(c3,12)
    fig, ax = plt.subplots()
    set_axes(ax,'Yaw/\xb0','Yaw Coefficient','Reynolds variation at 30\xb0 pitch',0,0)
    a1 = ax.plot(c1['Iota'][0,0][:,32],coef1[:,32],label = 'Re = 1,853',color = 'r')
    a1 = ax.plot(c2['Iota'][0,0][:,32],coef2[:,32],label = 'Re = 3,700',color = 'b')
    a1 = ax.plot(c3['Iota'][0,0][:,32],coef3[:,32],label = 'Re = 5,560',color = 'g')
    ax.legend()
    ax.grid()
    ax.set_xlim(-30,30)
    ax.set_ylim(-20,20)


    # Plot static coefficient variations with Reynolds
    fig, ax = plt.subplots()
    set_axes(ax,'Yaw/\xb0','Normalised Left Hole Coefficient','(b) Reynolds variation at 30\xb0 pitch',0,0)
    a1 = ax.plot(c1['Iota'][0,0][:,16],c1['C_Alpha'][0,0][:,16],label = 'R_e = 1,853',color = 'r')
    a1 = ax.plot(c2['Iota'][0,0][:,16],c2['C_Alpha'][0,0][:,16],label = 'R_e = 3,700',color = 'b')
    a1 = ax.plot(c3['Iota'][0,0][:,16],c3['C_Alpha'][0,0][:,16],label = 'R_e = 5,560',color = 'g')
    ax.legend()
    ax.set_xlim(-30,30)
    ax.set_ylim(-6,6)

    # Plot static coefficient variations with Reynolds
    fig, ax = plt.subplots()
    set_axes(ax,'Pitch/\xb0','Normalised Top Hole Coefficient','(a) Reynolds variation at 30\xb0 yaw',0,0)
    a1 = ax.plot(c1['Tau'][0,0][12,:],c1['C_Beta'][0,0][12,:],label = 'Re = 1,853',color = 'r')
    a1 = ax.plot(c2['Tau'][0,0][12,:],c2['C_Beta'][0,0][12,:],label = 'Re = 3,700',color = 'b')
    a1 = ax.plot(c3['Tau'][0,0][12,:],c3['C_Beta'][0,0][12,:],label = 'Re = 5,560',color = 'g')
    ax.legend(fontsize= 30)
    ax.set_xlim(-30,30)
    ax.set_ylim(-10,10)

    plt.show()
    