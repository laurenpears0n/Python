# -*- coding: utf-8 -*-
"""
Thickness of Boron nitride assignment

Finds the thickness of a sample of Boron nitride by analysing the fraction of electrons that tunnel through
Reads in the data file, validates data to remove errors and values outside of permitted range
Compares the data to a fitted line for different values of thicknesses to minimise chi squared
Plots a graph of the data and the minimised chi squared line
Prints the result for thickness in Angstroms and reduced chi squared to appropriate precision and calculates the number of layers thick the BN is

Lauren Pearson 22/11/19
"""

import numpy as np
import matplotlib.pyplot as plt

#defining constants
h_bar_sqrt_two_m = 0.512317
vacuum_permittivity = 0.00553
V_0 = 3
relative_permittivity = 4

#defining values for hill climbing
initial_d = 2.5
step = 0.0001
tolerance = 0.00001

def float_validation(transmission_coefficient, energy, transmission_coefficient_error):
    """
    Validates whether the data in the file are floats or strings and rejects strings
    Also validates whether consistent with the range of data and rejects anomalies. 
    
    transmision_coefficient(string or float)
    energy(string or float)
    transmission_coefficient_error(string or float)
    
    Lauren Pearson 22/11/19
    """
    
    try:
        float(transmission_coefficient)
        float(energy)
        float(transmission_coefficient_error)
    except ValueError:
        return False

    if 0 <= float(transmission_coefficient) <= 1 and 0 <= float(energy) <= 1 and 0 <= float(transmission_coefficient_error) <= 1:
        return True
    else:
        return False
     
       
def chi_squared_calculator(data, calculated_data, data_error):
    """
    Calculates the chi squared for each line of data compared to calculated data
    
    data(float)
    calculated_data(float)
    data_error(float)
    
    Lauren Pearson 22/11/19
    """
    chi_squared = ((data-calculated_data)/data_error)**2 
    return chi_squared
   

def transmission_coefficient_calculation(energy, d):
    """
    Calculates the transmission coefficient for each energy data value given for a value of thickness
    
    energy(float)
    d(float) 
    
    Lauren Pearson 22/11/19
    """
    d_1 = (1.2 * np.log(2))/(8 * np.pi * relative_permittivity * vacuum_permittivity * V_0)
    d_2 = d - d_1
    average_potential = V_0 - ((1.15 * (np.log(2)/(8 * np.pi * relative_permittivity * vacuum_permittivity))/(d_2-d_1)) * np.log((d_2*(d - d_1))/(d_1*(d - d_2))))
    transmission_coefficient_value = np.exp(-2*(d_2-d_1)*h_bar_sqrt_two_m*(average_potential - energy)**0.5)
    return transmission_coefficient_value
    

def no_of_layers(d):
    """
    Calculates the number of layers of BN present given one layer is approximately 3 Angstoms thick
    
    d(float)
    
    Lauren Pearson 22/11/19
    """
    layers = d/3
    return layers

#open data file and check if file exists
data_open = False

try:
    input_file = open('Tunnelling_data_BN.csv', 'r')
    data_open = True    
except:
    print('Could not open file. ')
   
#extract the data to an array line by line and remove invalid lines   
if data_open:
    data = np.zeros((0,3))

    for line in input_file:
        
        lines = line.split(',')
           
        if float_validation(lines[0], lines[1], lines[2]) == False:
            print('Invalid data, line removed')
           
        else:
            temp = np.array([])
            temp = np.append(temp, float(lines[0]))
            temp = np.append(temp, float(lines[1]))
            temp = np.append(temp, float(lines[2]))
            data = np.vstack((data,temp))

    input_file.close()
       
    #find d based on hill climbing to minimise chi squared
    d = initial_d
    difference = np.sum(chi_squared_calculator(data[:,0], transmission_coefficient_calculation(data[:,1], d), data[:,2]))
    
    while difference > tolerance:
        
        comparison_0 = np.sum(chi_squared_calculator(data[:,0], transmission_coefficient_calculation(data[:,1], d), data[:,2]))
    
        comparison_1 = np.sum(chi_squared_calculator(data[:,0], transmission_coefficient_calculation(data[:,1], d + step), data[:,2]))
        
        comparison_2 = np.sum(chi_squared_calculator(data[:,0], transmission_coefficient_calculation(data[:,1], d - step), data[:,2]))
        
        if comparison_0 > comparison_1:
            difference = comparison_0 - comparison_1
            d += step
            
        elif comparison_0 > comparison_2:
            difference = comparison_0 - comparison_2
            d -= step
        else:
            break  
    
    print('The fitted value for the thickness d of Boron nitride is {:3.3f}'.format(d), '\u212B')
    print('This is {:3.3f}'.format(no_of_layers(d)), ' layers thick.')


    #reduced chi squared calculation
    degrees_of_freedom = len(data)-1
    reduced_chi_2 = np.sum((chi_squared_calculator(data[:,0], transmission_coefficient_calculation(data[:,1],d), data[:,2])))/degrees_of_freedom
    print('The reduced chi squared for this line is {:3.2f}.'.format(reduced_chi_2))


    #plot graph
    plt.errorbar(data[:,1], data[:,0], data[:,2], fmt = 'x', c = '#30B26B', label = 'Data')
    plt.plot(data[:,1], transmission_coefficient_calculation(data[:,1], d), c = '#B90076', label = 'Minimised chi squared line')
    plt.legend(bbox_to_anchor=(1.01,0.99))
    plt.grid(True)
    plt.title('Graph to Find Thickness of Boron Nitride', fontsize = 13)
    plt.xlabel('Energy (eV)')
    plt.ylabel('Transmission Coefficient')
    plt.show
