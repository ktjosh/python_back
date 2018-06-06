"""
file name: HW00_joshi_ketan.py
author : ketan joshi (ksj4205)

"""

import math
import matplotlib.pyplot  as mp


def plot(x,y,best_fluxrate,best_speed):
    """
    Te cuntion plots the curve using matplot lib
    :param x: an array of x coordinate
    :param y: an array of y coordinates
    :param best_fluxrate: the best flux rate of a car
    :param best_speed: the speed for which best fluxrate
    :return:
    """
    mp.plot(x, y, '.-')

    mp.xlim( [0 , 120] ) #sets the x limit
    mp.ylim( [0 , 900] ) #sets the y limit

    mp.title("Flux Rate of cars")

    mp.axhline( y=best_fluxrate , xmin=0 , xmax=(best_speed / 120 ) )
    mp.axvline( best_speed , 0 , best_fluxrate/900 )

    mp.xlabel("Speed in mph/ hr")
    mp.ylabel("Number of cars / hr")

    mp.show()



def calculate_fluxrate():
    """
    the function calculates the reaction time for the cars, based on that it finds the safety gap and based on that it
    calculates flux rate.
    :return:
    """
    alpha = 0.0055 #constant
    default_reaction_time =4 #default reaction
    y =[]
    x =[]
    x.append(0)
    y.append(0)
    best_fluxrate = 0
    best_speed = 0

    for speed in range (1,121):

        reaction_time = alpha * ( speed*speed ) #reaction time based on formula

        #the actual reaction time is the time is the maximum of default time and calculated reaction time
        actual_reaction_time = max( reaction_time , default_reaction_time )

        #the car packing density will be the distance between car andthe length of the car  which is 10 here.
        car_packing_density = ( (speed*5280*actual_reaction_time)/(60*60) ) +10

        #we calculate the car will take to cover the car packing density.
        time_to_cover_carpacking_density = ( car_packing_density*3600 ) / ( speed*5280 )

        #number of cars that will pass through the road will be how many cars cover the car packing distance in an hour.
        number_of_cars = (3600 / time_to_cover_carpacking_density )

        #we add the data to our x and y array.
        y.append(math.floor(number_of_cars))
        x.append(speed)

        #if statement to find the best flux rate and speed for that rate.
        if number_of_cars>best_fluxrate:
            best_fluxrate =math.floor(number_of_cars)
            best_speed = speed

    plot(x,y,best_fluxrate,best_speed)

def main():
    """
    main function
    :return:
    """
    calculate_fluxrate()
if __name__ == '__main__':
        main()
