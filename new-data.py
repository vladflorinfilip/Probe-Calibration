import matplotlib.pyplot as plt
import numpy as np

# Data
species = ["Static Pressure", "Stagnation Pressure"]
penguin_means = {
    'Yaw Nulling': (0.13, 0.406),
    'Pitch Nulling': (0.16, 0.157),
}

# Configuration
x = np.arange(len(species))  # the label locations
width = 0.35  # the width of the bars

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))

colors = ['green', 'springgreen']
i = 0
# Stacking bars from bottom to top
bottom = np.zeros(len(species))
for attribute, measurement in penguin_means.items():
    ax.bar(x, measurement, width, bottom=bottom, label=attribute,color = colors[i])
    bottom += np.array(measurement)
    i = i +1

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('RMSE (%)', fontsize = 30)
plt.title('(b) Pressure Error Reduction', fontsize = 30)
plt.yticks(fontsize = 30)
plt.xticks(x , species, fontsize = 30)
plt.legend(loc='upper left', fontsize = 30)

plt.show()