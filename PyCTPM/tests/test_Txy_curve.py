# TEST
# -----

# import package/module
import numpy as np
from PyCTPM import component, pool, is_component_available

# check component available in database
ids = ["methanol", "acetone"]
res0 = is_component_available(ids)

# define a molecule
comp1 = component("methanol")
comp2 = component("acetone")

# ! VLE
# define a binary system
compList1 = [comp1, comp2]
pool1 = pool(compList1)

# feed properties
# system pressure [Pa]
P1 = 101.325*1e3
# temperature [K]
T = 50 + 273.15

# Txy binary
bpt0 = pool1.Txy_binary(P1)
print("bubble temperature: ", bpt0)
