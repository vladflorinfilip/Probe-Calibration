import numpy as np
from scipy.ndimage import rotate

def rotate_and_crop(matrix, angle):
    # Rotate the matrix
    rotated_matrix = rotate(matrix, angle=angle, reshape=False)

    # Calculate the center of the original and rotated matrices
    original_center = np.array(matrix.shape) // 2
    rotated_center = np.array(rotated_matrix.shape) // 2

    # Calculate the cropping box
    start = rotated_center - original_center
    end = start + np.array(matrix.shape)

    # Crop the rotated matrix to the original shape
    cropped_matrix = rotated_matrix[start[0]:end[0], start[1]:end[1]]

    return cropped_matrix

def rotate_map(c,angle):

    c['C_Alpha'][0,0] = rotate_and_crop(c['C_Alpha'][0,0],angle)
    c['C_Beta'][0,0] = rotate_and_crop(c['C_Beta'][0,0],angle)
    c['C_P'][0,0] = rotate_and_crop(c['C_P'][0,0],angle)
    c['C_Po'][0,0] = rotate_and_crop(c['C_Po'][0,0],angle)
    return c

