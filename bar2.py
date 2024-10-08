import matplotlib.pyplot as plt
import numpy as np

# Plot Pitch 
species = ("Probe 2", "Probe 3", "Probe 4", "Probe 5")
penguin_means = {
    'Hemispherical': (
8.208781401746608,
7.0969026700404685,
1.8190868161745075,
1.8190868161745075
),
    'Conical': (
58.749928614240396,
57.10809569686134,
37.305075207408095,
37.305075207408095


),
    'Perpemndicular': (
8.192599020705936,
7.215940421249978,
2.6881371217638597,
2.6881371217638597
 
),
}

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0
colors = ['royalblue', 'darkslategrey', 'navy']
i = 0
for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    plt.bar(x + offset, measurement, width, label=attribute, color = colors[i])
    i += 1
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('RMSE (%)', fontsize = 30)
plt.title('Static Pressure Error', fontsize = 30)
plt.yticks(fontsize = 30)
plt.xticks(x + width, species, fontsize = 30)
plt.legend(loc='upper right', fontsize = 30)

plt.show()

# Plot Pitch 
species = ("Probe 2", "Probe 3", "Probe 4", "Probe 5")
penguin_means = {
    'Oxford': (
4.00743518255717,
4.10647026662134,
1.5435588439201096,
1.5435588439201096
),
    'Hodson': (
26.93222229634458,
28.526298590933866,
20.15778147023865,
20.15778147023865


),
    'Curtis': (
4.911558387110955,
4.435539246069146,
2.001074858246256,
2.001074858246256
 
),
}

x = np.arange(len(species))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0
colors = ['royalblue', 'darkslategrey', 'navy']
i = 0
for attribute, measurement in penguin_means.items():
    offset = width * multiplier
    plt.bar(x + offset, measurement, width, label=attribute, color = colors[i])
    i += 1
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
plt.ylabel('RMSE (%)', fontsize = 30)
plt.title('Stagnation Pressure Error', fontsize = 30)
plt.yticks(fontsize = 30)
plt.xticks(x + width, species, fontsize = 30)
plt.legend(loc='upper right', fontsize = 30)

plt.show()