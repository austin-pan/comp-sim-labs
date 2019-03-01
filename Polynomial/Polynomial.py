import time

class Poly(object):
    def __init__(self, coefficients):
        self.coefs = coefficients                           # setting up instance variable list that represents coefficients
    
    def __add__(self, other):                               # adding of two polynomials
        total = []                                          # temporary list to represent the sum of the coefficients
        longPoly = self.coefs                               # polynomial with higher degree
        shortPoly = other.coefs                             # polynomial with lower degree
        if len(self.coefs) < len(other.coefs):              # correctly setting up longPoly and shortPoly
            longPoly = other.coefs;
            shortPoly = self.coefs;
            
        for i in range(0, len(shortPoly)):                  # adding coefficients of polynomials
            total.append(shortPoly[i] + longPoly[i])
        for i in range(len(shortPoly), len(longPoly)):      # appending remaining coefficients of longer polynomial
            total.append(longPoly[i])
        return Poly(total)
    
    def __str__(self):
        equation = ""                                                           # string representation of polynomial
        defaultLen = len(equation)                                              # the length of the empty string
        for i in range(0, len(self.coefs)):                                     # appending of terms to string
            if self.coefs[i] != 0:                                              # only append non-zero terms
                tail = ""                                                       # what comes after a term in string form
                if i == 0:                                                      # 0th term, constant
                    tail = ""
                elif i == 1:                                                    # 1st term, not visible exponent
                    tail = "x"
                else:                                                           # all other terms, visible exponent
                    tail = "x^" + str(i)
                
                coef = str(abs(self.coefs[i]))                                  # initialize coefficient of term, get rid of 1s
                if abs(self.coefs[i]) == 1  and  i > 0:
                    coef = ""
                
                if len(equation) == defaultLen:                                 # when no terms have been appended to string, add current one
                    if(self.coefs[i] < 0):
                        equation = equation + "-"
                    equation = equation + coef + tail
                else:                                                           # add a '+' or '-' and whitespace in between terms
                    sign = " + "
                    if self.coefs[i] < 0:
                        sign = " - "
                    equation = equation + sign + coef + tail
        return equation
    
    def order(self):                            # order of a polynomial
        return (len(self.coefs) - 1)
    
    def derivative(self):                       # derivative of a polynomial
        temp = list(self.coefs)                 # temporary list for coefficients to be copied to
            
        for i in range(len(temp)):              # multiplying each coefficient by its corresponding exponent(index)
            temp[i] = temp[i] * i
        temp.pop(0);                            # removing the constant b/c its derivative is 0
        return Poly(temp)
    
    def antiderivative(self, const):            # anti-derivative of a polynomial with a given constant
        temp = list(self.coefs)                 # temporary list for coefficients to be copied to
            
        for i in range(0, len(temp)):           # dividing each term by its successive exponent
            temp[i] = temp[i] / (i+1)
        temp.insert(0, const)                   # adding constant, increasing the exponent(index) of all other terms by one
        return Poly(temp)
    
class Rand(object):
    a = 9301
    c = 49297
    m = 233280
    
    def random(self, maxNum):                                                           # random number generator
        decShift = 10000
        obscure = (time.time() * decShift - int(time.time() * decShift)) * decShift     # current time in seconds without first 4 digits, decimal shifted
        
        seed = float(obscure * self.a + self.c) % self.m
        randInt = int(int(abs(seed / self.m) * 100) / 100 * maxNum)                     # random number
        
        return randInt
    
    