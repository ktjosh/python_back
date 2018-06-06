"""

filename : HW02_joshi_ketan.py
This file plots uses otsu's method for 1 D classification

Author : Ketan Joshi (ksj4205)
"""



import csv
import numpy
import math
import matplotlib.pyplot as mp



def inputRead():
    """
    The function reads the csv file , loads the data into a list , converts this to floating point.

    :return:
    """
    #opening an empty list.
    data=[]
    # read from a csv file
    with open("DATA_v2175_FOR_CLUSTERING_using_Otsu.csv") as csvfile:
        reader = csv.reader(csvfile,delimiter=",")
        i=0
        for row in reader:
                data.append( float ( row[0].strip() ) )

    OneDclustering (data)



def OneDclustering(data):
    """
    This algorithm finds the best threshold for which we can seggregate the data into two types safe driver and aggresive
    driver. It puts data into bins and then test the code for each bin to find the best mixed variance .
    The value which gives the best mixed threshold is the best threshold value.
    :param data:
    :return:
    """


    binned_data=[] #floating point data will be converted to int

    #Quantizing the data
    for i in range (0,len(data)):
        binned_data.append(math.floor(data[i]))


    #plots the histogram
    histogram(binned_data)

    #finding the minimum and maximum speed value in the dataset
    min_speed = min (binned_data)
    max_speed = max (binned_data)

    #higher value assigned to best mixed variance
    best_mixed_variance = 99999999
    best_threhold = 0

    #dictionary to fill the fin sizes
    bining ={}

    #creating bins
    for i in range(45,76):
        bining[i]=0

    #for loop which seggregates the speed into bins
    for index in range (len(binned_data)):
        if binned_data [index] in bining :
            count = bining[binned_data[index]]+1
            bining[binned_data[index]] = count

        else:
            bining[binned_data[index]] = 1

    #lists initialized to filled respective values
    under_threshold =[]
    over_threshold  =[]
    mixed_variance_array= []
    threshold_array =[]


    """
    This for loop loops through all the bin values i.e the threshold , which will be tested for mixed variance copies
    to find the best mixed variance to find the best threshold value
    """
    for threshold in range (45,76): #(min_speed,max_speed):

        """
        It loops through all the bin values and divides the speed values into list more than threshold and less than
        threshold
        """
        for keys in bining:
            if keys <= threshold:

                under_threshold = under_threshold + [keys for i in range(bining[keys])]

            else:
                over_threshold = over_threshold + [keys for i in range(bining[keys])]


        # find the variance for the list uder threshld speed and above threshold speed
        if(len(under_threshold) == 0):
            under_variance =0
        else:
            under_variance = numpy.var(under_threshold)
        if(len(over_threshold)==0):
            over_variance=0
        else:
            over_variance  = numpy.var(over_threshold)

        # finding the mixed variance
        mixed_variance = ( (over_variance * len(over_threshold)) + (under_variance * len(under_threshold)) ) / len(binned_data)


        #sets the best mixed variance values
        if mixed_variance < best_mixed_variance:
            best_mixed_variance = mixed_variance
            best_threhold = threshold

        #filling the list of mixed variance threshold values
        mixed_variance_array.append(mixed_variance)
        threshold_array.append(threshold)

        #reassigning the lists
        under_threshold =[]
        over_threshold =[]

    print("Best speed threshold is :", best_threhold)

    #plotting the graph of y- mixed variance vs x - threshold
    plot(threshold_array,mixed_variance_array)



def histogram(binned_data):
    """
    This function plots the hisogram of the data passed (a list)
    :param binned_data: data of the speed
    :return:
    """

    mp.title("Histogram of speeds with bin size = 1 mph (45 to 75)") #title of the  plot

    mp.xlabel("Speed in mph") #x label
    mp.ylabel("Frequency of the bins")    #y label

    mp.hist(binned_data,bins=range(45,76),rwidth=0.7) #plotting the  histogram

    mp.show()


def plot(x,y,):
    """
    This function plots the mixed variance vs threshold graph
    :param x: x list to be plotted
    :param y: y list to be plotted
    :return:
    """

    #plotting the pyplot
    mp.plot(x, y, '.-')

    #title of the plot
    mp.title("Mixed Variance vs Threshold")


    #assigning the x label , y label
    mp.xlabel("Threshold")
    mp.ylabel("Mixed variance")

    mp.show()


def main():
    """
    main function
    :return:
    """
    inputRead()




if __name__ == '__main__':
    main()