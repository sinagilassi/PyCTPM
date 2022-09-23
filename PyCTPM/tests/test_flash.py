# TEST
# -----

# import package/module
import numpy as np
from PyCTPM import component, pool, is_component_available

# check component available in database
ids = ["benzene", "toluene", "ethylbenzene"]
res0 = is_component_available(ids)

# define a molecule
comp1 = component("benzene")
comp2 = component("toluene")
comp3 = component("ethylbenzene")

# ! VLE
# define a binary system
compList1 = [comp1, comp2, comp3]

# ! set system
pool1 = pool(compList1)

# ! feed properties
# mole fraction
moleFraction1 = [0.4, 0.4, 0.2]
# feed pressure [Pa]
Pf = 26664.5
# temperature [K]
T = 50 + 273.15
# feed flowrate [mol/min]
F = 100

# ! flash properties
# flash pressure [Pa]
Pf0 = 13332.2
# flash temperature [K]
Tf0 = T

# ! run
flash0 = pool1.flash_isothermal(moleFraction1, Pf0, Tf0, Pf)
print("flash0: ", flash0)
