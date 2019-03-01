from Polynomial import Poly
from Polynomial import Rand

def main():
    pa = Poly([2, 0, 4, -1, 0, 6])
    pb = Poly([-1, 3, 0, 4.5])
    
    print("Pa(x) = " + str(pa))
    print("Pb(x) = " + str(pb))
    
    print()
    print("Order of Pa: " + str(pa.order()))
    
    total = pa + pb
    print("Pa(x) + Pb(x)                        = " + str(total))
    
    deriv = pa.derivative()
    print("derivative of Pa(x)                  = " + str(deriv))
    
    antideriv = deriv.antiderivative(2)
    print("anti-derivative of dPa(x)/dx, C = 2  = " + str(antideriv))

def random():
    print()
    print("Random Numbers: ", end = " ")
    r = Rand()
    for _ in range(0, 10):
        print(r.random(10), end = " ")

main()
random()