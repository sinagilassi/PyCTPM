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

# thermal conductivity of components in the mixture [W/m.K]
res = thermo("ThCo", modelInput)
# log
print("ThCoi: ", res)

# viscosity mixture [W/m.K]
res = thermo("ThCo-MIX", modelInput)
# log
print("ThCo-MIX: ", res)
