import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

# Measured value for Channel 1
mean_channel_1 = 0  # kPa

# Assumed standard deviation for Channel 1
std_dev_channel_1 = 5  # Pa

# Define the normal distribution
distribution_channel_1 = norm(loc=mean_channel_1, scale=std_dev_channel_1)

# Generate data points from the distribution
data_points_channel_1 = distribution_channel_1.rvs(size=1000)  # Generating 1000 random samples

# Plot the histogram of the generated data points
plt.hist(data_points_channel_1, bins=30, density=True, alpha=0.6, color='g')

# Plot the probability density function (PDF) of the distribution
x = np.linspace(mean_channel_1 - 3*std_dev_channel_1, mean_channel_1 + 3*std_dev_channel_1, 100)
plt.plot(x, distribution_channel_1.pdf(x), 'k', linewidth=2)

# Add labels and title
plt.xlabel('Pressure (Pa)', fontsize = 30, weight='bold')
plt.ylabel('Probability Density', fontsize = 30, weight='bold')
plt.title('(c) Normal Distribution Central Channel, 1000 samples', fontsize = 30, weight='bold')
plt.xticks(fontsize = 20)
plt.yticks(fontsize = 20)

# Show plot
plt.grid(True)
plt.show()