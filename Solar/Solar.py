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
        
        self.bound = 0                                                                                                  # Number to keep track of graph size
        
        for line in self.dataText:
            inputs = line.split(", ")
            
            name = inputs[0]
            mass = eval(inputs[1])
            initPos = [0, 0]
            initVel = [0, 0]
            parentName = inputs[len(inputs) - 1].strip()
            if len(inputs) > 4:
                initPos = eval(inputs[2])
                dist = Vector(initPos).magnitude()
            else:
                radius = eval(inputs[2])
                initPos = [radius, 0]
                dist = radius
            self.rawInfo.append(Celestial (name, mass, initPos, initVel, parentName))
            
            if dist > self.bound:                                                                                       # Setting bound to enlarge graph size
                self.bound = dist
        for x in self.rawInfo:
            if x.getParent() != "None":
                parent = self.rawInfo[self.indexOf(x.getParent(), self.rawInfo)]
                x.setPos(x.getPos() + parent.getPos())
        for x in self.rawInfo:
            copy = x.clone()
            copy.setVel(self.initVelocityVertical(copy.getName(), self.rawInfo))
            self.bodies.append(copy)
        
        
        '''self.dataText = open(self.filePath, "r")
        self.dataText.readline()
        for line in self.dataText:
            inputs = line.split(", ")                                                                                   # Interpret input
            
            name = inputs[0]
            mass = eval(inputs[1])
            initPos = Vector([0, 0])
            initVel = Vector([0, 0])
            parentName = ""
            if len(inputs) > 4:                                                                                         # Input type of: name, mass, initial position, initial velocity
                initPos = Vector(eval(inputs[2]))
                dist = initPos.magnitude()
                initVel = Vector(eval(inputs[3]))
                parentName = inputs[4].strip()
            else:                                                                                                       # Input type of: name, mass, orbital radius
                radius = eval(inputs[2])
                initPos = Vector([radius, 0])
                dist = radius
                initVel = self.initVelocityVertical(name, self.rawInfo)                                                 # Initial velocity calculated with sqrt( G * mass1 / radius ) based on Mars
                parentName = inputs[3].strip()
                
            if parentName != "None":
                    parent = self.bodies[self.indexOf(parentName, self.bodies)]
                    initPos += parent.getPos()
            self.bodies.append(Celestial(name, mass, initPos.arr(), initVel.arr(), parentName))                         # Add celestial with input parameters
            
            if dist > self.bound:                                                                                       # Setting bound to enlarge graph size
                self.bound = dist'''
        
        self.initialBodies = self.deepCopyCelests(self.bodies)                                                          # Set up a list representing the initial states of the bodies
    
    def initVelocityVertical(self, bodyName, bodies):
        currIndex = self.indexOf(bodyName, bodies)
        curr = bodies[currIndex]
        total = 0
        for x in bodies:
            if bodyName != x.getName():
                distVector = curr.getPos() - x.getPos()
                velocity = math.sqrt((Celestial.gConst * x.getMass()) / distVector.magnitude())
                sign = distVector[0] / abs(distVector[0])
                total += sign * velocity
        return Vector([0, total])
    
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
        return -1
    
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
            temp.append(x.clone())
        return temp
    
    def totalKE(self, bodies):                                                                                          # Calculation of total kinetic energy
        total = 0
        for x in bodies:
            total += x.kineticEnergy()
        return total
    
    def totalGPE(self, bodies):
        total = 0
        for x in bodies:
            for y in bodies:
                if x != y:
                    total += x.gravPotentialEnergy(y)
        total /= 2.0
        return total
    
    def totalEnergy(self, bodies):
        return self.totalKE(bodies) + self.totalGPE(bodies)
    
    def init(self):                                                                                                     # Animation init function
        for i in range(len(self.initialBodies)):                                                                        # Reset all bodies to their initial states
            curr = self.initialBodies[i]
            coords = curr.getPos().arr()
            self.patches[i].center = tuple(coords)
            self.labels[i].set_position(coords)
        return self.patches
    
    def animate(self, frameNum):                                                                                        # Animation function
        self.orbit(self.dt)                                                                                             # Simulate orbits of bodies for a small time step
        for i in range(len(self.bodies)):                                                                               # Update positions of bodies after orbiting
            curr = self.bodies[i]
            coords = tuple(curr.getPos().arr())
            self.patches[i].center = coords
            self.labels[i].set_position(coords)
            magnify = 10**-8
            self.netForces[i].set_data([coords[0], coords[0]+curr.netForce(self.bodies)[0] * magnify], [coords[1], coords[1]+curr.netForce(self.bodies)[1] * magnify])
            magnify = 10**7
            self.directions[i].set_data([coords[0], coords[0]+curr.getVelocity()[0] * magnify], [coords[1], coords[1]+curr.getVelocity()[1] * magnify])
        if not self.silent:
            print("Total Energy: " + str(self.totalEnergy(self.bodies)))                                                # Print total energy
        return self.patches + self.labels + self.netForces + self.directions
    
    def orbit(self, dt):                                                                                                # Orbit each body with a small time step
        bodyCopy = self.deepCopyCelests(self.bodies)                                                                    # Deep copies current state of bodies so that locations and velocities won't be altered mid-orbit
        nextBodyCopy = []
        for x in bodyCopy:
            nextBodyCopy.append(Celestial(x.getName(), x.getMass(), x.getNextPos(dt).arr(), [0, 0]))
        for i in range(len(self.bodies)):
            curr = self.bodies[i]
            curr.orbit(bodyCopy, nextBodyCopy, dt)
    
    def simulate(self, rep = False, silent = False):                                                                                            # Simulate orbits visually. Parameter is for whether animation repeats
        self.silent = silent
        fig = plt.figure()
        ax = plt.axes()
        
        OrbitalMotion.defaultRad = 0.05 * self.bound                                                                    # Set default size for visual marker of bodies
        self.patches = []
        self.netForces = []
        self.directions = []
        self.labels = []
        for x in self.bodies:                                                                                           # Add visuals for each body including a circle and the name of the body
            coords = tuple(x.getPos().arr())
            self.patches.append(plt.Circle(coords, OrbitalMotion.defaultRad, color = "g", animated = False))
            self.netForces.append(plt.Line2D([coords[0], coords[0] + x.netForce(self.bodies)[0]], [coords[1], coords[1] + x.netForce(self.bodies)[1]], color = "r", animated = False))
            self.directions.append(plt.Line2D([coords[0], coords[0] + x.getVelocity().arr()[0]], [coords[1], coords[1] + x.getVelocity().arr()[1]], color = "b", animated = False))
            self.labels.append(plt.annotate(x.getName(), xy = coords, ha = "center", va = "bottom", animated = False))
        
        for x in self.patches:                                                                                          # Add patches
            ax.add_patch(x)
        for x in self.directions:
            ax.add_line(x)
        for x in self.netForces:
            ax.add_line(x)
        
        self.printVelocities(self.bodies)
        
        ax.axis("scaled")                                                                                               # Scale axes
        largeBound = self.bound * 1.5                                                                                   # Set graph size based on largest orbital radius
        ax.set_xlim(-largeBound, largeBound)
        ax.set_ylim(-largeBound, largeBound)
        
        anim = FuncAnimation(fig, self.animate, init_func = self.init, frames = self.numTimeSteps, interval = 5, repeat = rep, blit = False)    # Animation loop
        
        plt.show()
        self.printLocations(self.bodies)
        self.printVelocities(self.bodies)
    
    def orbitalPeriod(self, bodyName, accuracyDt = 1000, simple = True, clockwise = False, returnType = "years"):       # Simulation's orbital period for a given body
        self.bodies = self.deepCopyCelests(self.initialBodies)                                                          # Reset bodies to their initial states
        time = 0                                                                                                        # Variable to keep track of time (based on time step, dt = 1 means in seconds)
        
        index = self.indexOf(bodyName, self.bodies)
        curr = self.bodies[index]
        
        initial = self.initialBodies[index]
        parentName = curr.getParent()
        initialParentIndex = self.indexOf(parentName, self.initialBodies)
        initialParent = self.initialBodies[initialParentIndex]
        parentIndex = self.indexOf(parentName, self.bodies)
        currParent = self.bodies[parentIndex]
        
        prevPos = curr.getPos()
        prevParentPos = currParent.getPos()
        while True:                                                                                                     # Repeatedly orbit bodies until body of interest nears its initial position
            self.orbit(accuracyDt)
            time += accuracyDt
            
            currDistToInitialVector = (curr.getPos() - currParent.getPos()) - (initial.getPos() - initialParent.getPos())                # Distance between current position and initial position
            prevDistToInitialVector = (prevPos - prevParentPos) - (initial.getPos() - initialParent.getPos())
            if simple:                                                                                                  # Simple assumes that start position will be (radius, 0)
                if not clockwise:
                    if (curr.getPos() - currParent.getPos())[1] >= 0 and (prevPos - prevParentPos)[1] < 0:
                        break
                else:
                    if (curr.getPos() - currParent.getPos())[1] <= 0 and (prevPos - prevParentPos)[1] > 0:                                                        # Counter-Clockwise
                        break
            else:
                if not clockwise:
                    if (currDistToInitialVector[0] <= 0 and prevDistToInitialVector[0] > 0) or (currDistToInitialVector[1] >= 0 and prevDistToInitialVector[1] < 0):
                        break
                else:
                    if (currDistToInitialVector[0] >= 0 and prevDistToInitialVector[0] < 0) or (currDistToInitialVector[1] <= 0 and prevDistToInitialVector[1] > 0):
                        break
            prevPos = curr.getPos()
            prevParentPos = currParent.getPos()
            
        if returnType == "seconds":
            time = time
        elif returnType == "minutes":
            time = time / 60
        elif returnType == "hours":
            time = time / 60 / 60
        elif returnType == "days":
            time = time / 60 / 60 / 24
        elif returnType == "years":
            time = time / 60 / 60 / 24 / 365.25
        return time                                                                                                     # Initial position is less than magnitude of velocity


class Celestial(object):                                                                                                # Class that represents a celestial body
    gConst = 6.67428 * 10**-11                                                                                             # Gravitation constant, 6.67E-11
    
    def __init__(self, name, mass, pos, vel, parent = "None"):                                                          # Initialize name, mass, position, and velocity
        self.name = name
        self.mass = mass
        self.pos = Vector(pos)
        self.vel = Vector(vel)
        self.prevAccel = Vector([0, 0])
        self.currAccel = Vector([0, 0])
        self.parent = parent
    
    def __str__(self):                                                                                                  # String representation
        return str(self.getName()) + " " + str(self.getMass()) + " " + str(self.getPos()) + " " + str(self.getVelocity()) + " " + self.parent
    
    def __eq__(self, other):                                                                                            # Comparing two celestials
        nameEq = self.getName() == other.getName()
        massEq = self.getMass() == other.getMass()
        posEq = self.getPos() == other.getPos()
        velEq = self.getVelocity() == other.getVelocity()
        return nameEq and massEq and posEq and velEq
    
    def clone(self):
        return Celestial(self.getName(), self.getMass(), self.getPos().arr(), self.getVelocity().arr(), self.parent)
    
    def getName(self):                                                                                                  # Return name
        return self.name
    
    def getMass(self):                                                                                                  # Return mass
        return self.mass
    
    def getParent(self):
        return self.parent
    
    def getPos(self):                                                                                                   # Return position
        return self.pos
    
    def getNextPos(self, dt):
        nextPos = self.getPos() + self.getVelocity()*dt + 1/6*(4*self.getCurrAccel() - self.getPrevAccel())*(dt**2)
        return nextPos
    
    def getVelocity(self):                                                                                              # Return velocity
        return self.vel
    
    def getPrevAccel(self):
        return self.prevAccel
    
    def getCurrAccel(self):
        return self.currAccel
    
    def setPos(self, pos):
        self.pos = pos
    
    def setVel(self, vel):
        self.vel = vel
    
    def netForce(self, bodies):                                                                                         # Calculate net force on this body by other bodies in system
        summation = Vector([0, 0])
        for other in bodies:
            if self.getName() != other.getName():
                prodMass = self.getMass() * other.getMass()
                diffVect = other.getPos() - self.getPos()
                curr = (prodMass / ((diffVect.magnitude())**2)) * diffVect.unitVector()
                summation = summation + curr
        return summation * Celestial.gConst
    
    def orbit(self, bodies, nextBodies, dt):                                                                            # Move a bit in orbit, based on time step
        currNetForce = self.netForce(bodies)
        self.currAccel = currNetForce / self.getMass()
        nextNetForce = self.netForce(nextBodies)
        nextPos = self.getNextPos(dt)
        nextAccel = (1/self.getMass()) * nextNetForce
        nextVel = self.getVelocity() + 1/6*(2*nextAccel + 5*self.getCurrAccel() - self.getPrevAccel())*dt
        
        self.pos = nextPos
        self.vel = nextVel
        self.prevAccel = Vector(self.getCurrAccel().arr())
        
    def kineticEnergy(self):                                                                                            # Return this body's kinetic energy
        energy = 1/2 * self.getMass() * (self.getVelocity().magnitude()**2)
        return energy
    
    def gravPotentialEnergy(self, other):                                                                               # Return the gravitational potential energy between this body and another body
        dist = (self.getPos() - other.getPos()).magnitude()
        energy = -1 * Celestial.gConst * self.getMass() * other.getMass() / dist
        return energy
    
    