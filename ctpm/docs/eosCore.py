# Peng-Robinson (PR) equation of state
# --------------------------------------

# import packages/modules
import core.constants as CONST
from docs.eos import eosClass
from docs.eosData import dbClass
import math


# main
def main():
    print("EOS function list")


#! PR EOS
def _eosPR(P, T, components) -> float:
    print(P, T, components)

    # * eos class
    eos = eosClass(CONST.PR)
    # * eos database
    eosData = dbClass()

    #! test data
    dataLoad = eosData.loadData()
    print(dataLoad)

    # database
    # with open("")
    # Pc

    # Tc

    # w

    # * cal parameters
    # a = pengRobinson_a(R, T, Tc, Pc, w)
    # b = pengRobinson_b(R, P, Tc, Pc)
    # A = eos_A("peng-robinson", a, P, R, T)
    # B = eos_B(b, P, R, T)
    # #  alpha = this.eos_alpha("peng-robinson", B)
    # #  beta = this.eos_beta("peng-robinson", A, B)
    # #  gamma = this.eos_gamma("peng-robinson", A, B)

    return "OK"


#! a
def pengRobinson_a(R, T, Tc, Pc, w):
    k = 0.37464 + 1.54226 * w - 0.26993 * math.pow(w, 2)
    alpha = math.pow(1 + k * (1 - math.sqrt(T / Tc)), 2)
    ac = (0.45723553 * (math.pow(R, 2) * math.pow(Tc, 2))) / Pc
    res = ac*alpha
    return res

#! b


def pengRobinson_b(R, P, Tc, Pc):
    return (0.07779607 * CONST.R_CONST * Tc) / Pc


# main
if __name__ == "__main__":
    main()
