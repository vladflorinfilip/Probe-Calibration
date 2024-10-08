import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Plot Pitch 
species = ("low Re", "high Re", "Probe 2", "Probe 3", "Probe 4", "Probe 5")
penguin_means = {
    'RMSE': (1.643 ,
12.71 ,
22.95 ,
23.38 ,
24.51 ,
23.93 
),
    'Mean': (1.101 ,
8.143 ,
13.35 ,
13.22 ,
13.43 ,
14.51 


),
    'Standard Deviation': (1.219 ,
9.772 ,
18.66 ,
19.28 ,
20.52 ,
19.04 
 
),
}

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0
colors = ['cornflowerblue', 'darkolivegreen', 'maroon']

for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    plt.bar(x + offset, measurement, width, label=attribute)
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('Error (%)', fontsize = 20)
plt.title('Stagnation Pressure Errors', fontsize = 20)
plt.yticks(fontsize = 20)
plt.xticks(x + width, species, fontsize = 20)
plt.legend(loc='upper left', fontsize = 20)
plt.ylim(0,40)

plt.show()