"""
Author :Ketan Joshi (ksj4205)

filename: HW10_joshi_ketan.py

file trains the knn classier to find the best value of k.
"""

import csv
import math


import pandas as panda
import matplotlib.pyplot as mp



def Load_Data():
    """
    This function loads the data into lists of attribute 1
    attribute 2 and target data
    :return:
    """
    filename = "C:\\Users\\ketan\\PycharmProjects\\exam\\HW_kNN__DATA_v060.csv"


    x1=[]
    x2=[]
    target_data =[]

    # reading the csv file
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        # loading the data into lists
        for rawdata in reader:
            x1.append(float(rawdata[0].strip()))
            x2.append(float(rawdata[1].strip()))
            target_data.append(int(rawdata[2].strip()))

    Partition(x1, x2, target_data)

def Partition(x1, x2, target_data):
    """
    Teh data here partitioned to get 10 sets of the data which will be used for
    10 fold classification
    :param x1: is list of 1st parameter of the training data
    :param x2: is list of 2nd parameter of the training data
    :param target_data: is the target class which will be used for determing whether it is classified correctly or not
    :return:
    """

    # dividing the data into chunks
    # finding the chunk size
    chunk_size = math.floor(len(x1)/10)
    data=[]
    chunk=[]


    for i in range (len(x1)):

        if (len(x1)-i)< chunk_size :
            while i < len(x1):
                p = (x1[i], x2[i], target_data[i])
                chunk.append(p)
                i += 1

            data.append(chunk)
            #print(len(chunk))
            break
        p = (x1[i], x2[i], target_data[i])
        chunk.append(p)

        if (i+1)% chunk_size ==0:
            data.append(chunk)
            chunk=[]

    Perform_KNN(data)

def Perform_KNN(Data):
    """
    this function will train knn classifier to find the best value of k
    :param Data: data is a list of tuple, each tuble has (att1,att2,target class)
    :return:
    """

    # list to store accuracy value for each k
    classification_rate_for_k=[]
    k_values =[1,3,5,7,9,11]

    # for loop which will take an entry from the first partition
    # it will be used to find the distances with points in all other partitions
    # out of those distance best k will be taken to perform classificatoion

    # loop runs for all value of k
    for k in k_values:

        correct_count = 0
        correctcly_classified = []
        incorrectly_classified = []

        # loop for each partition
        for i in range (len(Data)):
            #print(Data[i])

            # loop for each entry in the current partition
            for entry in Data[i]:
                #print(entry)

                Eu_dist = []
                # loop will be tested for all other partition
                for j in range (len(Data)):

                    # if statement to check if it is not checked against its own partition
                    if i!=j:

                        for data_items in Data[j]:
                            dist = GiveMeEuclidianDistance(entry,data_items)
                            Eu_dist.append((dist,data_items))


                sorted_list = sorted(Eu_dist, key=lambda tup: tup[0])


                sorted_list = sorted_list[:k]
                class0_count=0
                class1_count=0
                majority_class = 0

                # checking in best k distances
                for items in sorted_list:
                    if (items[1][2]==0):
                        #print(items[1][2])
                        #exit(56)
                        class0_count+=1
                    else:
                        class1_count+=1

                # deciding the majority class
                if class0_count>class1_count:
                    majority_class=0
                else:
                    majority_class=1

                # checking if classified correctly or not
                if entry[2]==majority_class:
                    correct_count+=1
                    correctcly_classified.append(entry)
                else:
                    incorrectly_classified.append(entry)

        classification_rate_for_k.append((correct_count/2803))
        corrx=[]
        corry=[]
        Incorrx=[]
        Incorry=[]

        # adding correctly and incorrectly classified data
        for tupless in correctcly_classified:
            corrx.append(tupless[0])
            corry.append(tupless[1])

        for tuplesss in incorrectly_classified:
            Incorrx.append(tuplesss[0])
            Incorry.append(tuplesss[1])

        Scatter_plot(corrx,corry,Incorrx,Incorry,k)
    print("K values")
    print(k_values)
    print("Correctly classified points associated with K values")
    print(classification_rate_for_k)
    Plot_Kvs_Accuracy(k_values,classification_rate_for_k)





def Scatter_plot(correctx, correcty,Incorrectx,Incorrecty,k):
    """
    this function plots the scatter plot
    :param correctx: correctlu classified x coordinate of points
    :param correcty: correctlu classified 0y coordinate of points
    :param Incorrectx: incorrectlu classified x coordinate of points
    :param Incorrecty: incorrectlu classified y coordinate of points
    :param k:  k value used
    :return:
    """
    mp.scatter(correctx,correcty,c='',edgecolors='pink')
    mp.scatter(Incorrectx, Incorrecty, c='', edgecolors='green')
    mp.title("Plotting correctly and Incorrectly Classified for K = "+str(k)+"\n Correct = Pink , Incorrect = Green")
    mp.xlabel("X1")
    mp.ylabel("X2")
    mp.show()





def Plot_Kvs_Accuracy(k,Accurary):
    """
    this function plits the graph of accuracy vs K value
    :param k: list of k values used
    :param Accurary: list of accuracy value for each of the k
    :return:
    """
    mp.plot(k, Accurary,'.-')
    mp.xlabel("K Values")
    mp.ylabel("Correctly Classified Values")
    mp.title("K vs Accuracy plot")
    mp.show()






def GiveMeEuclidianDistance(p1,p2):
    """
    this function calculates euclidean distance between two points and returns
    :param p1: tubple of point 1 (att1,att2,target class)
    :param p2: tubple of point 2 (att1,att2,target class)
    :return: returns euclidean distance between two points
    """
    xdist = p1[0]-p2[0]
    ydist = p1[1]-p2[1]

    dist = math.pow((xdist**2+ydist**2),0.5)

    return dist






def main():
    """
    main function
    :return:
    """
    Load_Data()



if __name__ == '__main__':
    main()