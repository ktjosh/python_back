"""

filename : HW03_joshi_ketan.py

The program performs one dimensional classifer

Author : Ketan Joshi (ksj4205)
"""
import csv
import matplotlib.pyplot as mp



def InputRead():
    """
    This unction reads input from the specified file, loads the data from the csv file to the applicaton specific lists
    :return:
    """

    #opening an empty list.
    speed_array = []
    recklessness_array = []

    # read from a csv file
    filename = "DATA_v2175_FOR_CLASSIFICATION_using_Threshold.csv"

    #reading the csv file
    with open(filename) as csvfile:
        reader = csv.reader(csvfile,delimiter=",")
        #loading the data into lists
        for rawdata in reader:
            speed_array.append(float(rawdata[0].strip()))
            recklessness_array.append(int(rawdata[1].strip()))

    #print(speed_array)
    Process_data(speed_array,recklessness_array)

def Process_data(raw_speed_array,recklessness_array):
    """
    This function converts the raw data from the csv files to the application specific format. bins the data according
    to the bin size.
    The binned data is processsed to get the exact number of times the driver for that specific speed was caught for
    recklessness or not and load it into a dictionary
    :param raw_speed_array: the raw speed array with floating point value
    :param recklessness_array: the array containing recklessness index, if it is 0 the the driver was not caught for
           recklessnes, if it is 1 then the driver was caught.
    :return:
    """
    rounded_speed_array =[]
    caught_or_not ={}

    #to process all the speed values.
    for index in range (len(raw_speed_array)):

        #we bin the data by rounding it off to the nearest integer
        rounded_speed_array.append( round(raw_speed_array[index]) )

        #check the recklessness bit, whether it is 0 or 1
        if (rounded_speed_array[index]) not in caught_or_not:
            caught_or_not[rounded_speed_array[index]] = [0,0]

        temp = caught_or_not[rounded_speed_array[index]]
        if recklessness_array[index] == 0:
            temp[0] = temp[0] + 1
        else:
            temp[1] = temp[1] + 1
        caught_or_not[rounded_speed_array[index]] = temp

    speed_aray =[] # list for all the unique speed values

    for key in caught_or_not:
        speed_aray.append(key)

    speed_aray.sort() #sorting the speed array
    #print(caught_or_not)

    Classification(speed_aray,caught_or_not)


def Classification(speed_array,caught_or_not):
    """
    This function performs classification on he processed data.
    it considers every speed as a threshold and according to that, it finds out if the driver was caught or not for that
    specific threshold.

    based on that if the driver is not caught according to the threshold and its actually 0 in the csv file, then it is
    true positive.
    if it is below threshold and for that speed it is 1 in csv file then it is false alarm
    if it is above threshold in the csv file and 0 in the csv file, then it is a miss
    and if it is above threshold and it is 1 in the csv file, then it is correctly rejected to be safe
    :param speed_array: it is the sorted unique speed array
    :param caught_or_not: it is a dictionary containing whether the person is caught or not
    :return:
    """

    best_missed_rate =9999999999 #set very high value

    #initialized empty arrays
    threshold_array =[]
    missed_rate_array =[]
    true_positive_array =[]
    false_positive_array =[]

    #initialized the best threshold variable
    best_threshold=0


    #looping for all possible thrshold to findout the lowest missed rate
    for threshold in speed_array:
        num_false_alarm =0
        num_misses=0
        true_positive =0
        true_negative =0

        #checking the threshold for each speed value
        for speed in speed_array:

            #calculating the total number of false alarm, true positive rate , false negative and true negative
            if speed <= threshold:
                num_misses += (caught_or_not[speed])[1]
                true_negative += (caught_or_not[speed])[0]
            else:
                true_positive += (caught_or_not[speed])[1]
                num_false_alarm += (caught_or_not[speed])[0]

        num_wrong = num_misses + num_false_alarm

        #finding the best missed rate and the best threhold
        if num_wrong <= best_missed_rate:
            best_missed_rate = num_wrong
            best_threshold = threshold


        #appending the threshold and missed values into array for plotting
        threshold_array.append(threshold)
        missed_rate_array.append(num_wrong)

        best_threshold_index_array =[]

        #finding out the indices which has the lowest misclassification rate
        for i in range (len(missed_rate_array)):
            if missed_rate_array[i] == best_missed_rate:
                best_threshold_index_array.append(i)

        #calculating the false positive and true positive rate

        if (num_false_alarm + true_negative) == 0:
            false_positive_rate =0
        else:
            false_positive_rate = num_false_alarm / ( num_false_alarm + true_negative )
        if ( true_positive + num_misses ) == 0 :
            true_positive_rate =0
        else:
            true_positive_rate = true_positive /( true_positive + num_misses )


        true_positive_array.append(true_positive_rate)
        false_positive_array.append(false_positive_rate)

    #print(true_positive_array)

    #print("max true positive", max(true_positive_array))
    #print("max fale alarm",max(false_positive_array))
    print("best threshold:",best_threshold)
    print("lowest missed rate:",best_missed_rate)



    #plotting the graph of missed rate vs the threshold
    plot(threshold_array,missed_rate_array,best_threshold_index_array)

    #plotting the roc curve of true positive rate vs false positive rate
    ROC_plot(false_positive_array,true_positive_array,best_threshold_index_array)



def ROC_plot (x,y,best_threshold_index_array):
    """
    Plotting the Roc curve
    :param x: is the  list false positive rate data
    :param y: is the list of true positive rate data
    :param best_threshold_index_array : it is a list containing the indices of points with lowest misclassifiction rate
    :return:
    """

    #50% line for roc curve
    xl =[x[0],x[-1]]
    yl =[y[0],y[-1]]


    mp.plot(xl,yl,'r-',)
    mp.plot(x, y, '.-')

    # title of the plot
    mp.title("ROC Curve")

    # assigning the x label , y label
    mp.xlabel("False Positive rate")
    mp.ylabel("True Positive rate")

    #plotting the points with lowest missclassification rate
    for i in range (len(best_threshold_index_array)):
        index = best_threshold_index_array[i]
        mp.scatter(x[index], y[index], s=100, marker="o", facecolors='none', edgecolors='r')

    mp.show()


def plot(x,y,best_threshold_index_array):
    """
    This function plots the missclassification vs threshold graph
    :param x: is the list of threshold values
    :param y: is the list of misclassification rate values
    :param best_threshold_index_array : it is a list containing the indices of points with lowest misclassifiction rate
    :return:
    """

    #plotting the pyplot
    mp.plot(x, y, '.-')


    #title of the plot
    mp.title("Missclassification as a function of threshold")


    #assigning the x label , y label
    mp.xlabel("Threshold in MPH")
    mp.ylabel("Missclassification ")

    #plotting points with lowest misclassification rate
    for i in range(len(best_threshold_index_array)):
        index = best_threshold_index_array[i]
        mp.scatter(x[index], y[index], s=90, marker="H", facecolors='none', edgecolors='r')

    mp.show()




def main():
    """
    The main function
    :return:
    """

    InputRead()

if __name__ == '__main__':
   main()