# Import modules
import numpy as np

# This function calculates specific pressure coefficient
# Based on Treaster and Yocum (1997)
# Hodson and Dominy
# 11 centre
# 12 top
# 13 bottom
# 14 right
# 15 left
def tr_yc(c,i):

    P_mean = 0.25* (c['P_raw'][0,0][:,:,0,11] + c['P_raw'][0,0][:,:,0,12] + c['P_raw'][0,0][:,:,0,13] + c
                    ['P_raw'][0,0][:,:,0,15])
    
    coef = (c['P_raw'][0,0][:,:,0,i] - c['P_raw'][0,0][:,:,0,0])/(P_mean-c['P_raw'][0,0][:,:,0,1])



    return coef