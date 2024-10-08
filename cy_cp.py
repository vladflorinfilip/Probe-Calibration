# IMPORTS
import matplotlib.pyplot as plt 
from stencils import closest

# Function
def cy_cp(c):
    
    plt.plot(c['C_Alpha'][0,0],c['C_Beta'][0,0])
    plt.xlabel('Yaw Coefficient')
    plt.ylabel('Pitch Coefficient')
    plt.grid()
    plt.show()


# Compare function

def cy_cp_1(c,color,label,angle):

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
    
    lines = plt.plot(c['C_Alpha'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],c['C_Beta'][0,0][min_yaw:max_yaw,min_pitch:max_pitch],color = color)
    plt.xlabel('Yaw Coefficient',fontsize = 20)
    plt.ylabel('Pitch Coefficient',fontsize = 20)
    return lines

def compare(c1,angle):

    lines1 = cy_cp_1(c1,'red','Side',angle)

    plt.grid()
    plt.legend([lines1[0]],['Side'],fontsize = 20)
    plt.show()