# CALCULATE FUGACITY
# -------------------

# import module/package
# externals
import numpy as np
import matplotlib.pyplot as plt
# import package/module
import PyCTPM
from PyCTPM import eos
from PyCTPM.ctpm import fugacity

# model input
# eos model
eosModel = 'PR'

# component phase
phase = "gas"

# component list
compList = ["H2O"]

# mole fraction
MoFri = []

# temperature [K]
T = 200 + 273.15
# pressure [Pa]
P = 15.55*1e5

# model input
modelInput = {
    "eos-model": eosModel,
    "phase": phase,
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
}

# eos
res = fugacity(modelInput)
# log
print("res: ", res)
