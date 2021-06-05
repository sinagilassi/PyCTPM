# test
import unittest
from ctpm import eosExe, showJson
import core.constants as CONST

# input
# argon
components = [
    "Ar", "CO"
]

# operating conditions
# temperature (K)
T = 105.6
# pressure (MPa)
P = 0.496

# model input
modelInput = {
    "eos": CONST.PENG_ROBINSON,
    "pressure": P,
    "temperature": T,
    "components": components
}

# single component estimation
res = eosExe(modelInput)
msg = "PR eos result {res}"
print(msg.format(res=res))

# showJson()
