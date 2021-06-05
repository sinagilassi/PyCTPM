# equation of states
# --------------------------------------

# import packages/modules
import core.constants as CONST
from docs.eos import eosClass
from docs.eosData import dbClass
import math


# eos methods
class eosCoreClass(eosClass):
    # * init
    def __init__(self, P, T, components, eosName) -> None:
        # log
        # print(P, T, components)
        self.P = P
        self.T = T
        self.components = components
        self.eosName = eosName
        # parent
        super().__init__(eosName)

    #! PR eos
    def _eosPR(self) -> float:
        # * eos class
        eos = eosClass(CONST.PENG_ROBINSON)
        # * eos database
        eosData = dbClass()

        # * component data
        componentsData = eosData.loadItemData(self.components)
        print(f"component data {componentsData}")
        # sorted data
        componentsDataSorted = [
            [item['Tc'], item['Pc'], item['w']] for item in componentsData]
        print("componentsDataSorted {}".format(componentsDataSorted))

        # cal parameters
        # a, b
        a = []
        b = []
        for item in componentsDataSorted:
            print(f"item: {item}")
            aLoop = self.pengRobinson_a(item[0], item[1], item[2])
            a.append(aLoop)
            bLoop = self.pengRobinson_b(item[0], item[1])
            b.append(bLoop)

        # log
        print(f"a: {a} | b: {b}")

        # A = eos_A("peng-robinson", a, P, R, T)
        # B = eos_B(b, P, R, T)
        # * build polynomial eos equation f(Z)
        # *  alpha =  eos_alpha("peng-robinson", B)
        # #  beta = eos_beta("peng-robinson", A, B)
        # #  gamma = eos_gamma("peng-robinson", A, B)
        return 1.0

    #! a
    def pengRobinson_a(self, Pc, Tc, w) -> float:
        k = 0.37464 + 1.54226 * w - 0.26993 * math.pow(w, 2)
        alpha = math.pow(1 + k * (1 - math.sqrt(self.T / Tc)), 2)
        ac = (0.45723553 * (math.pow(CONST.R_CONST, 2) * math.pow(Tc, 2))) / Pc
        res = ac*alpha
        return res

    #! b
    def pengRobinson_b(self, Pc, Tc) -> float:
        return (0.07779607 * CONST.R_CONST * Tc) / Pc


# main
# if __name__ == "__main__":
#     main()
