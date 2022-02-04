# -*- coding: utf-8 -*-
"""
Bouncy Ball Asignment 

Calculates the number of bounces a ball makes given the initial and minimum height and the bounce efficiency.
It also calculates the time taken for the bouncec to occur, stating when the ball is dropped and finishing at the end of the last bounce, when it hits the ground
Also gives the option to see the maximum height reached on each bounce, and gives the option to show a graph plotting the decay in the height of the bounces against time.

Lauren Pearson 18/10/19
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
        print('The minimum height must be a number. ')   
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
    Calculates the number of bounces the ball makes using the conversion of gravitational potential energy and bounce efficiency
    minimum_height (float)
    initial_height (float)
    bounce_efficiency (float)
    
    Lauren Pearson 18/10/19
    """
    bounces = np.log(minimum_height/initial_height)/np.log(bounce_efficiency)
    return bounces


x = bounce_calculator(minimum_height, initial_height, bounce_efficiency)
no_of_bounces=math.floor(x) #rounds bounces down to complete bounces


t=[]
h=[]
for n in range(1, no_of_bounces+1):
    """
    This finds the height reached by the ball on each subsequent bounce.
    n is the bounce number, so this finds the height for each bounce up to the number of the complete bounces.
    This then calculates the time taken for each bounce.
    """
    new_heights=(initial_height * bounce_efficiency**n)
    
    time_bounces = 2*(((2 * new_heights)/gravity)**0.5)
    
    h.append(new_heights) #makes an list of the heights reached on each bounce after the first drop
    
    t.append(time_bounces) #makes a list of the time taken on each bounce after the first drop
    
    
time_first_drop = ((2*initial_height)/gravity)**0.5     
time_taken = time_first_drop + sum(t) #calculates the total time taken for all the bounces to happen, up to the end of the last bounce


if no_of_bounces == 0:
    #if no bounces occur, this is printed and the program stops
    print('The ball makes',no_of_bounces, 'complete bounce between',initial_height, 'm and ',minimum_height,'m. ')

elif no_of_bounces == 1:
    #prints 'complete bounce' for singular bounce
    print('The ball makes',no_of_bounces, 'complete bounce between',initial_height, 'm and ',minimum_height,'m in {0:3.2f} seconds.'.format(time_taken))

else:
    #prints 'complete bounces' for multiple bounces
    print('The ball makes',no_of_bounces, 'complete bounces between',initial_height, 'm and ',minimum_height,'m in {0:3.2f} seconds.'.format(time_taken))


if no_of_bounces >= 1:
    height_question = input('Would you like to know the height of each bounce? Please enter "yes" or "no": ')
    if height_question in {'yes'}:
        for n in range(1, no_of_bounces+1):
            new_heights = (initial_height * bounce_efficiency**n)
            print('{0:3.2f}'.format(new_heights) + 'm') #prints the max height of each bounce in a list

    
graph_question = input('Would you like to see a graph of the decay in maximum bounce heights? Please enter "yes" or "no": ')
if graph_question in {'yes'}:
    t.insert(0, time_first_drop) #adds the first drop time to the list of times for each subsequent bounce
    cumulative_times = np.cumsum(t) #adds up the bounce times cumulatively in a list

    h.insert(0, initial_height) #adds the initial height to the list of max bounce heights
    
    plt.plot([cumulative_times], [h], 'xb') #plots a scatter graph of the maximum heights of each bounce against time
    plt.xlabel('Time (s)')
    plt.ylabel('Maximum Height (m)')
    plt.title('The decay of maximum bounce height for the ball against time')
    plt.show