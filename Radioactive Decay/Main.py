'''
Created on Jan 23, 2019

@author: austinp
'''
from RDecay import RDecay

def main(dc, n, ts):
    rd = RDecay(dc, n, ts)
    initial = rd.currNucleiNum
    rd.simulate()
    for r in rd.nuclei:
        print(r)
    print("Initial Number of Undecayed Nuclei: " + str(initial))
    print("Final Number of Undecayed Nuclei: " + str(rd.currNucleiNum))
    shl = rd.simulatedHalfLife()
    print("Simulated Half Life: " + str(shl) + " min")
    ahl = rd.actualHalfLife()
    print("Actual Half Life: " + str(ahl) + " min")
    
    uncertainty = round(abs(shl - ahl) / ahl * 100, 2)
    print("Uncertainty: " + str(uncertainty) + "%")
    
dc = eval(input("Decay Constant: "))
n = int(input("N: "))
ts = float(input("Timestep: "))
print()
main(dc, n, ts)

# main(0.02775, 50, 0.01)