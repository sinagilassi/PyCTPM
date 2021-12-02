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

# viscosity of components in the mixture [Pa.s]
Vi = [1.30232874e-05, 2.48896262e-05, 1.81758741e-05,
      2.65479558e-05, 1.72349516e-05, 1.59648895e-06]

# model input
# without Vi-MIX
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

# with Vi-MIX
modelInput2 = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
    "eq": 'DEFAULT',
    "Vi": Vi
}


# viscosity mixture [Pa.s]
res = thermo("Vi-MIX", modelInput1)
# log
print("Vi-MIX: ", res)
