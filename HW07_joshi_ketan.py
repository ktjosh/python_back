"""
filename:

Author:  Ketan Joshi (ksj4205)
"""

import pandas as panda
import math
import numpy as np
import csv
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

def InputRead():
    """
    The file reads the input from the csv file, store it in a panda Dataframe
    and then calls the clustering method to perfrom clustering
    :return:
    """

    filename = "HW_AG_SHOPPING_CART_v512.csv"

    shopping_data = panda.read_csv(filename,index_col='ID')

    #stripping the spaces, converting all upercase to lowercase
    headers = ((shopping_data.columns.str.upper()).str.lower()).str.strip()
    shopping_data.columns = headers

    PerformClustering(shopping_data)





def PerformClustering(shopping_data):
    """
    This function calculates the Croscorrelation matrix
    :param shopping_data:
    :return:
    """


    corr = shopping_data.corr()


    print("The Cross-correlation matrix is:")
    print(corr)
    print()



    findclusters(shopping_data)




def findclusters(shopping_data):
    """
    The function performs clusting shopping dsta data frame and returns the set of clusers.
    :param shopping_data:  The data frame containing all the data
    :return:
    """

    rows = {} #dictionary for saving each row from the data frame
    count= {} # to keep count of points in every cluster

    last_10_cluster =[]

    for i in range(1,101):
        rows[i] = shopping_data.ix[i].values
        count[i]=1

    clust = set()

    #while loop where all the clustering is performed
    while len(rows)>1:
        minimum = 99999
        arg1 = 0
        arg2 = 0
        for rowi in rows:
            for rowj in rows:
                if(rowi!=rowj):
                    dist = Euclidean_Distance(rows[rowi],rows[rowj])
                    if(minimum > dist):
                        arg1 = rowi
                        arg2 = rowj
                        minimum = dist

        row1 = rows[arg1]
        row2 = rows[arg2]
        ct1 = count[arg1]
        ct2 = count[arg2]
        row_avg = Average(row1,row2,ct1,ct2)

        #once the cluster is formed the original data points are popped
        rows.pop(arg1)
        rows.pop(arg2)
        count.pop(arg1)
        count.pop(arg2)

        s = str(arg1)+"-"+str(arg2)
        clust.add(s)
        rows[s]  = row_avg
        count[s] = ct1+ct2
        minval = min (ct1,ct2)

        if(len(rows)<11):
            last_10_cluster.append(minval)


    print("The last 10 minimum cluster sizes are")
    for val in last_10_cluster:
        print(str(val))

    myDendrogram(shopping_data)



def myDendrogram(shopping_data):
    """
    The function takes the shopping data and plots the dendrogram from it
    :param shopping_data:  Data frame of the shopping data.
    :return:
    """
    dataframe = shopping_data.values
    Z = hierarchy.linkage(dataframe, 'centroid')
    plt.figure()
    plt.xlabel('Node ID')
    plt.ylabel('Euclidean distance')
    plt.title('Agglomerative Clustering')
    dn = hierarchy.dendrogram(Z)
    plt.show()


def Average(arg1,arg2,ct1,ct2):
    """
    function finds weighted average of two nd arrays
    :param arg1: nd array 1 containing centroid of the cluster
    :param arg2: ndarray 2  containing centroid of the cluster
    :param ct1: count of elements in cluster one
    :param ct2: count of elements in cluster two
    :return: nd array giving new centroid of combined cluster
    """

    a = (arg1*ct1 + arg2*ct2)/(ct1+ct2)
    return a


def Euclidean_Distance(arr1,arr2):
    """
    finds Euclidean distance between two data points
    :param arr1: ndarray of point one
    :param arr2: ndarray of point two
    :return: returns the scalar distance
    """
    sum1=0
    for i in range (len(arr1)):
        sum1 = sum1 + math.pow((arr1[i]-arr2[i]),2)

    sum1 = math.pow(sum1,0.5)

    return sum1

def main():
    """
    main function
    :return:
    """
    InputRead()


if __name__ == '__main__':
    main()