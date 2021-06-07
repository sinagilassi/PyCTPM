# test
import unittest
from ctpm import eosExe, showJson, main
import core.constants as CONST

# input
# argon
components = [
    "Ar", "CO2"
]

xi = [0.5, 0.5]

# operating conditions
# temperature (K)
T = 105.6
# pressure (MPa)
P = 0.496
# molar volume (cm3/gmol)

# model input
modelInput = {
    "eos": CONST.PENG_ROBINSON,
    "pressure": P,
    "temperature": T,
    "components": components,
    "moleFraction": xi
}

# single component estimation
# res = eosExe(modelInput)
# msg = "PR eos result {res}"
# print(msg.format(res=res))

# showJson()

print(main().__doc__)
