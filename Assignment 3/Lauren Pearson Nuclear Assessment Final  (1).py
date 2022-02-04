# -*- coding: utf-8 -*-
"""
Nuclear Decay Assessment

Determines the half-lives and decay constants for rubidium79 and strontium79.
Also determines the uncertainties on these values.

Reads in data, combines two separate data files and validates data for faulty measurements.
Performs a minimised chi squared fit for the activity of rubidium against the data, dependent on to parameters, the decay constants of rubidum79 and strontium79.
Produces a graph of the data and the reduced chi squared line for the decay constant values.
Also produces a contour plot of the reduced chi squared values.
Saves the plots as png files.

Lauren Pearson 13/12/19
"""
import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as pc
from scipy.optimize import fmin
from scipy.optimize import curve_fit

#defining constants
n_sr_0 = 1e-6 * pc.Avogadro
#statting values for the fitting
lambda_rb_start = 0.0005
lambda_sr_start = 0.005

""" Functions """

def import_file(file_name):
    """
    Imports a file, replaces any non-float values with 'nan' and skips the header
    
    file_name(string)
    """
    imported_data = np.genfromtxt(file_name, delimiter = ',', skip_header = 1)
    return imported_data

    
def activity_calculator(time, lambda_rb, lambda_sr):
    """
    Calculates the activity of Rubidium based on nuclear decay equations
    
    time(float)
    lambda_Rb(float)
    lambda_Sr(float)
    """
    n_rb = n_sr_0 * (lambda_sr / (lambda_rb - lambda_sr)) * (np.exp(-lambda_sr * time) - np.exp(-lambda_rb * time))
    activity = lambda_rb * n_rb
    return activity


def half_life_calculator(lambdas):
    """
    Calculates the half life of an isotope based on the decay constant lambda for that isotope
    Converts the hald life to minutes
    
    lambdas(float)
    """
    half_life_time = np.log(2)/(lambdas * 60)
    return half_life_time


def half_life_error(lambda_values, lambda_errors):
    """
    Calculates the error on the half life
    Equation found by performing error propagation on the equation for the half life in minutes
    
    lambda_values(float)
    lambda_errors(float)
    """
    error = (np.log(2)/(lambda_values**2*60))*lambda_errors
    return error


def chi_squared_function(values):
    """
    Calculates the chi squared for data for varous values of decay constants for Rb and Sr
    data is a 2D array composed of rows of [time, activity and uncertainties]
    
    values(float)
    """
    rb, sr = values
    chi_squared = np.sum(((data[:,1]-activity_calculator(data[:,0], rb, sr))/data[:,2])**2)
    return chi_squared


def chi_squared(rb, sr):
    """
    Returns chi squared for data for a mesh of decay constant values for Rb and Sr
    data is a 2D array composed of rows of [time, activity and uncertainties]

    rb(mesh)
    sr(mesh)
    """
    #chi_square = (((activity_calculator(data[:,0], rb, sr) - data[:,1])/data[:,2])**2)
    chi_square = 0
    for entry in data:
        chi_square += ((activity_calculator(entry[0], rb, sr) - entry[1])/entry[2])**2
    return chi_square


""" Main Code """

#importing data, correcting the units and removing nan values
data = np.concatenate((import_file('Nuclear_data_1.csv'),import_file('Nuclear_data_2.csv')))
data = data[np.argsort(data[:,0])]

data[:,0] *= 3600
data[:,1] *= 1e12
data[:,2] *= 1e12

data[data==0] = 'nan'
data = data[~np.isnan(data).any(axis=1)]

#fitting data first time
fit_results_1 = fmin(chi_squared_function, (lambda_rb_start, lambda_sr_start), full_output = True, disp = False)
[lambda_rb_1,lambda_sr_1] = fit_results_1[0]

#removing anomalies
for i in range(len(data)):
    if abs(activity_calculator(data[i][0], lambda_rb_1, lambda_sr_1)-data[i][1]) > 3*data[i][2]:
        data[i][1] = 'nan'
        
data = data[~np.isnan(data).any(axis=1)]

#running fit again to find actual lamba values
fit_results_2 = fmin(chi_squared_function, (lambda_rb_start, lambda_sr_start), full_output = True, disp = False)
[lambda_rb_2,lambda_sr_2] = fit_results_2[0]


#error calculation based on a curve fit
starting_values = [lambda_rb_start, lambda_sr_start]
popt,pcov = curve_fit(activity_calculator, data[:,0], data[:,1], starting_values, sigma = data[:,2], absolute_sigma = True)
perr = np.sqrt(np.diag(pcov))

[lambda_rb_error, lambda_sr_error] = perr

#half life errors based on decay constant errors
half_life_rb_error = half_life_error(lambda_rb_2,lambda_rb_error)
half_life_sr_error = half_life_error(lambda_sr_2,lambda_sr_error)



#plotting the graph
graph = plt.figure()

axes = graph.add_subplot(111)

axes.plot(data[:,0], activity_calculator(data[:,0], lambda_rb_2, lambda_sr_2), c = '#D300FF', label = 'Minimised chi squared line', zorder = 2)
axes.errorbar(data[:,0], data[:,1], data[:,2], fmt = 'x', c = '#30B26B', label = 'Data', zorder = 1)
axes.legend(bbox_to_anchor=(1,1))
axes.set_xlabel('Time (s)')
axes.set_ylabel('Activity (Bq)')
axes.set_title('Activity against time for rubidium')

plt.savefig('activity_graph.png', dpi = 300)

plt.show()



print('The decay constant for Rubidium is {:.3g}'.format(lambda_rb_2), '\u00B1 {:.2g}'.format(lambda_rb_error), 's\u207b\u00b9.')
print('The decay constant for Strontium is {:.3g}'.format(lambda_sr_2), '\u00B1 {:.2g}'.format(lambda_sr_error), 's\u207b\u00b9.')
print('The half life of Rubidium is {:.3g}'.format(half_life_calculator(lambda_rb_2)), '\u00B1 {:.2g}'.format(half_life_rb_error), 'minutes.')
print('The half life of Strontium is {:.3g}'.format(half_life_calculator(lambda_sr_2)), '\u00B1 {:.1g}'.format(half_life_sr_error), 'minutes.')

reduced_chi_2 = fit_results_2[1]/(len(data)-2)
print('The reduced chi squared for the minimised chi squared line is {:3.2f}.'.format(reduced_chi_2))


#contour plot of chi squared values for various decay constants
lambda_rb_values = np.linspace(0.00041, 0.0006, 500)
lambda_sr_values = np.linspace(0.0029, 0.009, 500)
lambda_rb_values_mesh, lambda_sr_values_mesh = np.meshgrid(lambda_rb_values, lambda_sr_values)

chi_squared_levels = (fit_results_2[1] + 1, fit_results_2[1] + 2.30, fit_results_2[1] + 5.99, fit_results_2[1] + 9.21)

initial_figure = plt.figure()

contour_plot = initial_figure.add_subplot(111)
contour_plot.scatter(lambda_rb_2, lambda_sr_2, label = 'Minimum')
parameter_plot = contour_plot.contour(lambda_rb_values_mesh, lambda_sr_values_mesh, chi_squared(lambda_rb_values_mesh,  lambda_sr_values_mesh), colors=['#00813B', '#009BFF', '#3600FF', '#FF00D8'], levels = chi_squared_levels)
contour_plot.legend(bbox_to_anchor=(1,1))
contour_plot.set_xlabel('Rb decay constant values (s\u207b\u00b9)')
contour_plot.set_ylabel('Sr decay constant values (s\u207b\u00b9)')
contour_plot.set_xlim(0.00049,0.00053)
contour_plot.set_ylim(0.0045, 0.00575)
contour_plot.set_title(r'$\chi^2$ contours against parameters.')
contour_plot.clabel(parameter_plot, fontsize = 9)
labels = ['Minimum',r'$\chi^2_{{\mathrm{{min.}}}}+1.00$', r'$\chi^2_{{\mathrm{{min.}}}}+2.30$',r'$\chi^2_{{\mathrm{{min.}}}}+5.99$',r'$\chi^2_{{\mathrm{{min.}}}}+9.21$']

#allowing the ledgend to move with the plot depending of the size
box = contour_plot.get_position()
contour_plot.set_position([box.x0, box.y0, box.width * 0.7, box.height])
for i in range(len(labels)):
    contour_plot.collections[i].set_label(labels[i])
    
contour_plot.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize = 14)

plt.savefig('contour_plot.png', dpi = 400)

plt.show()
