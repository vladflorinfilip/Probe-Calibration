import matplotlib.pyplot as plt
import numpy as np

# Data
species = ("Yaw RMSE(\xb0)")
penguin_means = {
    'Conical': (1.422742376680629),
    'Hemispherical': (1.290241195589075),
    'Perpendicular': (1.3579562041162347),
}

# Configuration
x = np.arange(len(species))  # the label locations
height = 0.25  # the height of the bars

# Plotting
fig, ax = plt.subplots(figsize=(12, 8))
colors = ['green', 'darkolivegreen', 'springgreen']
print
for i, (attribute, measurement) in enumerate(penguin_means.items()):
    ax.barh(x + i*height, measurement, height, label=attribute, color=colors[i])

# Adding labels, title, and custom x-axis tick labels
ax.set_xlabel('RMSE (%)', fontsize=30)
ax.set_title('Static Pressure Error', fontsize=30)
ax.set_yticks(x + height)
ax.set_yticklabels(species, fontsize=30)
ax.legend(loc='upper right', fontsize=30)
ax.tick_params(axis='x', labelsize=30)

plt.show()

