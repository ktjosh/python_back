"""

file name : HW05_joshi_keyan_trainer.py
This file is decision tree program that trains a writes another Decision tree program which is the classifier.

Author : Ketan Joshi (ksj4205)
"""


import pandas as pd
import csv



def InputRead(file):
    """
    The function reads the data from the .csv file and loads it into the memory
    :param file: it the file object in which , the decision tree program will be written
    :return:
    """


    indices =[] #list to keep track of all the data points to be considered.

    # read from a  specified csv file
    filename = "Recipes_For_Release_2175_v201.csv"

    #reading the csv file
    with open(filename) as csvfile:
        reader = csv.reader(csvfile,delimiter=",")
        #loading the data into lists
        boo = True
        data = {}
        attribute_names=[]
        for rawdata in reader:
            if(boo):
                for type in rawdata:
                    if type !="":
                        data[type.strip()] = []
                        attribute_names.append(type.strip())
                boo = False
            else:
                for index in range (len(attribute_names)):
                    if index == 0:
                        data[attribute_names[index]].append(rawdata[index])
                    else:
                        data[attribute_names[index]].append(float(rawdata[index]))

    #appending all the indices
    for i in range(len(data[attribute_names[1]])):
        indices.append(i)

    #calling the function to create the decision tree
    CalculateDecisionTree(file,attribute_names,data,indices,2,"C")


def CalculateDecisionTree(file,attribute_names , data,indices,level,LorR):
    """
    The function calculates the best attribute to create the split, when the attribute is found, it will split the tree
    based on that attrbute into left and right sub tree. To do so, when the best attribute found, it will call the the
    function for the lest and right subpart recursively.
    :param file: It is file object, in which the decision tree will write.
    :param attribute_names: it is the list of names of all the attributes.
    :param data: It is a dictionary which contain all the coulmns values of the attributes.
    :param indices: it is list containing all the indices which are to be considered for the given sub tree
    :param level: it is the level of the tree, at which the current recursive call is.
    :param LorR: It is the attribute which tells the call is for the left or the right subtree
    :return:
    """
    tab = "\t"

    #Initializing all the variables.
    best_gini=9
    best_thresh =0
    best_att_name =""
    typeC = "cupcake"
    typec = "Cupcake"
    typem = "muffin"
    typeM = "Muffin"
    greater_muffin =0
    smaller_muffin =0
    greater_cupcake =0
    smaller_cupcake = 0

    #initialzing the  indices to be considered for the left and right subtree recursive call.
    new_lesser_indices =[]
    new_greater_indices =[]

    #names of all the attributes
    type = data[attribute_names[0]]

    #for loop which iterates through all the attributes to find the one with lowest weighted gini index

    for index in range (1,len(attribute_names)):
        gini,val = CalulateIpurity(type,data[attribute_names[index]],indices)

        #comparision to find the best gini
        if best_gini >= gini:
            best_gini = gini
            best_thresh = val
            best_att_name = attribute_names[index] # contains names of all the attribute

    #getting the column of the best attribute
    best_att_col = data[best_att_name]

    #finding the number of instances which belong to either muffin or cupcake and are lower or greater than threshold
    for i in indices :
        if best_att_col[i] <= best_thresh:
            if type [i] == typeC or type[i] == typec :
                smaller_cupcake+=1
            elif type[i]== typem or type[i] == typeM :
                smaller_muffin += 1
            new_lesser_indices.append(i)

        else:
            if type [i] == typeC or type[i] == typec :
                greater_cupcake+=1
            elif type[i]== typem or type[i] == typeM :
                greater_muffin += 1
            new_greater_indices.append(i)

    #tab spaces used for the indentation
    tab_spaces = tab * level


    #*** If part of decision tree
    spaces = tab * level

    string = 'if attributes["'+str(best_att_name)+'"]<='+ str(best_thresh)+ ":\n"
    string = spaces+string
    file.write(string)

    recurse,winner =ShouldRecurse(smaller_cupcake, smaller_muffin)

    #decision is made whether to recurse or not for the LEFT SUBTREE
    if recurse:
        CalculateDecisionTree(file,attribute_names, data, new_lesser_indices, level+1,"L")
    else:

        str2 = spaces+tab+"file.write('"+winner+"\\n')\n"
        file.write(str2)


    #*** Else part of Decision tree
    str1 = spaces+"else:\n"
    file.write(str1)


    recurse, winner =ShouldRecurse(greater_cupcake,greater_muffin)

    #decision is made whether to recurse or not for the RIGHT SUBTREE
    if recurse:
        CalculateDecisionTree(file,attribute_names, data, new_greater_indices, level+1,"R")

    else:
        # return target variable
        str2 = spaces + tab +"file.write('" + winner + "\\n')\n"
        file.write(str2)




    

def CalulateIpurity(type,att_col,indices):
    """
    the function returns the weigheted gini index of the attribute sent
    :param type: contains the name of the attribute
    :param att_col: contains the coulmn of the attribute, meaning value of that attribute for each row.
    :param indices: contains the list of indices i.e. rows to be considered
    :return:  returns a touple : lowest gini index, and the threshold for which it is the lowest.
    """

    
    typeC = "cupcake"
    typec = "Cupcake"
    typem = "muffin"
    typeM = "Muffin"

    #finds the minimum and maximum value of the data.
    minI = int(min(att_col))
    maxI = int(max(att_col))
    min_gini = 999999999
    best_thresh = 0

    #finds the best threshold for which, the gini index is lowest.
    for index in range (minI,maxI+1):

        typeL1 =0
        typeL2 =0
        typeG1 =0
        typeG2 = 0
        threshold = index

        for i in indices:
            if att_col[i]<= threshold:
                if type[i] == typeC or type[i] == typec:
                    typeL1 +=1
                else:
                    typeL2 +=1
            else:
                if type[i] == typeC or type[i] == typec:
                    typeG1 +=1
                else:
                    typeG2 +=1

        #if rows satisfy the condition then addition will be zero and we will get divide by zero error.
        if (typeL2 + typeL1)!= 0:
            fracL = (typeL1 /( typeL2 + typeL1 ))**2 + (typeL2 /( typeL2 + typeL1 ))**2
        else:
            fracL =0.5
        if (typeG2 + typeG1)!= 0:
            fracG = (typeG1 /( typeG2 + typeG1 ))**2 + (typeG2 /( typeG2 + typeG1 ))**2
        else:
            fracG = 0.5



        total = typeL1 + typeL2 + typeG1 + typeG2

        #finds gini for the left and right partition
        gini1 = 1 - fracL
        gini2 = 1 - fracG

        if total!=len(indices):
            print("false")

        #finds the weighted gini
        wtd_gini = (((typeL1 + typeL2)/ total ) * gini1 )+ (((typeG1 + typeG2) / total) * gini2)



        #if statement to find the best gini.
        if min_gini >= wtd_gini:
            min_gini = wtd_gini
            best_thresh = threshold

    return min_gini,best_thresh


def ShouldRecurse(Cupcake_count, Muffin_count):
    """
    This functionchecks if 95% of the data belong to one class or not. if yes the it sends false meaning the calling
    function should not recurse. Otherwise it should recurse.
    :param Cupcake_count: the totl cupcake counts
    :param Muffin_count: the total muffin counts
    :return: returns a tuple of boolean and the class which has greater value
    """
    n = max(Cupcake_count, Muffin_count)
    per = n /(Cupcake_count + Muffin_count)

    c = "0"
    m = "1"
    winner = c if Cupcake_count>Muffin_count else m
    if per>0.95:
        return False,winner
    else:
        return True,winner

def Writeprolog(file):
    """
    This function writes the prolog
    :param file: the file object of the file to be written in
    :return:
    """
    file.write('""" \n\nFile name : HW05_joshi_ketan_Classifier.py\n'
               'This file is a decision tree program that classifies recipes into cupcakes and muffins\n\n'
               'Author: Ketan Joshi (ksj4205)\n\n"""')


def Writefunction(file):
    """
    This function writes the clssification function in the file to be written
    :param file: it is the file object
    :return:
    """
    file.write('\n\ndef Doclassification():\n\n\n')
    file.write('\tfile1 = open("Recipes_For_VALIDATION_2175_RELEASED_v201.csv","r")\n')
    file.write('\tfile = open("HW05_joshi_ketan_MyClassification.csv","w")\n')
    file.write("\talline = file1.readlines()\n")
    file.write("\tattributes={}\n")
    file.write("\tname = []\n")
    file.write("\tattributes_name = alline[0].split(',')\n")
    file.write("\tfor att in attributes_name:\n")
    file.write("\t\tattributes[att]=0\n")
    file.write("\t\tname.append(att)\n")
    file.write("\tfor index in range(1,len(alline)):\n")
    file.write("\t\tline = alline[index].split(',')\n")
    file.write("\t\tline=line[0:26]\n")
    file.write("\t\tfor i in range(1,len(line)):\n")
    file.write("\t\t\tattributes[name[i]]= float(line[i])\n")





def Writemain(file):
    """
    function to write the main function in the classifier file.
    :param file:
    :return:
    """
    file.write("\ndef main():\n")
    file.write("\tDoclassification()\n\n")
    file.write("\nif __name__ == '__main__':\n")
    file.write("\tmain()")



def main():
    """
    The maiin function
    :return:
    """
    file = open("HW05_joshi_ketan_classifier.py",'w')
    Writeprolog(file)
    Writefunction(file)
    InputRead(file)
    Writemain(file)
    file.close()

if __name__ == '__main__':
    main()