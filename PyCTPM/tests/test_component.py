# TEST
# -----

# import package/module
from PyCTPM import component

# model input
# eos model
eosModel = 'PR'

# temperature [K]
T = 373.15
# pressure [Pa]
P = 50*1e5

# define a molecule
comp1 = component("C6H6", "g")

# molecular weight
# print(comp1.MW)

# thermo list
# print(comp1.thermo_data())

# T/Tc
print(comp1.T_Tc_ratio(T))

# molar-volume [m^3/mol]
res1 = comp1.molar_volume(P, T)
print("molar-volume: ", res1[0])
print('Zs: ', res1[1])


# fugacity [Pa] & fugacity coefficient
res2 = comp1.fugacity(P, T)
print("fugacity: ", res2[0])
print("fugacity coefficient: ", res2[1])
