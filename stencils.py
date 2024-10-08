import numpy as np
import matplotlib.pyplot as plt 

# Define interpolation function
def interpol(x_new,x,y):
    xdif = x[1] - x[0]
    ydif = y[1] - y[0]
    y = y[0] + (x_new - x[0])*ydif/xdif
    return y

# Set Axes
def set_axes(ax,xlab,ylab,title,ylim,xlim):
    # Add axes labels
    ax.set_title(title,fontsize = 30, weight='bold')
    ax.set_xlabel(xlab,fontsize = 30, weight='bold'); ax.set_ylabel(ylab,fontsize = 30, weight='bold');
    if ylim!=0 and xlim!=0:
        ax.set_ylim(-ylim,ylim)
        ax.set_xlim(-xlim,xlim)
    ax.tick_params(axis = 'x', labelsize = 20)
    ax.tick_params(axis = 'y', labelsize = 20)
    return(ax)

# Polynomial fit function
def pol_fit(x,y,order):

    # Get best fit function
    z = np.polyfit(x, y, order)
    f = np.poly1d(z)  

    return f(x)

# Find closest to number function
def closest(lst, K):
     
    return lst[min(range(len(lst)), key = lambda i: abs(lst[i]-K))]
     
# Flip angle signs
def flip_sgn(c):
    for row in range(len(c['Iota'][0,0][:,0])):
        for col in range(len(c['Tau'][0,0][0,:])):
            c['C_Beta'][0,0][row,col] = -c['C_Beta'][0,0][row,col]
            c['C_Alpha'][0,0][row,col] = -c['C_Alpha'][0,0][row,col]
    return c