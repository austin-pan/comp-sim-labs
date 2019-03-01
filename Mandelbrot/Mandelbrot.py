'''
Created on Jan 24, 2019

@author: austinp
'''

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Mandelbrot(object):

    def __init__(self):                                                         # Setting up instance variables
        self.points = []                                                        # 2D array of points on the grid
        self.iterNum = []                                                       # 2D array representing the number of iterations for each point
        self.breakValue = 2                                                     # Break value compared to |z|
        self.iterationCap = 255                                                 # Maximum number of iterations per point before inferring point is convergent
        self.gridWidth = 255                                                    # Density of points horizontally
        self.gridHeight = 255                                                   # Density of points vertically
        self.xCoords = np.linspace(-2.025, 0.6, self.gridWidth)                 # Assignment of x coordinates based on density
        self.yCoords = np.linspace(-1.125, 1.125, self.gridHeight)              # Assignment of y coordinates based on density
        self.gridW = abs(self.xCoords[len(self.xCoords) - 1] - self.xCoords[0]) # Grid width
        self.gridH = abs(self.yCoords[len(self.yCoords) - 1] - self.yCoords[0]) # Grid height
        self.colorMax = 255                                                     # Maximum color value (RGB)
        self.colors = np.linspace(0, self.colorMax, self.iterationCap)          # Range of colors spaced based on iteration cap
        for y in self.yCoords:                                                  # Setting up points and iteration arrays
            newRow = []
            tempRow = []
            for x in self.xCoords:
                # newRow.append((x, y))
                newRow.append(complex(x, y))                                    # Setting up points as complex numbers based on their coordinates
                tempRow.append(1)                                               # Setting up iterations to default values of 1
            self.points.append(newRow)
            self.iterNum.append(tempRow)
    
    def __str__(self):                                                          # String form of 2D array, connected with newlines
        stringMandel = ""
        for i in range(len(self.iterNum)):
            stringMandel += str(self.iterNum[i]) + "\n"
        return stringMandel
    
    def draw(self):                                                                                                                             # Plotting of current set's iterations
        ax = plt.axes()
        
        listMax = 0
        for x in self.iterNum:                                                                                                                  # Find maximum number of iterations
            for y in x:
                if listMax < y:
                    listMax = y
                
        for r in range(len(self.yCoords)):                                                                                                      # Plotting on graph based on number of iterations
            for c in range(len(self.xCoords)):
                color = 1 - self.iterNum[r][c] / listMax                                                                                        # Normalizing iterations to percentages
                w = 1/self.gridW                                                                                                                # Point width based on grid
                h = 1/self.gridH                                                                                                                # Point height based on grid
                ax.add_patch(patches.Rectangle((self.xCoords[c], self.yCoords[r]), w, h, color = (color, color, color)))                        # Plotting points with colors based on iterations

        plt.xlim(self.xCoords[0], self.xCoords[len(self.xCoords) - 1])                                                                          # Limit x and y axes
        plt.ylim(self.yCoords[0], self.yCoords[len(self.yCoords) - 1])
        plt.show()
        
    def inMandel(self, point):                                                      # Tests whether a point is outside of the Mandelbrot Set
        # return point.abs() < self.breakValue
        return abs(point) < self.breakValue
    
    def mandelSet(self):                                                            # Iterate through every point in the grid to check if it is in the Mandelbrot Set
        for r in range(len(self.points)):
            self.iterNum.append([])
            for c in range(len(self.points[r])):
                compPoint = self.points[r][c]
                self.iterNum[r][c] = self.mandelPoint(compPoint, compPoint, 1)      # Iterate through point, where c = z because z0 = (0, 0)
    
    def mandelPoint(self, c, z, iteration):                                         # Recursively iterate through point using zn = z^2 + c
        if iteration < self.iterationCap and self.inMandel(z):
            zn = z**2 + c
            return self.mandelPoint(c, zn, iteration + 1)                           # Recursive call keeping track of iteration number and changing zn
        return iteration
    
    def juliaSet(self, static):                                                     # Iterate through every point in the grid to check if it is in the Julia Set
        for r in range(len(self.points)):
            self.iterNum.append([])
            for c in range(len(self.points[r])):
                compPoint = self.points[r][c]
                self.iterNum[r][c] = self.mandelPoint(static, compPoint, 1)         # Iterate through point, where c is kept constant
    
    
    