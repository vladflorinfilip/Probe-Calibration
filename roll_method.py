import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit
from scipy.optimize import minimize

def interpolated_func(x_val):
    return f2(x_val)

RSME_Probe2 = [14.789995379910986,12.41220160118824,10.217890978203727,9.0807141910131422,8.537255159581134,8.376859775320215,8.195613974957361,8.183067995794904,9.488752175301724,11.87285342953422,14.457178777749464]
RSME_Probe1 = [2.5,1.8,1.4602784531209443,0.9838912837547946,0.4841944384549892,0,0.47559173654126224,0.9638702800843983,1.4349082236647768,1.8,2.500]
angles= [-5,-4,-3,-2,-1,0,1,2,3,4,5]

# Example Data
x = np.array(angles)
y1 = np.array(RSME_Probe1)
y2 = np.array(RSME_Probe2)

# Interpolation
f1 = interp1d(x, y1, kind='cubic')
f2 = interp1d(x, y2, kind='cubic')

# For interpolation, we create a finer set of x values
x_new = np.linspace(x.min(), x.max(), 500)
y1_interp = f1(x_new)
y2_interp = f2(x_new)

# Curve Fitting (assuming a polynomial function for example)
def poly_func(x, a, b, c, d):
    return a * x**3 + b * x**2 + c * x + d

params1, _ = curve_fit(poly_func, x, y1)
params2, _ = curve_fit(poly_func, x, y2)

y1_fit = poly_func(x_new, *params1)
y2_fit = poly_func(x_new, *params2)

# Find the minimum using minimize
result = minimize(interpolated_func, x0=np.mean(x), bounds=[(x.min(), x.max())])

# Get the x and y values of the minimum
x_min = result.x[0]
y_min = interpolated_func(x_min)

# Print the x and y values of the minimum
print(f"Minimum at x: {x_min}, y: {y_min}")

# Plotting
plt.figure(figsize=(12, 8))
plt.plot(x, y1, 'o', label='Probe 1 (data)')
plt.plot(x, y2, 'o', label='Probe 2 (data)')
plt.plot(x_new, y1_interp, '-', label='Probe 1 (interp)')
plt.plot(x_new, y2_interp, '-', label='Probe 2 (interp)')
plt.plot(x_new, y1_fit, '--', label='Probe 1 (fit)')
plt.plot(x_new, y2_fit, '--', label='Probe 2 (fit)')
plt.ylabel('Static Pressure RMSE [%]', fontsize=20)
plt.xlabel('Angle [\xb0]', fontsize=20)
plt.legend(fontsize=20)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)
plt.grid()
plt.show()

