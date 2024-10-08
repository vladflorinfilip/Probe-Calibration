time = [0,1,2,3,4,4.5,4.7,4.7,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,15,20,25]
reactivity = [0,0,0,0,0,0,-14,-12,-10,-8,-7,-6,-5.5,-5.2,-5,-4.8,-4.7,-4.6,-4.5,-3.5,-3,-2.5]

import matplotlib.pyplot as plt
import numpy as np



plt.plot(time,np.log(reactivity),'-o')
plt.show()