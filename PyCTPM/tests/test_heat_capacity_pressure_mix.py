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

# mean heat capacity of components at desired temp (Tref = 25 C) [kJ/kmol.K]
CppiMEAN = [28.60520155, 41.08544857, 34.75029085,
            29.62105504, 53.71405537, 79.34119544]

# model input
# without CppMEAN
modelInput1 = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
    "eq": 'DEFAULT',
}

# with CppMEAN
modelInput2 = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
    "eq": 'DEFAULT',
    "Cppi-MEAN": CppiMEAN
}

# mixture heat capacity of components at desired temp (Tref = 25 C) [kJ/kmol.K]
res = thermo("Cpp-MIX", modelInput1)
# log
print("Cpp-MIX: ", res)
