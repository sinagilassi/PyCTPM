# TEST
# -----

# import package/module
import PyCTPM
from PyCTPM import thermo, comp, thermoInfo

# version
# print("PyCTPM version: ", PyCTPM.__version__)
# description
# print("PyCTPM description: ", PyCTPM.__description__)

# component available
# print(comp())

# NOTE
# components
compList = ["CO2", "CO", "H2O"]
# compList = ["CO2"]

# NOTE
# mole fraction
MoFri = [0.25, 0.25, 0.5]
# MoFri = [1]

# NOTE
# operating conditions
# pressure [Pa]
P = 1
# temperature [K]
T = 2

modelInput = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI"
}

# NOTE
# molecular weight
res = thermo("MW", modelInput)
print("res: ", res)

# mix molecular weight
res2 = thermo("MW-MIX", modelInput)
print("res2: ", res2)

# NOTE
# other properties
# property list
# propNameList = ["MW", "Tc", "Pc", "w", "dHf25", "dGf25"]

# for i in range(len(propNameList)):
#     print(thermo(propNameList[i], modelInput))

# NOTE
# property info
# all property info
# print(thermoInfo('ALL'))

# one property
# for i in range(len(propNameList)):
#     print(thermoInfo(propNameList[i]))
