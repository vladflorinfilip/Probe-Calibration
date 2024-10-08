import matplotlib.pyplot as plt

# Data for the bars
categories = ['Conical', 'Hemispherical', 'Perpendicular']
values = [2.789, 2.138, 1.201]

# Colors for the bars
colors = ['royalblue', 'darkslategrey', 'navy']

# Width of each bar
bar_width = 0.5

# Positions for the bars
positions = range(len(categories))

# Creating the bar chart
plt.bar(positions, values, width=bar_width, color=colors)

# Adding text at the top of each bar
for i, value in enumerate(values):
    plt.text(i, value + 0.001, str(value), ha='center', color='black', fontsize=30)

# Adjusting the x-axis ticks and labels
plt.xticks(positions, categories, fontsize=30)
plt.ylim(0, 3)
plt.yticks(fontsize=30)

# Adding labels and title
plt.ylabel('Static Pressure RMSE [%]', fontsize=30)
plt.title('(c) Static Pressure Error', fontsize=30, weight='bold')

# Adjust layout to make room for the text at the bottom
plt.tight_layout()

# Show the plot
plt.show()

