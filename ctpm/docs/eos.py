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

    # component no
    def componentNoSet(self):
        return len(self.moleFraction)

    #
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

    # !
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
        #
        zList = []
        zGuess = np.linspace(0, 1, 11)
        for item in zGuess:
            zLoop = fsolve(self.fZ, [item], args=data)
            zList.append(zLoop[0])

        # list -> array
        zListArray = np.array(zList)
        # limit between 0,1
        zListLimit = zListArray[np.where(
            (zListArray >= 0.0) & (zListArray <= 1.0))]
        # print(f"zListLimit: {zListLimit}")
        # round z
        zListRound = self.sortRootfZ(zListLimit)
        # print(f"zListRound: {zListRound}")
        #  remove duplicate items
        zListNet = np.array(removeDuplicatesList(zListRound))
        # print(f"zListNet: {zListNet}")
        # return
        return zListNet

    # net fZ root
    def sortRootfZ(self, data):
        zList = roundNum(data, 4)
        return zList

    # k[i,j]
    def kijFill(self):
        """ interaction parameter should be taken from experimental data, otherwise have to set to zero! """
        # components number
        componentsNo = self.componentNoSet()
        print(f"componentsNo {componentsNo}")
        # square matrix
        matrixShape = (componentsNo, componentsNo)
        kijMatrix = np.zeros(matrixShape)
        # set
        for i in range(componentsNo):
            for j in range(componentsNo):
                if i == j:
                    kijMatrix[i, j] = 0.0
                else:
                    kijMatrix[i, j] = 0.0
        # res
        return kijMatrix

    # a[i,j]
    def aijFill(self, ai, kij):
        # components number
        componentsNo = self.componentNoSet()
        # square matrix
        matrixShape = (componentsNo, componentsNo)
        aijMatrix = np.zeros(matrixShape)
        # set
        for i in range(componentsNo):
            for j in range(componentsNo):
                aijMatrix[i, j] = (1-kij[i, j])*np.sqrt(ai[i]*ai[j])
        # res
        return aijMatrix

    # mixing rule b
    def bMixing(self, bi, xi):
        # components number
        componentsNo = self.componentNoSet()
        # square matrix
        matrixShape = (componentsNo)
        bMatrix = np.zeros(matrixShape)
        # set
        for i in range(componentsNo):
            bMatrix[i] = xi[i]*bi[i]
        # sum
        res = np.sum(bMatrix)
        return res

    # mixing rule a
    def aMixing(self, aij, xi):
        # components number
        componentsNo = self.componentNoSet()
        # square matrix
        matrixShape = (componentsNo, componentsNo)
        aMatrix = np.zeros(matrixShape)
        # set
        for i in range(componentsNo):
            for j in range(componentsNo):
                aMatrix[i, j] = xi[i]*xi[j]*aij[i, j]
        # sum
        res = np.sum(aMatrix)
        return res

    # molar volume [cm3/gmol]
    def molarVolume(self, Z):
        return Z * ((CONST.R_CONST * self.T) / self.P)
