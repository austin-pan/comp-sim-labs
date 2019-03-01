'''
Created on Feb 21, 2019

@author: austinp
'''
from Solar import OrbitalMotion

def main():
    om = OrbitalMotion("input.txt")
    om.simulate(rep = True, silent = True)
    print()
    if True:
        rt = "seconds"
        celests = ["Moon"]
        for x in celests:
            print("Orbital Period of " + x + ": " + str(om.orbitalPeriod(x, accuracyDt = 100, simple = True, returnType = rt)) + " " + rt)
main()