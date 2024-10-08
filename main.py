# Import modules
import numpy as np
import scipy.io
from error_plt import plot_error
from yaw_transform import yaw_trans
from pitch_transform import pitch_trans
from pitch_transform import pitch_trans_side
from plot_map import plot_cont
from re_var import plot_re
from calc_coef import tr_yc
from stencils import set_axes
from new_error import error
from averaging_time import avg_time
from cy_cp import cy_cp
from cy_cp import compare
from yaw_pitch_variation import variations
import matplotlib.pyplot as plt
from coef import change
from montecarlo import calculate_uncertainty
from stencils import flip_sgn
from rotation import rotate_map

# Define main
def main():

    # BIGGEST DATA SET
    
    # MICHAELMAS
    # Specify directory and filename of run to process
    directory = '/Users/vladfilip/Desktop/IIB/Project/Probe_Calibration/Results//'
    # Calibration load
    filename1 = 'Probe 1/FHP_1 _ 5HP_Calib_ns_37 _ 03-Nov-2023 _ New_Machine _ 1 .mat'
    filename2 = 'Probe 2/FHP_1 _ 5HP_Calib_ns_51 _ 03-Nov-2023 _ New_Machine _ 1 .mat'
    filename3 = 'Probe 3/FHP_1 _ 5HP_Calib_ns_50 _ 17-Nov-2023 _ New_Machine _ 1 .mat'
    filename4 = 'Probe 4/ FHP_1 _ 5HP_Calib_ns_51 _ 16-Nov-2023 _ New_Machine _ 1 .mat'
    filename5 = 'Probe 5/ FHP_1 _ 5HP_Calib_ns_50 _ 16-Nov-2023 _ New_Machine _ 1 .mat'
    # Reynolds variation load
    filename120 = 'Probe 1/FHP_1 _ 5HP_Calib_ns_22 _ 15-Nov-2023 _ New_Machine _ 1_20.mat'
    filename160 = 'Probe 1/FHP_1 _ 5HP_Calib_ns_51 _ 13-Nov-2023 _ New_Machine _ 60.mat'

    # LENT
    # 5 degree steps
    filename15 = 'Lent/Probe_1/5 degree steps/ FHP_1 _ 5HP_Calib_ns_29 _ 02-Feb-2024 _ New_Machine _ 1 .mat'
    filename25 = 'Lent/Probe_2/5 degrees/FHP_2 _ 5HP_Calib_ns_29 _ 02-Feb-2024 _ New_Machine _ 1 .mat'
    # 2 degree steps
    filename22_30 = 'Lent/Probe_2/2 degrees/FHP_2_ 5HP_Calib_ns_15 _ 09-Feb-2024 _ New_Machine _ 1.mat'
    # 1 degree steps
    filename11 = 'Lent/Probe_1/1 degree steps/ FHP_1 _ 5HP_Calib_ns_29 _ 08-Feb-2024 _ New_Machine _ 2 .mat'
    #SU
    filename_con = 'Lent/SU/FHP_Con _ 5HP_Calib_ns_15 _ 09-Feb-2024 _ New_Machine _ 1.mat'
    filename_con_check = 'Lent/SU/FHP_Con _ 5HP_Calib_ns_14 _ 23-Feb-2024 _ New_Machine _ 1.mat'
    filename_hem = 'Lent/SU/FHP_Hem _ 5HP_Calib_ns_15 _ 13-Feb-2024 _ New_Machine _ 1.mat'
    filename_norm_1 = 'Lent/SU/ FHP_Norm _ 5HP_Calib_ns_15 _ 14-Feb-2024 _ New_Machine _ 2 .mat'
    filename_nonc = 'Lent/SU/FHP_Non_C _ 5HP_Calib_ns_15 _ 28-Feb-2024 _ New_Machine _ 1.mat'
    filename_nonc_blocked = 'Lent/SU/FHP_NonC _ 5HP_Calib_ns_15 _ 20-Feb-2024 _ New_Machine _ 1.mat'
    filename_side = 'Lent/SU/FHP_Side _ 5HP_Calib_ns_14 _ 19-Feb-2024 _ New_Machine _ 1.mat'

    # Final set of small calibrated probes
    filename12 = 'Lent/Final/Probe_1/FHP_1 _ 5HP_Calib_ns_15 _ 27-Feb-2024 _ New_Machine _ 1 .mat'
    filename22 = 'Lent/Final/Probe_2/FHP_2 _ 5HP_Calib_ns_14 _ 28-Feb-2024 _ New_Machine _ 1.mat'
    filename32 = 'Lent/Final/Probe_3/FHP_3 _ 5HP_Calib_ns_14 _ 28-Feb-2024 _ New_Machine _ 1.mat'
    filename42 = 'Lent/Final/Probe_4/FHP_4 _ 5HP_Calib_ns_15 _ 26-Feb-2024 _ New_Machine _ 1.mat'
    filename52 = 'Lent/Final/Probe_5/FHP_5 _ 5HP_Calib_ns_15 _ 27-Feb-2024 _ New_Machine _ 1.mat'

    # Reynolds Data
    filename12_low = 'Easter/Reynolds/ FHP_1 _ 5HP_Calib_ns_low _ 09-May-2024 _ New_Machine _ 1 .mat'
    filename12_high = 'Easter/Reynolds/ FHP_1 _ 5HP_Calib_ns_high _ 13-May-2024 _ New_Machine _ 1 .mat'

    # SC, Shepherd's Croock
    filename_SC_con = 'Lent/SC/FHP_con_ 5HP_Calib_ns_7 _ 01-Mar-2024 _ New_Machine _ 1.mat'
    filename_SC_hem = 'Lent/SC/FHP_hem _ 5HP_Calib_ns_7 _ 29-Feb-2024 _ New_Machine _ 3.mat'
    filename_SC_norm_1 = 'Lent/SC/FHP_norm_1 _ 5HP_Calib_ns_7 _ 29-Feb-2024 _ New_Machine _ 3.mat' # could be baseline design
    filename_SC_norm_2 = 'Lent/SC/ FHP_Povey _ 5HP_Calib_ns_7 _ 29-Feb-2024 _ New_Machine _ 2 .mat'
    filename_try = 'Lent/SC/ FHP_1 _ 5HP_Calib_ns_7 _ 29-Feb-2024 _ New_Machine _ 2 .mat'
    filename_SC_side = 'Lent/SC/FHP_Side _ 5HP_Calib_ns_7 _ 01-Mar-2024 _ New_Machine _ 1.mat'
    filename_SC_nonc = 'Lent/SC/FHP_SC_Non_C _ 5HP_Calib_ns_7 _ 01-Mar-2024 _ New_Machine _ 1.mat'
    filename_SG_nonc = 'Easter/Non-circular/ FHP_1 _ 5HP_Calib_ns_7 _ 17-May-2024 _ New_Machine _ 1 .mat'
    # SG, stepped geometries
    filename_SC_SG_pyr = 'Lent/SC/SG/FHP_SC_SG_pyr _ 5HP_Calib_ns_7 _ 29-Feb-2024 _ New_Machine _ 1.mat'
    filename_SC_SG_con = 'Lent/SC/SG/FHP_SC_SG_con _ 5HP_Calib_ns_7 _ 29-Feb-2024 _ New_Machine _ 1.mat'

    # AVERAGING TIME
    avg_1 = 'Probe 1/FHP_1 _ Averaging_Time_1500 _ 03-Nov-2023 _ New_Machine _ 1 .mat'
    avg_2 = 'Probe 5/ FHP_2 _ Averaging_Time_1500 _ 02-Feb-2024 _ New_Machine _ 1 .mat'
    avg_3 = 'Probe 3/FHP_1 _ Averaging_Time_1500 _ 08-Nov-2023 _ New_Machine _ 5 .mat'
    avg_4 = 'Probe 4/FHP_1 _ Averaging_Time_1500 _ 08-Nov-2023 _ New_Machine _ 7 .mat'
    avg_5 = 'Probe 5/FHP_1 _ Averaging_Time_1500 _ 10-Nov-2023 _ New_Machine _ 1 .mat'

    # Cleared hole geometry

    # Read the experimental data
    c1 = scipy.io.loadmat(directory + filename12); c1 = c1['c']
    c2 = scipy.io.loadmat(directory + filename22); c2 = c2['c']
    c3 = scipy.io.loadmat(directory + filename_SC_con); c3 = c3['c']
    c4 = scipy.io.loadmat(directory + filename_SC_SG_pyr); c4 = c4['c']
    c5 = scipy.io.loadmat(directory + filename_SC_SG_con); c5 = c5['c']

    # Read the experimental data
    a1 = scipy.io.loadmat(directory + avg_1); a1 = a1['c']
    a2 = scipy.io.loadmat(directory + avg_2); a2 = a2['c']
    a3 = scipy.io.loadmat(directory + avg_3); a3 = a3['c']
    a4 = scipy.io.loadmat(directory + avg_4); a4 = a4['c']
    a5 = scipy.io.loadmat(directory + avg_5); a5 = a5['c']

    # Change Coefficient
    # 0 – Hodson
    # 1 - Minimum
    # 2 - Oxford
    # 3 - Curtis
    c1 = change(c1,2)
    c2 = change(c2,2)
    c3 = change(c3,2)
    c4 = change(c4,2)
    c5 = change(c5,2)

    # Yaw transform
    c1 = yaw_trans(c1)
    c2 = yaw_trans(c2)
    c3 = yaw_trans(c3)
    c4 = yaw_trans(c4)
    c5 = yaw_trans(c5)

    # Rotate 


    # Pitch transform
    c1 = pitch_trans(c1)
    c2 = pitch_trans(c2)
    c3 = pitch_trans(c3)
    c4 = pitch_trans(c4)
    c5 = pitch_trans(c5)

    c2 = rotate_map(c2,1.8)

    plot_error(c1,c2,2,20)


main()








