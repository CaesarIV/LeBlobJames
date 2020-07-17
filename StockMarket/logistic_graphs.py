#V.20.07.05.01
import numpy as np


class decision():

    def __init__(self, attributes):
        self.p_threshhold = attributes[0]

        maximum = 10
        minimum = -10 
        self.B0 = attributes[1] * (maximum-minimum)+ minimum
        self.B1 = attributes[2] * (maximum-minimum)+ minimum
        self.B2 = attributes[3] * (maximum-minimum)+ minimum
        self.B3 = attributes[4] * (maximum-minimum)+ minimum
        self.B4 = attributes[5] * (maximum-minimum)+ minimum
        self.B5 = attributes[6] * (maximum-minimum)+ minimum
        self.B6 = attributes[7] * (maximum-minimum)+ minimum
        pass


    def check(self, x):
        k  =   self.B0 \
             + self.B1 * x[0] \
             + self.B2 * x[1] \
             + self.B3 * x[2] \
             + self.B4 * x[0] * x[1] \
             + self.B5 * x[0] * x[2] \
             + self.B6 * x[1] * x[2]
        
        p = 1 / ( 1 + (np.exp(-k)) )
        
        if p >= self.p_threshhold:
            return(1)
        else:
            return(0)


class chemical():

    def __init__(self, attributes):
        maximum = 10
        minimum = -10
        self.B0 = attributes[0] * maximum-minimum + minimum
        self.B1 = attributes[1] * maximum-minimum + minimum
        self.B2 = attributes[2] * maximum-minimum + minimum
        pass

    def production(self, x):
        k = self.B0 \
            + self.B1 * x \
            + self.B2 * (x**2)
        
        p = 1 / ( 1 + (np.exp(-k)) )

        return(p)
