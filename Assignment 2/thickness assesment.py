# -*- coding: utf-8 -*-
"""
Lauren Pearson 15/11/19

Thickness of Boron nitride assignment


"""

import numpy as np
import matplotlib.pyplot as plt

e_r = 4.0
e_0 = 0.00553
m_h = 0.512317
V_0 = 3.0

def float_validation(trans_coeff, energy, trans_coeff_error):
    """
    Validates whether the data in the file are floats and are
    in the correct range and rejects errorr or invalid values
    """
    try:
        float(trans_coeff)
        float(energy)
        float(trans_coeff_error)
    except ValueError:
        return False

    if 0 <= float(trans_coeff) <= 1 and 0 <= float(energy) <= 1 and 0 <= float(trans_coeff_error) <= 1:
        return True
    else:
        return False
      
        
def chi_squared(data, calculated_data, data_error):
    """
    calculates the chi squared for each line of data compared to the best fit line
    """
    return ((data-calculated_data)/data_error)**2     
    
def equation_7(energy):
    
    return np.exp(-2 * (d_2-d_1) * m_h * (V_bar - energy)**0.5)


data_open = False

try:
    input_file = open('Tunnelling_data_BN.csv', 'r')
    data_open = True    
except:
    print('Could not open file. ')
   
    
if data_open:
    data = np.zeros((0,3))
    skipped_first_line = False 

    for line in input_file:
        
        if not skipped_first_line:
            skipped_first_line = True
        
        else:
            linesplit = line.split(',')
            
            if float_validation(linesplit[0], linesplit[1], linesplit[2]) == False:
                print('Invalid data, line removed')
           
            else:
                temp = np.array([])
                temp = np.append(temp, float(linesplit[0]))
                temp = np.append(temp, float(linesplit[1]))
                temp = np.append(temp, float(linesplit[2]))
                data = np.vstack((data,temp))

    input_file.close()
    
    y = data[:,0]
    x = data[:,1]
    error = data[:,2]
    
    # function plot

    d = 90
    d_1 = (0.15 * np.exp(2) * np.log(2))/(np.pi * e_r * e_0 * V_0)
    d_2 = d - d_1

    V_bar = V_0 - (((1.15 * np.exp(2) * np.log(2))/(8 * np.pi * e_r * e_0 * (d_2 - d_1))) * np.log((d_2 * (d - d_1))/(d_1 * (d - d_2))))
    
    plt.plot(x, equation_7(x))
    
    
    
    V0 = 1
    
    
    
    
    degrees_of_freedom = len(data[:,0])-1 
    
    chi_2 = chi_squared(y, equation_7(x), error)
    reduced_chi_2 = np.sum(chi_2/degrees_of_freedom) 
  
    
    
        

    #plot graph
    plt.errorbar(x, y, error, fmt = 'x', label = 'data')
    plt.legend(bbox_to_anchor=(1.22,0.99))
    plt.xlabel('Energy (eV)')
    plt.ylabel('Transmission Coefficient')
    plt.show

    



