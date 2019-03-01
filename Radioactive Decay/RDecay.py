'''
Created on Jan 22, 2019

@author: austinp
'''
import math
import random

class RDecay(object):
    def __init__(self, decayConst, n, timeStep):                            # setting up instance variables
        self.decayConst = decayConst                                        # Decay Constant
        self.initialNucleiNum = n * n                                       # Initial number of undecayed nuclei
        self.currNucleiNum = self.initialNucleiNum                          # Current number of undecayed nuclei
        self.nuclei = [[1] * n for _ in range(n)]                           # Setting up N x N 2d array representation of nuclei
        self.timeStep = timeStep                                            # Time step
        self.deltaN = decayConst * self.initialNucleiNum * timeStep         # Delta N
        self.decayProb = self.deltaN / self.initialNucleiNum                # Probability of a given nucleus to decay
        self.decayTime = 0                                                  # Total time for decaying process
    
    def actualHalfLife(self):                                               # Calculation of actual half life
        hl = math.log(2) / self.decayConst
        return hl
    
    def simulatedHalfLife(self):                                            # Simulated half life after running simulate
        return self.decayTime
    
    def simulate(self):                                                         # Simulation of decay
        while self.currNucleiNum > int(self.initialNucleiNum / 2):              # Continue simulation until half the nuclei has decayed
            self.decayTime = self.decayTime + self.timeStep                     # Increase time of decay for each cycle
            for r in range(len(self.nuclei)):                                   # Run through each row of nuclei
                if self.currNucleiNum == int(self.initialNucleiNum / 2):        # Leave loop when half of the nuclei has decayed
                    break
                
                for c in range(len(self.nuclei[r])):                            # Run through each nucleus in a row
                    currProb = random.random()                                  # Generate random probability
                    if self.nuclei[r][c] == 1 and currProb < self.decayProb:    # If random probability is less than probability of decay, decay current nucleus
                        self.nuclei[r][c] = 0                                   # Set visual representation of decay
                        self.currNucleiNum = self.currNucleiNum - 1             # Decrease current number of undecayed nuclei
                    if self.currNucleiNum == int(self.initialNucleiNum / 2):    # Leave loop when half of the nuclei has decayed
                        break
                
                
                