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
compList = ["C5H12"]

# mole fraction
MoFri = []

# temperature [K]
T = 373.15
# pressure [Pa]
P = 1e5

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
