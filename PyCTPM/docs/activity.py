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

    @staticmethod
    def wilson_activity_coefficient_parameter_estimation(xi, res_Aij):
        '''
        The Wilson equation can be used when the components in the liquid phase are
        completely miscible over the whole composition range. For example, it works well
        for mixtures of highly polar compounds, i.e. alcohol and water, and mixtures of
        hydrocarbons

        alpha_ij: composition-independent parameters (is constant for all temperature range)

        args:
            xi: mole fraction
            Aij: temperature dependence of the parameters

        return:
            AcCo: activity coefficient
        '''
        # component no
        compNo = xi.shape[0]

        # temperature dependent parameters
        Aij = np.ones((compNo, compNo))
        k = 0
        for i in range(compNo):
            for j in range(compNo):
                if i != j:
                    Aij[i, j] = res_Aij[k]
                    k += 1

        # activity coefficient
        AcCoi = np.zeros(compNo)

        # activity coefficient
        xj_Aij = np.zeros((compNo, compNo))
        xk_Aki = np.zeros((compNo, compNo))
        xj_Akj = np.zeros((compNo, compNo))

        for i in range(compNo):
            for j in range(compNo):
                xj_Aij[i, j] = xi[j]*Aij[i, j]
            # _c2 = np.dot(xi, Aij[i, :])

            for k in range(compNo):
                _c0 = xi[k]*Aij[k, i]

                _c1 = 0
                for j in range(compNo):
                    _c1 = xi[j]*Aij[k, j] + _c1

                # set
                xk_Aki[i, k] = _c0/_c1

            _c3 = 1 - log(np.sum(xj_Aij[i, :])) - np.sum(xk_Aki[i, :])
            # _c3 = 1 - log(_c2) - np.sum(xk_Aki[i, :])
            AcCoi[i] = exp(_c3)

        # res
        return AcCoi

    def Wilson_activity_coefficient(self, xi, T, aij):
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
        # component no
        compNo = xi.shape[0]

        # activity coefficient
        AcCoi = np.zeros(compNo)
        #  molar volume [m^3/mol]
        MoVoi = np.zeros(compNo)

        # molar volume [m^3/mol]
        for i in range(compNo):
            _comp = self.components[i]
            _Pc = float(_comp.Pc)*1e5
            _Tc = _comp.Tc
            _w = _comp.w
            MoVoi[i] = ModifiedRackettEquation(T, _Pc, _Tc, _w)

        # parameter (dependent of temperature)
        Aij = np.ones((compNo, compNo))

        for i in range(compNo):
            for j in range(compNo):
                if j == i:
                    Aij[i, j] = 1
                else:
                    Aij[i, j] = (MoVoi[j]/MoVoi[i]) * \
                        exp(-1*aij[i, j]/(R_CONST*T))

        # activity coefficient
        xj_Aij = np.zeros((compNo, compNo))
        xk_Aki = np.zeros((compNo, compNo))

        for i in range(compNo):
            for j in range(compNo):
                xj_Aij[i, j] = xi[j]*Aij[i, j]

            for k in range(compNo):
                _c0 = xi[k]*Aij[k, i]

                _c1 = 0
                for j in range(compNo):
                    _c1 = xi[j]*Aij[k, j] + _c1

                # set
                xk_Aki[i, k] = _c0/_c1

            _c3 = 1 - log(np.sum(xj_Aij[i, :])) - np.sum(xk_Aki[i, :])
            AcCoi[i] = exp(_c3)

        # res
        return AcCoi

    @staticmethod
    def Wilson_excess_molar_Gibbs_free_energy(xi, AcCoi):
        '''
        calculate excess molar Gibbs free energy from activity coefficient of each component in a system

        args:
            xi: liquid mole fraction
            AcCoi: activity coefficient
        '''
        # # component no
        # compNo = xi.shape[0]

        # # G(E)/RT
        # c0 = np.zeros((compNo, compNo))
        # c1 = np.zeros(compNo)

        # for i in range(compNo):
        #     for j in range(compNo):
        #         if i != j:
        #             c0[i, j] = xi[i]*log(AcCoi[i])

        # # excess molar gibbs energy
        # c1 = np.sum(c0)

        # # res
        # return c1
        pass
