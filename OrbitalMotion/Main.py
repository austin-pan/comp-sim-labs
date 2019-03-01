'''
Created on Feb 18, 2019

@author: austinp
'''
from OrbitalMotion import OrbitalMotion

def main():
    om = OrbitalMotion("input.txt")
    om.printVelocities(om.bodies)
    om.simulate(False)
    print()
    ob = "Phobos"
    print("Orbital Period of " + ob + ": " + str(om.orbitalPeriod(ob, simple = True)) + " seconds")                              # Print Phobos' orbital period

main()