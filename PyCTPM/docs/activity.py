# ACTIVITY
# ---------

# packages/modules
from math import pow, exp, log
import numpy as np
from PyCTPM.core.constants import R_CONST

from PyCTPM.docs.dThermo import ModifiedRackettEquation


class ActivityClass:
    def __init__(self, components):
        self.components = components
        # set
        self.compNo = len(components)

    def wilson_activity_coefficient_parameter_estimation(self, xi, T, Aij):
        '''
        The Wilson equation can be used when the components in the liquid phase are
        completely miscible over the whole composition range. For example, it works well
        for mixtures of highly polar compounds, i.e. alcohol and water, and mixtures of
        hydrocarbons

        args:
            xi: mole fraction
            T: temperature
            aij: alpha[i,j] as composition-independent parameters which describe how the interactions
                between the unlike components differ from the like components

        return:
            AcCo: activity coefficient
        '''
        # activity coefficient
        AcCoi = np.zeros(self.No)
        #  molar volume [m^3/mol]
        MoVoi = np.zeros(self.compNo)

        # molar volume [m^3/mol]
        for i in range(self.compNo):
            _comp = self.components[i]
            _Pc = _comp.Pc
            _Tc = _comp.Tc
            _w = _comp.w
            MoVoi[i] = ModifiedRackettEquation(T, _Pc, _Tc, _w)

        # activity coefficient
        xj_Aij = np.zeros((self.compNo, self.compNo))
        xk_Aki = np.zeros((self.compNo, self.compNo))
        xj_Akj = np.zeros((self.compNo, self.compNo))

        for i in range(self.compNo):
            for j in range(self.compNo):
                xj_Aij[i, j] = xi[j]*Aij[i, j]

            for k in range(self.compNo):
                _c0 = xi[k]*Aij[k, i]
                for j in range(self.compNo):
                    xj_Akj[k, j] = xi[j]*Aij[k, j]
                xk_Aki[i, k] = _c0/np.sum(xj_Akj[k, :])

            _c0 = 1 - log(np.sum(xj_Aij[i, :])) - np.sum(xk_Aki[i, :])
            AcCoi[i] = exp(_c0)

        # res
        return AcCoi

    def wilson_activity_coefficient(self, xi, T, aij):
        '''
        The Wilson equation can be used when the components in the liquid phase are
        completely miscible over the whole composition range. For example, it works well
        for mixtures of highly polar compounds, i.e. alcohol and water, and mixtures of
        hydrocarbons

        args:
            xi: mole fraction
            T: temperature
            aij: alpha[i,j] as composition-independent parameters which describe how the interactions
                between the unlike components differ from the like components

        return:
            AcCo: activity coefficient
        '''
        # activity coefficient
        AcCoi = np.zeros(self.No)
        #  molar volume [m^3/mol]
        MoVoi = np.zeros(self.compNo)

        # molar volume [m^3/mol]
        for i in range(self.compNo):
            _comp = self.components[i]
            _Pc = _comp.Pc
            _Tc = _comp.Tc
            _w = _comp.w
            MoVoi[i] = ModifiedRackettEquation(T, _Pc, _Tc, _w)

        # parameter (dependent of temperature)
        Aij = np.ones((self.compNo, self.compNo))

        for i in range(self.compNo):
            for j in range(self.compNo):
                if j == i:
                    Aij[i, j] = 1
                else:
                    Aij[i, j] = (MoVoi[j]/MoVoi[i]) * \
                        exp(-1*aij[i, j]/(R_CONST*T))

        # activity coefficient
        xj_Aij = np.zeros((self.compNo, self.compNo))
        xk_Aki = np.zeros((self.compNo, self.compNo))
        xj_Akj = np.zeros((self.compNo, self.compNo))

        for i in range(self.compNo):
            for j in range(self.compNo):
                xj_Aij[i, j] = xi[j]*Aij[i, j]

            for k in range(self.compNo):
                _c0 = xi[k]*Aij[k, i]
                for j in range(self.compNo):
                    xj_Akj[k, j] = xi[j]*Aij[k, j]
                xk_Aki[i, k] = _c0/np.sum(xj_Akj[k, :])

            _c0 = 1 - log(np.sum(xj_Aij[i, :])) - np.sum(xk_Aki[i, :])
            AcCoi[i] = exp(_c0)
