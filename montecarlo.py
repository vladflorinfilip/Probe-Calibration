# Import
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt
from stencils import set_axes

def calculate_c_alpha(pressures):

    P_avg = 0.5*(min(pressures[1],pressures[2])+min(pressures[3],pressures[4]))    
    return (pressures[3]-pressures[4])/(pressures[0] - P_avg)

def calculate_c_beta(pressures):

    P_avg = 0.5*(min(pressures[1],pressures[2])+min(pressures[3],pressures[4]))    
    return (pressures[1]-pressures[2])/(pressures[0] - P_avg)

def calculate_kp(pressures):
    return(pressures[1]-pressures[2])/(pressures[5]-pressures[6])

def calculate_ky(pressures):
    return(pressures[3]-pressures[4])/(pressures[5]-pressures[6])

# Function to calculate uncertainty and plot data
def calculate_uncertainty(c,type):

    uncertainty_array = np.zeros_like(c['Iota'][0,0])
    uncertainty_array_1 = np.zeros_like(c['Iota'][0,0])

    # Iterate through each data point [row = yaw and col = pitch]
    for row in range(len(c['Iota'][0,0][:,0])):
        for col in range(len(c['Tau'][0,0][0,:])):
            
            # Extract data for the current point
            # 11 centre
            # 12 top
            # 13 bottom
            # 14 right
            # 15 left
            if type == 0:
                current_data = c['P_raw'][0,0][row,col,0,11]
            elif type == 1:
                current_data = c['P_raw'][0,0][row,col,0,12]
            elif type == 2:
                current_data = c['P_raw'][0,0][row,col,0,13]
            elif type == 3:
                current_data = c['P_raw'][0,0][row,col,0,14]
            elif type == 4:
                current_data = c['P_raw'][0,0][row,col,0,15]

                
            pressures =[]
            pressures.append(c['P_raw'][0,0][row,col,0,11])
            pressures.append(c['P_raw'][0,0][row,col,0,12])
            pressures.append(c['P_raw'][0,0][row,col,0,13])
            pressures.append(c['P_raw'][0,0][row,col,0,14])
            pressures.append(c['P_raw'][0,0][row,col,0,15])
            pressures.append(c['P_raw'][0,0][row,col,0,0])
            pressures.append(c['P_raw'][0,0][row,col,0,1])

            # Calculate mean and standard deviation for the current data point
            mean_channel_1 = current_data
            std_dev_channel_1 = 2.5  # Assuming a standard deviation of 1 kPa as an example

            # Define normal distribution for the current data point
            distribution_channel_1 = norm(loc=mean_channel_1, scale=std_dev_channel_1)

            # Run Monte Carlo simulations
            num_simulations = 500
            output_values = []
            output_values_1 = []
            for _ in range(num_simulations):
                # Generate random data point from the normal distribution for the current data point
                random_data_point_channel_1 = distribution_channel_1.rvs()

                if type == 0:
                    pressures[0] = random_data_point_channel_1
                elif type == 1:
                    pressures[1] = random_data_point_channel_1
                elif type == 2:
                    pressures[2] = random_data_point_channel_1
                elif type == 3:
                    pressures[3] = random_data_point_channel_1
                elif type == 4:
                    pressures[4] = random_data_point_channel_1                    
                
                # Run simulation with the random data point and obtain output value
                output_value = calculate_kp(pressures)
                output_value_1 = calculate_ky(pressures)
                output_values.append(output_value)
                output_values_1.append(output_value_1)

            # Assess output distribution
            output_std_dev = np.std(output_values)
            output_std_dev_1 = np.std(output_values_1)

            # Evaluate uncertainty for the current data point
            uncertainty = 2 * output_std_dev  # ±2σ
            uncertainty_1 = 2 * output_std_dev_1  # ±2σ

            # Store uncertainty value in the uncertainty array
            uncertainty_array[row,col] = uncertainty
            uncertainty_array_1[row,col] = uncertainty_1

    fig, ax = plt.subplots()
    set_axes(ax,'Yaw Coefficient','Pitch Coefficient','Kp [\xb0]', 0, 0)
    a1 = ax.contourf(c['C_Alpha'][0,0],c['C_Beta'][0,0]\
                , uncertainty_array, 20, cmap='viridis')
    cbar = fig.colorbar(a1)
    cbar.ax.tick_params(axis='y', labelsize=20)

    fig, ax = plt.subplots()
    set_axes(ax,'Yaw Coefficient','Pitch Coefficient','Kp [\xb0]', 0, 0)
    a2 = ax.contourf(c['C_Alpha'][0,0],c['C_Beta'][0,0]\
                , uncertainty_array_1  , 20, cmap='viridis')
    cbar = fig.colorbar(a1)
    cbar.ax.tick_params(axis='y', labelsize=20)

    plt.show()

    return uncertainty_array