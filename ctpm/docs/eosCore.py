# equation of states
# -------------------

# import packages/modules
import numpy as np
import math
import core.constants as CONST
from docs.eos import eosClass
from docs.eosData import dbClass

# eos methods


class eosCoreClass(eosClass):
    # number of components
    componentsNo = 0
    # init

    def __init__(self, P, T, components, eosName, moleFraction) -> None:
        self.P = P
        self.T = T
        self.components = components
        self.eosName = eosName
        self.moleFraction = moleFraction
        # parent
        super().__init__(P, T, eosName, moleFraction)

    def classDes():
        print("functions used by all equation of states")

    def _eosPR(self) -> float:
        # class init
        # ->  database
        eosData = dbClass()

        componentsNo = len(self.components)
        print(f"componentsNo: {componentsNo}")

        # component data
        componentsData = eosData.loadItemData(self.components)
        # print(f"component data {componentsData}")
        # sorted data
        componentsDataSorted = [
            [item['Pc'], item['Tc'], item['w']] for item in componentsData]
        print("componentsDataSorted {}".format(componentsDataSorted))

        # cal parameters
        # a b matrix
        a = np.zeros(componentsNo)
        b = np.zeros(componentsNo)

        count = 0
        for item in componentsDataSorted:

            print(f"item: {item}")
            aLoop = self.pengRobinson_a(item[0], item[1], item[2])
            # a.append(aLoop)
            a[count] = aLoop
            bLoop = self.pengRobinson_b(item[0], item[1])
            # b.append(bLoop)
            b[count] = bLoop
            count += 1

        # log
        print(f"a: {a} | b: {b}")

        # check pure, multi-component system
        if componentsNo > 1:
            # mixing rule to calculate a/b
            # kij
            kij = self.kijFill()
            aij = self.aijFill(a, kij)
            aSet = self.aMixing(aij, self.moleFraction)
            bSet = self.bMixing(b, self.moleFraction)
        else:
            # no change a/b
            aSet = a[0]
            bSet = b[0]

        # log
        print(f"aSet: {aSet} | bSet: {bSet}")

        # parameters A,B
        A = self.eos_A(aSet)
        B = self.eos_B(bSet)
        print(f"A: {A} | B: {B}")

        # build polynomial eos equation f(Z)
        alpha = self.eos_alpha(B)
        beta = self.eos_beta(A, B)
        gamma = self.eos_gamma(A, B)
        print(f"alpha: {alpha} | beta: {beta} | gamma: {gamma}")

        # find f(Z) root
        rootList = self.findRootfZ(alpha, beta, gamma)
        print(f"rootList: {rootList}")

        # z
        minZ = np.amin(rootList)
        maxZ = np.amax(rootList)

        # molar volume [cm3/gmol]
        # -> liquid
        molarVolumeLiquid = self.molarVolume(minZ)
        print(f"molarVolumeLiquid {molarVolumeLiquid}")
        # -> gas
        molarVolumeGas = self.molarVolume(maxZ)
        print(f"molarVolumeGas {molarVolumeGas}")

        # molar volume fraction
        molarVolume = {
            "gas": self.sortRootfZ(molarVolumeGas*np.array(self.moleFraction)),
            "liquid": self.sortRootfZ(molarVolumeLiquid*np.array(self.moleFraction))
        }

        return molarVolume

    # a
    def pengRobinson_a(self, Pc, Tc, w) -> float:
        k = 0.37464 + 1.54226 * w - 0.26993 * math.pow(w, 2)
        alpha = math.pow(1 + k * (1 - math.sqrt(self.T / Tc)), 2)
        ac = (0.45723553 * (math.pow(CONST.R_CONST, 2) * math.pow(Tc, 2))) / Pc
        res = ac*alpha
        return res

    # b
    def pengRobinson_b(self, Pc, Tc) -> float:
        res = (0.07779607 * CONST.R_CONST * Tc) / Pc
        return res


# main
if __name__ == "__main__":
    eosCoreClass().classDes()
