# TEST
# -----

# import package/module
import numpy as np
from PyCTPM import component, pool, is_component_available, ExcessProperties

# check component available in database
ids = ["n-pentane", "benzene"]
res0 = is_component_available(ids)

# define a molecule
comp1 = component("n-pentane")
comp2 = component("benzene")

# ! VLE
# define a binary system
compList1 = [comp1, comp2]
pool1 = pool(compList1)

# feed properties
# mole fraction
MoFr = [0.5, 0.5]
# system pressure [Pa]
P1 = 101.325*1e3
# temperature [K]
T = 313.15

# activity coefficient
# res1 = ExcessProperties(compList1, MoFr)
# res1 = pool1.bubble_pressure(MoFr, T, model='modified-raoult')
# print(res1)

# Pxy
res2 = pool1.Pxy_binary(T, model='modified-raoult')
print(res2)
