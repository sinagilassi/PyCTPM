# test
import unittest
from ctpm import eosExe, showJson
import core.constants as CONST

# input
# argon
Argon = {
    "Tc": 150.9,  # K
    "Pc": 4.898,  # MPa
    "w": -0.004  # -
}

# operating conditions
# temperature (K)
T = 105.6
# pressure (MPa)
P = 0.496

# model input
modelInput = {
    "eos": "PR",
    "pressure": P,
    "temperature": T,
    "components": [Argon]
}

# single component estimation
res = eosExe(modelInput)
msg = "PR eos result {res}"
print(msg.format(res=res))

# showJson()
