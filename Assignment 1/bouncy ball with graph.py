# -*- coding: utf-8 -*-
"""
Bouncy Ball Asignment 

Lauren Pearson 11/10/19

Calculates the number of bounces a ball makes and the time taken for the bounces given the initial and minimum height and the bounce efficiency.
Also gives the option to see the maximum height reached on each bounce
"""

import numpy as np
import math
import matplotlib.pyplot as plt

gravity = 9.81 #assume on Earth

while True: #input of initial height, returning errors for invalid inputs
    try:
        initial_height = float(input('At what height, in metres, do you drop the ball from? '))
    except:
        print('The initial height must be a number. ')
        continue
    if initial_height <= 0:
        print('The initial height must be greater than 0. ')
        continue
    else:
        break
    
while True: #input of minimum height, returning errors for invalid inputs
    try:
        minimum_height = float(input('What is the minimum height that the ball must reach in metres? ' ))
    except:
        print('The minimum height must be  a number. ')   
        continue
    if minimum_height > initial_height:
        print('The minimum height must be less than the drop height. ') 
        continue
    elif minimum_height <= 0:
        print('The minimum height must be greater than 0. ') 
        continue
    else:
        break
    
while True: #input of bounce efficiency, returning errors for invalid inputs
    try:
        bounce_efficiency = float(input('What is the efficiency of the bounce? '))
    except:
        print('The bounce efficiency must be  a number. ')
        continue
    if not 0 < bounce_efficiency < 1:
        print('The bounce efficiency must be between 0 and 1. ')
        continue
    else:
        break


def bounce_calculator(minimum_height, initial_height, bounce_efficiency):
    """
    Calculates the number of bounces the ball makes
    """
    bounces = np.log(minimum_height/initial_height)/np.log(bounce_efficiency)
    return bounces

x = bounce_calculator(minimum_height, initial_height, bounce_efficiency)

no_of_bounces=math.floor(x) #rounds bounces down to complete bounces


a=[]
h=[]
for n in range(1, no_of_bounces+1):
    """
    This finds the height reached by the ball on each subsequent bouce and calculates the time taken for each bounce.
    n is the bounce number, so this finds the height for each bounce up to the number of the complete bounces.
    """
    new_heights=(initial_height * bounce_efficiency**n)
    
    time_bounces = 2*(((2 * new_heights)/gravity)**0.5)
    
    h.append(new_heights)
    
    a.append(time_bounces) 
    
    
time_first_drop = ((2*initial_height)/gravity)**0.5     
time_taken = time_first_drop + sum(a) #calculates the time taken for all the bounces to happen, up to the end of the last bounce


if no_of_bounces == 0:
    #if no bounces occur, this is printed and the program stops
    print('The ball makes',no_of_bounces, 'complete bounce above', minimum_height, 'm. ')

elif no_of_bounces == 1:
    #prints 'complete bounce' for singular bounce
    print('The ball makes',no_of_bounces, 'complete bounce above', minimum_height, 'm in {0:3.2f} seconds.'.format(time_taken))

else:
    #prints 'complete bounces' for multiple bounces
    print('The ball makes',no_of_bounces, 'complete bounces above', minimum_height, 'm in {0:3.2f} seconds.'.format(time_taken))


if no_of_bounces >= 1:
    height_question = input('Would you like to know the height of each bounce? Please enter "yes" or "no": ')
    if height_question in {'yes'}:
        for n in range(1, no_of_bounces+1):
            new_heights = (initial_height * bounce_efficiency**n)
            print('{0:3.2f}'.format(new_heights) + 'm')

    
    
graph_question = input('Would you like to see a graph of the decay in maximum bounce heights? Please enter "yes" or "no": ')
if graph_question in {'yes'}:
    a.insert(0, time_first_drop) #adds the first drop time to the list of time for each subsequent bounce
    cumulative_times = np.cumsum(a) #adds up the bounce times cumulatively

    h.insert(0, initial_height) #adds the initial height to the list of max bounce heights

    plt.plot([cumulative_times], [h])
    plt.xlabel('Time (s)')
    plt.ylabel('Maximum Height (m)')
    plt.title('The decay of maximum bounce height for the ball against time')
    plt.show