'''
Created on Jan 28, 2019

@author: austinp
'''
import random
import numpy as np
import matplotlib.pyplot as plt

class Traffic(object):

    def __init__(self, roadLength, carDensity):         # Initialize a new road
        self.newRoad(roadLength, carDensity)
    
    def newRoad(self, roadLength, carDensity):          # Initialize a new road
        self.road = [0] * roadLength                    # Creating a blank road
        self.carsInit = []
        self.avgSpd = 0                                 # Defaulting average speed
        
        for i in range(int(carDensity * roadLength)):   # Randomize car placement based on car density
            r = random.randint(0, roadLength - 1)
            while r in self.carsInit:
                r = random.randint(0, roadLength - 1)
            self.carsInit.append(r)
                
        for i in self.carsInit:
            self.road[i] = 1
    
    def __str__(self):                                          # Return string representation of road
        return str(self.road)
    
    def moveIter(self, curr, iteration, **kwargs):              # Repeatedly move cars recursively
        nex = curr
        if iteration > 0:
            if kwargs.get("debug"):                             # Printing road and iteration number for debugging purposes
                print(str(nex) + " " + str(iteration))
            if kwargs.get("showSpd"):                           # Printing average speed of current iteration/time step
                print(self.avgSpd)
            
            nex = self.moveCars(curr)
            return self.moveIter(nex, iteration - 1, **kwargs)  # Recursive call
        return nex                                              # Default call, only called on last iteration
    
    def moveCars(self, curr):                                   # Moving of cars
        currLength = len(curr)
        nex = [0] * currLength
        carsMoved = 0
        numCars = 0
        for x in curr:                                          # Count number of cars on road
            if x == 1:
                numCars += 1
                
        for i in range(len(curr)):                              # Move cars based on cars in front or behind
            if curr[i] == 1:
                if curr[(i+1) % currLength] == 1:
                    nex[i] = 1
                else:
                    nex[i] = 0
            elif curr[i] == 0:
                if curr[(i+currLength-1) % currLength] == 1:
                    nex[i] = 1
                    carsMoved += 1
                else:
                    nex[i] = 0
        self.avgSpd = 0                                         # Default average speed
        if numCars > 0:
            self.avgSpd = carsMoved / numCars
        return nex
    
    def steadySpd(self, curr):                                  # Calculate steady speed of a given road
        self.moveIter(curr,len(curr))                           # Recurse until steady speed has been established
        return self.avgSpd
    
    def graphSpd(self):                                         # Graph speed as a function of density
        x = np.linspace(0, 1, len(self.road))                   # Initialize axes
        y = []
        
        for i in x:                                             # Y axis is steady speed at each density
            self.newRoad(len(self.road), i)
            y.append(self.steadySpd(self.road))
        
        plt.plot(x, y)                                          # Plot x and y axes
        plt.xlabel("Car Density")
        plt.ylabel("Steady Speed")
        plt.show()
    
    def graphPos(self, iterations):                                     # Graph position as a function of time
        x = np.linspace(0, iterations, iterations)                      # Graphing position based on inputed road
        y = []
        xx = []
        
        for i in x:                                                     # Plotting road with position of cars vertically
            temp = self.moveIter(self.road, i)
            for j in range(len(temp)):
                if temp[j] == 1:
                    xx.append(i)                                        # Each car in a given road has the same x coordinate (time step)
                    y.append(j)
        
        plt.plot(xx, y, marker = ".", color = "k", linewidth = "0")     # Plot axes
        plt.xlabel("Time")
        plt.ylabel("Position")
        plt.show()
    
    