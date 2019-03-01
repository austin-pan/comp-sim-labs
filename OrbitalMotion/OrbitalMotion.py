'''
Created on Jan 31, 2019

@author: austinp
'''
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import math
from Vector import Vector

class OrbitalMotion(object):
    defaultRad = 0                                                                                                      # Default radius for drawing
    
    def __init__(self, filePath):
        self.filePath = filePath                                                                                        # Input text file
        self.bodies = []                                                                                                # List of celestial bodies
        self.rawInfo = []
        
        self.dataText = open(self.filePath, "r")                                                                        # Read in text file to construct system of celestial bodies
        timeInfo = eval(self.dataText.readline())                                                                       # First line specifies number of iterations and the time-step
        self.numTimeSteps = int(timeInfo[0])
        self.dt = timeInfo[1]
        
        for line in self.dataText:
            inputs = line.split(", ")
            if len(inputs) > 3:
                self.rawInfo.append((inputs[0], eval(inputs[1]), Vector(eval(inputs[2]))))
            else:
                self.rawInfo.append((inputs[0], eval(inputs[1]), Vector([eval(inputs[2]), 0])))
        
        self.bound = 0                                                                                                  # Number to keep track of graph size
        
        self.dataText = open(self.filePath, "r")
        self.dataText.readline()
        for line in self.dataText:
            inputs = line.split(", ")                                                                                   # Interpret input
            
            name = inputs[0]
            mass = eval(inputs[1])
            initPos = [0, 0]
            initVel = [0, 0]
            if len(inputs) > 3:                                                                                         # Input type of: name, mass, initial position, initial velocity
                initPos = eval(inputs[2])
                dist = Vector(initPos).magnitude()
                initVel = eval(inputs[3])
            else:                                                                                                       # Input type of: name, mass, orbital radius
                radius = eval(inputs[2])
                initPos = [radius, 0]
                dist = radius
                initVel = [0, self.initVelocity(name, self.rawInfo)]                                                    # Initial velocity calculated with sqrt( G * mass1 / radius ) based on Mars
            self.bodies.append(Celestial(name, mass, initPos, initVel))                                                 # Add celestial with input parameters
            
            if dist > self.bound:                                                                                       # Setting bound to enlarge graph size
                self.bound = dist
        self.initialBodies = self.deepCopyCelests(self.bodies)                                                          # Set up a list representing the initial states of the bodies
    
    def initVelocity(self, bodyName, rawBodies):
        currIndex = self.indexOf(bodyName, rawBodies)
        total = 0
        for x in rawBodies:
            if bodyName != x[0]:
                total += math.sqrt((Celestial.gConst * x[1]) / (rawBodies[currIndex][2] - x[2]).magnitude())
        return total
    
    def indexOf(self, bodyName, bodies):                                                                                # Find index of body of interest for orbital period
        for i in range(len(bodies)):
            curr = ""
            if isinstance(bodies[i], Celestial):
                curr = bodies[i].getName()
            else:
                curr = bodies[i][0]
                
            if curr == bodyName:
                return i
        print(bodyName + " does not exist")
        return None
    
    def printLocations(self, bodies):                                                                                   # Debug tool - print locations of each body
        for x in bodies:
            print(str(x.getName()) + " at " + str(x.getPos()))
            
    def printForces(self, bodies):                                                                                      # Debug tool - print net forces acting on each body
        for x in bodies:
            print(str(x.netForce(self.bodies)) + " on " + str(x.getName()))
    
    def printVelocities(self, bodies):                                                                                  # Debug tool - print velocities with their magnitude of each body
        for x in bodies:
            print(str(x.getName()) + " moving at " + str(x.getVelocity()) + " " + str(x.getVelocity().magnitude()))
    
    def deepCopyCelests(self, celests):                                                                                 # Creates a deep copy of the bodies so that the current list of celestials won't be altered
        temp = []
        for x in celests:
            curr = Celestial(x.getName(), x.getMass(), x.getPos().arr(), x.getVelocity().arr())
            temp.append(curr)
        return temp
    
    def totalKE(self, bodies):                                                                                          # Calculation of total kinetic energy
        total = 0
        for x in bodies:
            total += x.kineticEnergy()
        return total
    
    def init(self):                                                                                                     # Animation init function
        for i in range(len(self.initialBodies)):                                                                        # Reset all bodies to their initial states
            curr = self.initialBodies[i]
            coords = curr.getPos().arr()
            self.patches[i].center = tuple(coords)
            self.labels[i].set_position(coords)
        return self.patches
    
    def animate(self, frameNum):                                                                                        # Animation function
        if frameNum == 0:                                                                                               # Reset locations if animation is on repeat when frame number is 0
            self.bodies = self.deepCopyCelests(self.initialBodies)
            
        self.orbit(self.dt)                                                                                             # Simulate orbits of bodies for a small time step
        for i in range(len(self.bodies)):                                                                               # Update positions of bodies after orbiting
            curr = self.bodies[i]
            coords = tuple(curr.getPos().arr())
            self.patches[i].center = coords
            self.labels[i].set_position(coords)
        print("KE " + str(self.totalKE(self.bodies)))                                                                   # Print total kinetic energy
        return self.patches + self.labels
    
    def orbit(self, dt):                                                                                                # Orbit each body with a small time step
        bodyCopy = self.deepCopyCelests(self.bodies)                                                                    # Deep copies current state of bodies so that locations and velocities won't be altered mid-orbit
        for i in range(len(self.bodies)):
            curr = self.bodies[i]
            curr.orbit(bodyCopy, dt)
    
    def simulate(self, rep):                                                                                            # Simulate orbits visually. Parameter is for whether animation repeats
        fig = plt.figure()
        ax = plt.axes()
        
        OrbitalMotion.defaultRad = 0.05 * self.bound                                                                    # Set default size for visual marker of bodies
        self.patches = []
        self.labels = []
        for x in self.bodies:                                                                                           # Add visuals for each body including a circle and the name of the body
            coords = tuple(x.getPos().arr())
            self.patches.append(plt.Circle(coords, OrbitalMotion.defaultRad, color = "g", animated = True))
            self.labels.append(plt.annotate(x.getName(), xy = coords, ha = "center", va = "bottom", animated = True))
        
        for x in self.patches:                                                                                          # Add patches
            ax.add_patch(x)
        
        ax.axis("scaled")                                                                                               # Scale axes
        largeBound = self.bound * 1.5                                                                                   # Set graph size based on largest orbital radius
        ax.set_xlim(-largeBound, largeBound)
        ax.set_ylim(-largeBound, largeBound)
        
        anim = FuncAnimation(fig, self.animate, init_func = self.init, frames = self.numTimeSteps, interval = 20, repeat = rep, blit = True)    # Animation loop
        
        plt.show()
    
    def orbitalPeriod(self, bodyName, simple = True, clockwise = False):                                                                   # Simulation's orbital period for a given body
        self.bodies = self.deepCopyCelests(self.initialBodies)                                                          # Reset bodies to their initial states
        time = 0                                                                                                        # Variable to keep track of time (based on time step, dt = 1 means in seconds)
        accuracyDt = 1                                                                                              # Time step, value of 1 means seconds
        
        index = self.indexOf(bodyName, self.bodies)
        initial = self.initialBodies[index]
        prevPos = self.bodies[index].getPos()
        while True:                                                                                                     # Repeatedly orbit bodies until body of interest nears its initial position
            self.orbit(accuracyDt)
            time += accuracyDt
            curr = self.bodies[index]
            
            currDistVector = curr.getPos() - initial.getPos()                                                           # Distance between current position and initial position
            prevDistVector = prevPos - initial.getPos()
            if simple:                                                                                                  # Simple assumes that start position will be (radius, 0)
                if not clockwise:
                    if prevPos[1] < 0 and curr.getPos()[1] >= 0:                                                        # Break when current position's y position goes from negative to positive
                        break
                else:
                    if prevPos[1] > 0 and curr.getPos()[1] <= 0:                                                        # Counter-Clockwise
                        break
            else:
                if not clockwise:
                    if (currDistVector[0] <= 0 and prevDistVector[0] > 0) or (currDistVector[1] >= 0 and prevDistVector[1] < 0):
                        break
                else:
                    if (currDistVector[0] >= 0 and prevDistVector[0] < 0) or (currDistVector[1] <= 0 and prevDistVector[1] > 0):
                        break
            prevPos = curr.getPos()
        return time                                                                                                     # Initial position is less than magnitude of velocity


class Celestial(object):                                                                                                # Class that represents a celestial body
    gConst = 6.67 * 10**-11                                                                                             # Gravitation constant, 6.67E-11
    
    def __init__(self, name, mass, pos, vel):                                                                           # Initialize name, mass, position, and velocity
        self.name = name
        self.mass = mass
        self.pos = Vector(pos)
        self.vel = Vector(vel)
    
    def __str__(self):                                                                                                  # String representation
        return str(self.getName()) + " " + str(self.getMass()) + " " + str(self.getPos()) + " " + str(self.getVelocity())
    
    def __eq__(self, other):                                                                                            # Comparing two celestials
        nameEq = self.getName() == other.getName()
        massEq = self.getMass() == other.getMass()
        posEq = self.getPos() == other.getPos()
        velEq = self.getVelocity() == other.getVelocity()
        return nameEq and massEq and posEq and velEq
    
    def getName(self):                                                                                                  # Return name
        return self.name
    
    def getMass(self):                                                                                                  # Return mass
        return self.mass
    
    def getPos(self):                                                                                                   # Return position
        return self.pos
    
    def getVelocity(self):                                                                                              # Return velocity
        return self.vel
    
    def setPos(self, pos):
        self.pos = pos
    
    def setVel(self, vel):
        self.vel = vel
    
    def netForce(self, bodies):                                                                                         # Calculate net force on this body by other bodies in system
        summation = Vector([0, 0])
        for other in bodies:
            if self != other:
                prodMass = self.getMass() * other.getMass()
                diffVect = other.getPos() - self.getPos()
                curr = (prodMass / ((diffVect.magnitude())**2)) * diffVect.unitVector()
                summation = summation + curr
        return summation * Celestial.gConst
    
    def orbit(self, bodies, dt):                                                                                        # Move a bit in orbit, based on time step
        f = self.netForce(bodies)
        a = f / self.mass
        self.vel += a * dt
        self.pos += self.vel * dt
        
    def kineticEnergy(self):                                                                                            # Return this body's kinetic energy
        energy = 1/2 * self.getMass() * (self.getVelocity().magnitude()**2)
        return energy

    
    