"""
filename: HW08_joshi_ketan.py

Author: Ketan Joshi (ksj4205)
"""

import pandas as panda
import numpy as np
from numpy import linalg
import math
import matplotlib.pyplot as mp
from sklearn.cluster import KMeans


def InputRead():
    """
    The file reads the input from the csv file, store it in a panda Dataframe
    and then calls the clustering method to perfrom clustering
    :return:
    """

    filename = "HW_AG_SHOPPING_CART_v5121.csv"

    shopping_data = panda.read_csv(filename,index_col='ID')

    #stripping the spaces, converting all upercase to lowercase
    headers = ((shopping_data.columns.str.upper()).str.lower()).str.strip()
    shopping_data.columns = headers


    StartTheProcess(shopping_data)





def StartTheProcess(shopping_data):
    """
    This function takes input as the panda dataframe. It finds the covariance matrix of the data frame.Based on that it
    finds the eigen vectors representing the Data.

    Once eigen vecors ae found, it finds the two highest eigen values , and projects data on the two vectors with
    corresponding highest absolute eigen values.

    Once we get the 2-D projection , we perform K means clustering on the Data.

    :param shopping_data: dataframe object of the data
    :return:
    """

    #calculating the ovariance matrix
    cov_mat = Calculate_covariance_matrix(shopping_data)
    cov_mat_val = cov_mat.get_values()

    #finding eigen vector from the covariance natrix
    eigenVals,eigenVect = linalg.eig(cov_mat_val)

    abs_eigen_vals =[]

    # the eigen vectors are the columns in the list.
    eigenVect = eigenVect.transpose()

    for vals in eigenVals:
        abs_eigen_vals.append(math.fabs(vals))

    abs_eg = {}

    eg_vect = {}
    #associating eigen values to the vetor and eigen values to its absolute values
    for i in range(0, len(abs_eigen_vals)):
        abs_eg[abs_eigen_vals[i]] = eigenVals[i]

        eg_vect[eigenVals[i]] = eigenVect[i]


    abs_eigen_vals.sort( reverse=True)


    """
    for i in range(0,2):
        j = abs_eigen_vals[i]
        print(eg_vect[j])
    """

    #finding the two highest eigen vectors
    highest_vect1 = eg_vect[abs_eg[abs_eigen_vals[0]]]
    highest_vect2 = eg_vect[abs_eg[abs_eigen_vals[1]]]

    #printing them
    print("highest vector 1"+str(highest_vect1.tolist()))
    print("highest vector 2"+str(highest_vect2.tolist()))
    print("\n")

    #plotting the graph of cumulative sum vs the normalized eigen values
    plotthegraph(abs_eigen_vals)

    #finding the scatter plot of 2-D projected data.
    x,y = scatterplot(highest_vect1,highest_vect2,shopping_data)

    #plotting k means on the data
    centr = plot_kmeans(x,y)

    vect=[]


    for i in range (len(centr)):
        print("cluster "+str(i+1)+" :["+str(centr[i][0])+" ,"+str(centr[i][1])+"]")
        x_hv1 = centr[i][0]*highest_vect1
        y_hv2 = centr[i][1]*highest_vect2
        vect.append((x_hv1+y_hv2))

    print("\n")
    for i in range(len(vect)):
        print("Vector "+str(i)+":"+str(list(vect[i])))
    #print(vect)

def scatterplot(highest_vect1, highest_vect2,shopping_data):
    """
    projecting the data points on the two eigen vectors and plotting a scatter plot
    :param highest_vect1: vector with highest absolute eigen value
    :param highest_vect2: Vector with 2nd highest absolute eigen value
    :param shopping_data: the data frame containing the data points.
    :return: returns the x and y coordinate of the 2D projected data.
    """
    #findting the dot product of eigen vector and data point.
    x = shopping_data.dot(highest_vect1)
    y = shopping_data.dot(highest_vect2)

    mp.title("2-D plot of the Projected Values")
    mp.xlabel("1st Highest Vector Projection")
    mp.ylabel("2nd Highest Vector Projection")
    mp.scatter(x,y)
    mp.show()

    return x,y

def plotthegraph(abs_eigen_vals):
    """
    function plots the graph of normalized eigen values vs cumulative sum of vectors
    :param abs_eigen_vals: dictiorty containing absolute eigen values and the eigen values
    :return:
    """
    cum_vect_val =0

    for keys in abs_eigen_vals:
        cum_vect_val += keys

    cum_vect_arr =[]
    cum_vect_arr.append(0)
    key =0
    total_vals = []
    total_vals.append(0)
    i =1;

    #for loop normalizing each value
    for keys in abs_eigen_vals:
        key += keys
        val = key / cum_vect_val
        cum_vect_arr.append(val)
        total_vals.append(i)
        i+=1

    #plotting the graph
    mp.xlabel("Number of Eigen Vectors ")
    mp.ylabel("Cumulative Sum of Normalized Eigen values")
    mp.title("Cumulative sum of Noramalized Eigen vector vs Number of Vectors")
    mp.plot(total_vals,cum_vect_arr,'.-')
    mp.show()


def plot_kmeans(x, y):
    """
    Function perfroms K means clusting on the data
    :param x: nd-array X coordinates of the data
    :param y: nd-array Y coordinates of the data
    :return: returns the cluster centres formed
    """
    num_cluster =3

    #forming a new data frame
    X = panda.DataFrame({

        'x':x,
        'y': y

    })

    #perfoming K-means clusering
    kmeans = KMeans(n_clusters=num_cluster, init='k-means++', n_init=10, max_iter=500, tol=0.0001,
                    precompute_distances='auto', verbose=0,).fit(X)



    #plotting the data and cluster centres
    mp.scatter(x,y,c='',edgecolors='black')
    mp.xlabel("1st Highest Vector Projection")
    mp.ylabel("2nd Highest Vector Projection")
    for i in range(num_cluster):
        mp.scatter(kmeans.cluster_centers_[i][0],kmeans.cluster_centers_[i][1], c='red',edgecolors='blue')

    mp.title("K means Plot")
    mp.show()


    return kmeans.cluster_centers_


def Calculate_covariance_matrix(shopping_data):
    """
    calculates the covariance matrix and returns it
    :param shopping_data: data frame of the data
    :return: returns the covariance matrix
    """

    return shopping_data.cov()



def main():
    """
    main function
    :return:
    """
    InputRead()

if __name__ == '__main__':
    main()
