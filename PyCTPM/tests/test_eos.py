# CALCULATE GAS DIFFUSIVITY
# ---------------------------

# import module/package
# externals
import numpy as np
import matplotlib.pyplot as plt
# import package/module
import PyCTPM
from PyCTPM import eos

# model input
# eos model
eosModel = 'PR'

# component phase
phase = "gas"

# component list
compList = ["C2H2"]

# mole fraction
MoFri = []

# temperature [K]
T = 250
# pressure [Pa]
P = 10*1e5

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
res = eos(modelInput)
# log
print("res: ", res)
