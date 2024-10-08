import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

# Generate some data
x = np.linspace(-2, 2, 100)
y = np.linspace(-2, 2, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) * np.cos(Y)

# Define the new minimum and maximum values
new_min = -2.4
new_max = 3

# Scale and shift the data
scaled_and_shifted_Z = (Z - np.min(Z)) / (np.max(Z) - np.min(Z)) * (new_max - new_min) + new_min

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the contour plot
contour = ax.contourf(X, Y, scaled_and_shifted_Z, cmap='hot', levels=30, vmin=new_min, vmax=new_max)

# Manually create the color bar
cbar = fig.colorbar(contour, ax=ax)
cbar.ax.tick_params(axis='y', labelsize=20)


# Set the tick labels
cbar.set_ticks(np.linspace(new_min, new_max, 10))
cbar.ax.set_yticklabels([f'{tick:.1f}' for tick in np.linspace(new_min, new_max, 10)])

# Set labels and title for the plot
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Contour Plot')

plt.show()


