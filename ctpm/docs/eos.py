# eos class
# parameters for three equation of states
# van der Waals
# Redlich-Kwong and Soave
# Peng-Robinson

# import packages/modules
import numpy as np
from scipy.optimize import fsolve
import core.constants as CONST
from core.utilities import roundNum, removeDuplicatesList


class eosClass:
    # init
    def __init__(self, P, T, eosName, moleFraction) -> None:
        self.P = P
        self.T = T
        self.eosName = eosName
        self.moleFraction = moleFraction

    def eos_A(self, a):
        # A value
        # var
        res = 0
        # eos name
        eosNameSet = self.eosName
        # select method
        selectEOS = {
            "PR": lambda: (a * self.P) / np.power(CONST.R_CONST * self.T, 2),
            "RK": lambda: (a * self.P) / (np.power(CONST.R_CONST, 2) * np.power(self.T, 2.5)),
            "VDW": 1
        }
        # exe
        res = selectEOS.get(eosNameSet)()
        # return
        return res

    def eos_B(self, b):
        """ calculate B """
        return (b * self.P) / (CONST.R_CONST * self.T)

    def eos_Z(self, V):
        """ calculate specific volume """
        return (self.P * V) / (CONST.R_CONST * self.T)

    def eos_alpha(self, B):
        """ calculate alpha in f(Z) """
        # var
        res = 0
        # eos name
        eosNameSet = self.eosName

        # select eos
        selectEOS = {
            "VDW": lambda B: -1 - B,
            "SKR": lambda B: -1,
            "PR": lambda B: -1 + B,
        }
        # res
        res = selectEOS.get(eosNameSet)(B)
        # return
        return res

    def eos_beta(self, A, B):
        """ calculate parameter beta """
        # var
        res = 0
        # eos name
        eosNameSet = self.eosName

        # select eos
        selectEOS = {
            "VDW": lambda A, B: A,
            "SKR": lambda A, B: A - B - np.power(B, 2),
            "PR": lambda A, B: A - 3 * np.power(B, 2) - 2 * B,
        }
        # res
        res = selectEOS.get(eosNameSet)(A, B)
        # return
        return res

    def eos_gamma(self, A, B):
        """ calculate parameter gamma """
        # var
        res = 0
        # eos name
        eosNameSet = self.eosName

        # select eos
        selectEOS = {
            "VDW": lambda A, B: -A * B,
            "SKR": lambda A, B: -A * B,
            "PR": lambda A, B: -A * B + np.power(B, 2) + np.power(B, 3),
        }
        # res
        res = selectEOS.get(eosNameSet)(A, B)
        # return
        return res

    # f(Z)
    def fZ(self, x, *data):
        """ f(Z) gets parameters: alpha, beta, gamma """
        # print(data)
        alpha, beta, gamma = data
        fZSet = np.power(x, 3) + alpha*np.power(x, 2) + beta*x + gamma
        return fZSet

    # find fZ root
    def findRootfZ(self, alpha, beta, gamma):
        # vars
        data = (alpha, beta, gamma)
        # components number
        componentsNo = len(self.components)
        x0 = np.zeros(componentsNo)
        #
        zList = []
        zGuess = np.linspace(0, 1, 11)
        for item in zGuess:
            zLoop = fsolve(self.fZ, [item], args=data)
            zList.append(zLoop[0])

        # round z
        zListRound = self.sortRootfZ(zList)
        # print(f"zListRound: {zListRound}")
        #  remove duplicate items
        zListNet = removeDuplicatesList(zListRound)
        # print(f"zListNet: {zListNet}")
        # return
        return zListNet

    # net fZ root
    def sortRootfZ(self, data):
        zList = roundNum(data, 4)
        return zList
