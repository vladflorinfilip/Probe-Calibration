import matplotlib.pyplot as plt   
from stencils import set_axes 

def variations(c1,c2):

    # Call functions
    fig, ax = plt.subplots()
    print(int(len(c1['C_Alpha'][0,0][0,:])/2))
    a1 = ax.plot(c1['Iota'][0,0][:,int(len(c1['C_Alpha'][0,0][0,:])/2)], c1['C_Alpha'][0,0][:,int(len(c1['C_Alpha'][0,0][0,:])/2)],'-o',label = 'Original Data',color = 'darkolivegreen')
    a1 = ax.plot(c2['Iota'][0,0][:,int(len(c2['C_Alpha'][0,0][0,:])/2)], c2['C_Alpha'][0,0][:,int(len(c2['C_Alpha'][0,0][0,:])/2)],'-o',label = 'Nulled Transformation',color = 'royalblue')
    # a1 = ax.plot(c3['Tau'][0,0][23,:],coef3[23,:],label = 'R_e = 5,560',color = 'g')
    ax.legend(prop = {'size':30})
    # Plotting
    ylim = 1.5
    xlim = 15
    set_axes(ax,'Yaw/\xb0','Yaw Coefficient','', ylim, xlim)
    ax.grid()
    plt.show()

    fig, ax = plt.subplots()
    a2 = ax.plot(c1['Tau'][0,0][int(len(c1['Tau'][0,0][:,0])/2),:], c1['C_Beta'][0,0][int(len(c1['Tau'][0,0][:,0])/2),:],'-o',label = 'Original Data',color = 'darkolivegreen')
    a2 = ax.plot(c2['Tau'][0,0][int(len(c1['Tau'][0,0][:,0])/2),:], c2['C_Beta'][0,0][int(len(c1['Tau'][0,0][:,0])/2),:],'-o',label = 'Nulled Transformation',color = 'royalblue')
    ax.legend(prop = {'size':30})
    set_axes(ax,'Pitch/\xb0','Pitch Coefficient','',  ylim, xlim)
    ax.grid()
    plt.show()