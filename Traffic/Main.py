'''
Created on Jan 28, 2019

@author: austinp
'''

from Traffic import Traffic

def main():
    t = Traffic(roadLength, carDensity)
    print(t.moveIter(t.road, iterations, debug = True, showSpd = True))
    t.graphSpd()
    t.newRoad(roadLength, carDensity)
    t.graphPos(iterations)

roadLength = int(input("Road Length: "))
carDensity = float(input("Car Density: "))
iterations = int(input("Iterations: "))
main()