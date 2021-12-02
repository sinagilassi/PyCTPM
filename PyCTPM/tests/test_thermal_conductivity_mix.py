# CALCULATE GAS DIFFUSIVITY
# ---------------------------

# import module/package
# externals
import numpy as np
import matplotlib.pyplot as plt
# import package/module
import PyCTPM
from PyCTPM import thermo, thermoInfo


# component list
compList = ["H2", "CO2", "H2O", "CO", "CH4O", "C2H6O"]

# mole fraction
MoFri = [0.4998, 0.2499, 0.0001, 0.2499, 0.0001, 0.0001]

# temperature [K]
T = 523
# pressure [Pa]
P = 3500000

# thermal conductivity of components in the mixture [W/m.K]
ThCoi = [0.27458546, 0.03458594, 0.03965464, 0.03950025, 0.04261338, 0.0457769]

# model input
# without ThCoi
modelInput1 = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
    "eq": 'DEFAULT'
}

# with ThCoi
modelInput2 = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
    "eq": 'DEFAULT',
    "ThCoi": ThCoi
}

# thermal conductivity mixture [W/m.K]
res = thermo("ThCo-MIX", modelInput2)
# log
print("ThCo-MIX: ", res)
