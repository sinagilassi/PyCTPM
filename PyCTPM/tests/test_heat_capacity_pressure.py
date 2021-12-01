# CALCULATE GAS DIFFUSIVITY
# ---------------------------

# import module/package
# externals
import numpy as np
import matplotlib.pyplot as plt
# import package/module
import PyCTPM
from PyCTPM import thermo, comp, thermoInfo


# component list
compList = ["H2", "CO2", "H2O", "CO", "CH4O", "C2H6O"]

# mole fraction
MoFri = [0.4998, 0.2499, 0.0001, 0.2499, 0.0001, 0.0001]

# temperature [K]
T = 523
# pressure [Pa]
P = 3500000

# model input
modelInput = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
    "eq": 'DEFAULT'
}

# heat capacity of components at desired temp [kJ/kmol.K]
res = thermo("Cpp", modelInput)
# log
print("Cpp: ", res)

# mean heat capacity of components at desired temp (Tref = 25 C) [kJ/kmol.K]
res = thermo("Cpp-MEAN", modelInput)
# log
print("Cpp-MEAN: ", res)

# mixture heat capacity of components at desired temp (Tref = 25 C) [kJ/kmol.K]
res = thermo("Cpp-MIX", modelInput)
# log
print("Cpp-MIX: ", res)
