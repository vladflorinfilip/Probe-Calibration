# Function to change Hodson coefficients to Curtis as defined in
# https://iopscience.iop.org/article/10.1088/1361-6501/aa53a8/pdf

def change(c,type):

    # 11 centre
    # 12 top
    # 13 bottom
    # 14 right
    # 15 left
    if type == 0:
        pass
    
    if type == 1: 

        # Oxford with min

        for k in range(len(c['P_raw'][0,0][:,0,0,11])):
            for j in range(len(c['P_raw'][0,0][0,:,0,11])):
                P_avg = min(c['P_raw'][0,0][k,j,0,12],c['P_raw'][0,0][k,j,0,13],c['P_raw'][0,0][k,j,0,14],c['P_raw'][0,0][k,j,0,15])
                    
        
                P_mean = 0.25* (c['P_raw'][0,0][k,j,0,12] + c['P_raw'][0,0][k,j,0,13] + c['P_raw'][0,0][k,j,0,14] + c['P_raw'][0,0][k,j,0,15])
        
                c['C_Beta'][0,0][k,j] = c['C_Beta'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_Alpha'][0,0][k,j] = c['C_Alpha'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_P'][0,0][k,j] = c['C_P'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_Po'][0,0][k,j] = c['C_Po'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)

    if type == 2: 

        # Oxford with half of the mins in the two directions (pitch,yaw)

        for k in range(len(c['P_raw'][0,0][:,0,0,11])):
            for j in range(len(c['P_raw'][0,0][0,:,0,11])):
                P_avg = 0.5 * (min(c['P_raw'][0,0][k,j,0,12],c['P_raw'][0,0][k,j,0,13]) + min(c['P_raw'][0,0][k,j,0,14],c['P_raw'][0,0][k,j,0,15]))
                    
        
                P_mean = 0.25* (c['P_raw'][0,0][k,j,0,12] + c['P_raw'][0,0][k,j,0,13] + c['P_raw'][0,0][k,j,0,14] + c['P_raw'][0,0][k,j,0,15])
        
                c['C_Beta'][0,0][k,j] = c['C_Beta'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_Alpha'][0,0][k,j] = c['C_Alpha'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_P'][0,0][k,j] = (P_avg - c['P_raw'][0,0][k,j,0,1]) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_Po'][0,0][k,j] = c['C_Po'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)

    if type == 3: 

        # Curtis

        for k in range(len(c['P_raw'][0,0][:,0,0,11])):
            for j in range(len(c['P_raw'][0,0][0,:,0,11])):
                P = sorted([c['P_raw'][0,0][k,j,0,12],c['P_raw'][0,0][k,j,0,13],c['P_raw'][0,0][k,j,0,14],c['P_raw'][0,0][k,j,0,15]])
                P_h = 0.5 * (P[3]+P[2])
                P_l = 0.5 * (P[1]+P[0])
                P_max = 0.666 * c['P_raw'][0,0][k,j,0,11] + 0.334 * P_h

                P_mean = 0.25* (c['P_raw'][0,0][k,j,0,12] + c['P_raw'][0,0][k,j,0,13] + c['P_raw'][0,0][k,j,0,14] + c['P_raw'][0,0][k,j,0,15])

                c['C_Beta'][0,0][k,j] = c['C_Beta'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (P_max - P_l)
                c['C_Alpha'][0,0][k,j] = c['C_Alpha'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (P_max - P_l)
                c['C_P'][0,0][k,j] = c['C_P'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (P_max - P_l)
                c['C_Po'][0,0][k,j] = c['C_Po'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (P_max - P_l)

    if type == 4: 

        # Side

        for k in range(len(c['P_raw'][0,0][:,0,0,11])):
            for j in range(len(c['P_raw'][0,0][0,:,0,11])):
                P_avg = 0.5 * (min(c['P_raw'][0,0][k,j,0,12],c['P_raw'][0,0][k,j,0,13]) + min(c['P_raw'][0,0][k,j,0,14],c['P_raw'][0,0][k,j,0,15]))
                    
        
                P_mean = 0.25* (c['P_raw'][0,0][k,j,0,12] + c['P_raw'][0,0][k,j,0,13] + c['P_raw'][0,0][k,j,0,14] + c['P_raw'][0,0][k,j,0,15])
        
                c['C_Beta'][0,0][k,j] = c['C_Beta'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)/(c['P_raw'][0,0][k,j,0,12] - c['P_raw'][0,0][k,j,0,13]) * (c['P_raw'][0,0][k,j,0,11]-c['P_raw'][0,0][k,j,0,13])
                c['C_Alpha'][0,0][k,j] = c['C_Alpha'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_P'][0,0][k,j] = c['C_P'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)
                c['C_Po'][0,0][k,j] = c['C_Po'][0,0][k,j] * (c['P_raw'][0,0][k,j,0,11] - P_mean) / (c['P_raw'][0,0][k,j,0,11] - P_avg)


    return c