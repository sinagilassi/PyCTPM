# MARGULES MODELS
# ----------------

# packages/modules
from math import pow, sqrt, exp
import numpy as np


class Margules:
    def __init__(self, components):
        self.components = components
        # set
        self.compNo = len(components)

    def Margules1Parameter_activity_coefficient(self, xi, Aij):
        '''
        the Gibbs excess function is defined as a one-parameter Margules equation (binary system)

        args:
            xi: mole fraction
            Aij: Margules constant (which is taken from experimental results)
        '''
        # check
        if self.compNo > 2:
            return [0, 0]

        # activity coefficient
        AcCo = []
        for i in range(self.compNo):
            AcCo.append(exp(Aij*pow(1-xi[i], 2)))

        # res
        return AcCo

    def Margules1ParameterFunction(self, x):
        '''
        Margules 1-parameter function
        '''
        # set
        Aij = np.zeros(self.compNo)
        for i in range(self.compNo):
            Aij[i] = x[i]
