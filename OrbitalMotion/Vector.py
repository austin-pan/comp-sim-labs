'''
Created on Feb 22, 2019

@author: austinp
'''

import numpy as np
import math

class Vector(object):                                                                                                   # Class to represent vectors
    def __init__(self, arr):                                                                                            # Takes in a n-dimensional numpy array
        self.vector = np.array(arr)
    
    def arr(self):                                                                                                      # Returns numpy array version of self
        return self.vector
    
    def __str__(self):                                                                                                  # String representation of vector
        return "vector: " + str(self.vector)
    
    def __eq__(self, other):                                                                                            # Comparing same length vectors
        if len(self.arr()) == len(other.arr()):
            for i in range(len(self.arr())):
                if self.arr()[i] != other.arr()[i]:
                    return False
        else:
            return False
        return True
    
    def __getitem__(self, k):                                                                                           # Allow vector to be iterable
        return self.arr()[k]
    
    def __setitem__(self, k, v):                                                                                        # Directly edit vector components
        self[k] = v
    
    def __add__(self, other):                                                                                           # Vector addition
        return Vector(self.arr() + other.arr())
    
    def __sub__(self, other):                                                                                           # Vector subtraction
        return Vector(self.arr() - other.arr())
    
    def __mul__(self, num):                                                                                             # Vector multiplication by a number
        return Vector(self.arr() * num)
    
    __rmul__ = __mul__                                                                                                  # Make vector multiplication commutative
    
    def __truediv__(self, num):                                                                                         # Vector division by a number
        return Vector(self.arr() / num)
    
    def cross(self, other):                                                                                             # Vector cross product
        return np.cross(self.arr(), other.arr())
    
    def dot(self, other):                                                                                               # Vector dot product
        return np.dot(self.arr(), other.arr())
    
    def magnitude(self):                                                                                                # Vector magnitude
        sumSq = 0
        for x in self.arr():
            sumSq += x**2
        mag = math.sqrt(sumSq)
        return mag
    
    def unitVector(self):                                                                                               # Unit vector
        return self / self.magnitude()