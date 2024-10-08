# Import modules
import numpy as np
import scipy.io
import statistics as st
import matplotlib.pyplot as plt
from stencils import pol_fit

def set_time(c):

    # DON'T FORGET TO ADJUST SPEED
    v = 40
    rho = 1.29
    dh = rho * v ** 2.0 * 0.5


    # 11 centre
    # 12 top
    # 13 bottom
    # 14 right
    # 15 left
    data = {11 : [], 12 : [], 13 : [], 14 : [], 15 : []}
    for i in [11,12,13,14,15]:
        for j in range(2,len(c[0,0][2][0,0][0,:,0])):
            # Standard deviation
            std = np.std(c[0,0][2][0,0][0,0:j,i])
            # Standard deviation from the mean
            std = std * np.sqrt(1/(len(c[0,0][2][0,0][0,0:j,i])-1))
            # 95% confidence interval
            std = 2 * std
            # Calculate precision error of dynamic head
            pe = std / dh * 100
            data[i].append(pe)

    # DSA range with +- 0.2%
    pa = 2500 # 10'' H20
    rang = pa * 0.2 /100
    range_dh = rang/dh * 100
    plt.plot([0,len(data[15])],[range_dh,range_dh],'--',color = 'black',label = 'DSA range')


    plt.plot(np.arange(len(data[11]))/50.0,data[11],'.', label = 'centre', color = 'y')
    plt.plot(np.arange(len(data[15]))/50.0,data[15],'.', label = 'top', color = 'b')
    plt.plot(np.arange(len(data[13]))/50.0,data[13],'.', label = 'bottom', color = 'r')
    plt.plot(np.arange(len(data[14]))/50.0,data[14],'.', label = 'right', color = 'm')
    plt.plot(np.arange(len(data[12]))/50.0,data[12],'.', label = 'left', color = 'g')
    plt.xlabel('Time/s', fontsize = 20, weight = 'bold')
    plt.ylabel('Precision Error of the Dynamic Head / %', fontsize = 20, weight = 'bold')
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.grid()
    plt.xlim(0,30)
    plt.legend(fontsize = 20)


 # Find and display averaging time
    list_check = range_dh * np.ones(len(data[11]))
    idx1 = np.argwhere(np.diff(np.sign(data[11] - list_check))).flatten()
    idx2 = np.argwhere(np.diff(np.sign(data[12] - list_check))).flatten()
    idx3 = np.argwhere(np.diff(np.sign(data[13] - list_check))).flatten()
    idx4 = np.argwhere(np.diff(np.sign(data[14] - list_check))).flatten()
    idx5 = np.argwhere(np.diff(np.sign(data[15] - list_check))).flatten()
 
    idx1 = idx1.tolist()
    idx2 = idx2.tolist()
    idx3 = idx3.tolist()
    idx4 = idx4.tolist()
    idx5 = idx5.tolist()

    idx1.append(1)
    idx2.append(1)
    idx3.append(1)
    idx4.append(1)
    idx5.append(1)

    max_idx = max(max(idx1),max(idx2),max(idx3),max(idx4),max(idx5))

    plt.text(23, 0.55, 'Avg time = {} s'.format(np.arange(len(data[11]))[max_idx]/50.0), fontsize = 20)

    plt.show()

settling_times = [0,0.2,0.5,0.7,1.0,1.2,1.5,1.7,2,3,4,5,6]
yaw_angle_err = [1.06,0.628, 0.3571, 0.2,0.14, 0.11, 0.099,0.096, 0.094, 0.092, 0.090,0.089, 0.088]
plt.plot(settling_times,yaw_angle_err,'.-', color = 'royalblue')
list_check = 0.1 * np.ones(len(yaw_angle_err))
idx = np.argwhere(np.diff(np.sign(yaw_angle_err - list_check))).flatten()
idx = idx.tolist()
idx.append(1)
max_idx = max(idx)
plt.plot([0,6],[0.1,0.1],'--',color = 'black',label = '0.1% Error')
plt.text(3, 0.35, 'Set time = {} s'.format(1.51), fontsize = 20)
plt.xlim(0,6)
plt.ylim(0,1.1)
plt.xlabel("Settling Time/s", fontsize = 20)
plt.ylabel("Percentage of Yaw Angle Erro/%", fontsize = 20)
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)

plt.grid()
plt.show()