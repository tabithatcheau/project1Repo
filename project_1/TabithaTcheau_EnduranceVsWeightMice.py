#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# imports
import sys
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
from scipy.stats import linregress

class MiceData():

    def __init__(self, mice_list, mouse_number):

        self.model = self._buildGraphs(mice_list, mouse_number)

       
    def _buildGraphs(self, mice_list, mouse_number):

        i = 0
        KO_num = 0
        for mouse in mice_list:

            if mouse.knock_type == "KO":
                KO_num = KO_num + 1

        x1 = np.zeros(KO_num)
        y1 = np.zeros(KO_num)

        x2 = np.zeros(mouse_number - KO_num)
        y2 = np.zeros(mouse_number - KO_num)
    
        i = 0
        KO_num = 0
        for mouse in mice_list:

            if mouse.knock_type == "KO":

                x1[KO_num] = mouse.weight
                y1[KO_num] = mouse.endurance
                KO_num = KO_num + 1

            else:

                x2[i - KO_num] = mouse.weight
                y2[i - KO_num] = mouse.endurance

            i = i + 1            
        
        # plot the data with linregress and return ax, fig (KO mice)
        stats = linregress(x1,y1)
        m1 = stats.slope
        b1 = stats.intercept

        fig1,ax1 = plt.subplots()
        plt.plot(x1, m1 * x1 + b1, color="red")
        plt.scatter(x1,y1)

        ax1.set_xlabel('Weight in grams')
        ax1.set_ylabel('Endurance in minutes')
        ax1.set_title('Endurance vs weight of KO mice')

        # plot the data with linregress and return ax, fig (WT mice)
        stats = linregress(x2,y2)
        m2 = stats.slope
        b2 = stats.intercept

        fig2,ax2 = plt.subplots()
        plt.plot(x2, m2 * x2 + b2, color="red")
        plt.scatter(x2,y2)

        ax2.set_xlabel('Weight in grams')
        ax2.set_ylabel('Endurance in minutes')
        ax2.set_title('Endurance vs weight of WT mice')

        # compute means
        mean_x1 = np.mean(x1)
        mean_y1 = np.mean(y1)
        tot_x1 = np.sum(x1)
        tot_y1 = np.sum(y1)

        mean_x2 = np.mean(x2)
        mean_y2 = np.mean(y2)
        tot_x2 = np.sum(x2)
        tot_y2 = np.sum(y2)

        mean_x_tot = np.mean(np.concatenate((x1,x2),axis=0))
        mean_y_tot = np.mean(np.concatenate((y1,y2),axis=0))

        tot_x = np.sum(np.concatenate((x1,x2),axis=0))
        tot_y = np.sum(np.concatenate((y1,y2),axis=0))

        return {"fig1":fig1,"ax1":ax1, "fig2":fig2, "ax2":ax2, 
        "mean_x1":mean_x1, "mean_y1":mean_y1, "mean_x2":mean_x2, 
        "mean_y2":mean_y2, "mean_x_tot":mean_x_tot, "mean_y_tot":mean_y_tot, 
        "tot_x1":tot_x1, "tot_y1":tot_y1, "tot_x2":tot_x2, "tot_y2":tot_y2, 
        "tot_x":tot_x, "tot_y":tot_y}
    
#Class Mouse with attribute weight and endurance for each mouse type
class Mouse():

    def __init__(self, **argdict):

        self.knock_type = argdict.get("knock_type", None)
        self.weight = argdict.get("weight", 0)
        self.endurance = argdict.get("endurance",0)

#Class MiceLab with attributes number of mice       
class MiceLab():

    def __init__(self, **argdict):

        self.mouse_number = argdict.get("mouse_number", 0)
        self.mice_list = argdict.get("mice_list", [])
        self.Mice_data = MiceData(self.mice_list, self.mouse_number)

#Empty dictionary that will later take in the KO (knockout) mouse's weight and endurace, which the user will input
KO_endurance = {}
#Empty dictionary that will later take in the WT (wild type) mouse's weight and endurace, which the user will input
WT_endurance = {}

Select = ['KO', 'WT']

#The possible weight to input for each mouse will be between 1 and 1000 grams. This is an unrealistically "generous" range!
Weight_range = [*range(1,1000,1)]

#Initialize type
Type = 'KO'

#Initialize variables
count = 0
mice_list = []

totalWeightWT=0
totalWeightKO=0
totalEnduranceWT=0
totalEnduranceKO=0

total_mice_number = 0

#Input from the user
#WT stands for wild type; these mice have the functioning gene.
#KO stands for knockout; these mice lack the functioning gene.
while True:
    unformattedType = input("Select either WT or KO mouse: ")
    Type = unformattedType.upper() #the user can input lowercase or uppercase
   
    #The inputted mouse type needs to be either KO or WT, or user will be re-prompted.
    if Type in Select:
        break
    else:
        print("Not a valid option.")
       
while count<2:
    print("You've selected mouse of type:", Type)
    N = input("Enter number of mice of selected type: ")
   
    #if letter is entered, the user will recieve invalid note and be re-prompted.
    while True:
        try:
            N = int(N)
            break
        except:
            print("Invalid entry. Please enter integer value")
            N = input("Enter number of mice of selected type: ")
   
    for i in range(1,N+1):
        while True:
            Weight=input("Enter weight in grams of {} mouse: ".format(Type))
           
            #if letter is entered, the user will recieve invalid note and be re-prompted.
            while True:
                try:
                    Weight = int(Weight)
                    break
                except:
                    print("Invalid entry. Please enter integer value")
                    Weight = input("Enter the weight in grams of {} mouse: ".format(Type))
                   
            #The mouse needs to weigh at least 1 gram, and no more than 1000 grams, as defined by Weight_range        
            if Weight in Weight_range:
                #Computing total weight for each mouse type
                if (Type == "KO"):
                    totalWeightKO += Weight
                else:
                    totalWeightWT += Weight
                break
            #If user inputs weight that is not in range (1 gram to 1000 grams), the user will be re-prompted to input weight again.
            else:
                print('Not a valid option.')
        print("The weight in grams of {} mouse: {}".format(Type, Weight))
        Endurance = input("Enter the duration in minutes of the run: ")
        while True:
            try:
                Endurance = int(Endurance)
                if (Type == "KO"):
                    totalEnduranceKO += Endurance
                else:
                    totalEnduranceWT += Endurance
                break
            except:
                print("Invalid entry. Please enter integer value")
                Endurance = input("Enter the duration in minutes of the run: ")
           
        print ("The endurance in minutes of {} mouse: {}".format(Type, Endurance))
       
        #Assign the values to the key
        if (Type == 'KO'):
            KO_endurance[i] = Weight, Endurance
            print (KO_endurance)

        else:
            WT_endurance[i] = Weight, Endurance
            print (WT_endurance)
        
        current_mouse = Mouse(knock_type = Type, weight = Weight, endurance = Endurance)

        # append the current_mouse into a mouse_list
        mice_list.append(current_mouse)
           
    #After inputting the weight and endurance values for all mice of the first selected type,
    #the second mouse type the user selects must be the other type, or the user will be re-prompted.    
    if(count<1):
        Select.remove(Type)
        while True:
            unformattedType2 = input('Select new mouse type: ')
            Type2 = unformattedType2.upper()
            if Type2 in Select:
                break
            elif (Type2==Type):
                print("You already entered {}".format(Type))
            else:
                print("Not a valid option.")
               
      
    count+=1
    Type = Type2

    total_mice_number = total_mice_number + N
    continue

# need total mice, and then save to MiceLab object
Laboratory = MiceLab(mouse_number = total_mice_number, mice_list = mice_list)

#Display the average weights and endurances for WT mice and KO mice
print("The average weight in grams of WT mice: {0:8.2f}".format(Laboratory.Mice_data.model["mean_x2"]))
print("The average weight in grams of KO mice: {0:8.2f}".format(Laboratory.Mice_data.model["mean_x1"]))
print("The average endurance in minutes of WT mice: {0:8.2f}".format(Laboratory.Mice_data.model["mean_y2"]))
print("The average endurance in minutes of KO mice: {0:8.2f}".format(Laboratory.Mice_data.model["mean_y1"]))

# extract fig and ax, and plot them
fig1 = Laboratory.Mice_data.model["fig1"]
ax1 =  Laboratory.Mice_data.model["ax1"]
fig2 = Laboratory.Mice_data.model["fig2"]
ax2 =  Laboratory.Mice_data.model["ax2"]

# show
plt.show()

