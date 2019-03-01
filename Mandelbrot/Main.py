'''
Created on Jan 27, 2019

@author: austinp
'''

from Mandelbrot import Mandelbrot

def main():
    
    m = Mandelbrot()
    m.mandelSet()
    m.draw()
    
    m.juliaSet(complex(-1, 0))
    m.draw()
    m.juliaSet(complex(0, -1)) # The Dendrite
    m.draw()
    m.juliaSet(complex(0.5, 0))
    m.draw()
    m.juliaSet(complex(-0.1, 0.8)) # The Rabbit
    m.draw()
    m.juliaSet(complex(0.36, 0.1)) # The Dragon
    m.draw()

main()