# TEST
# -----

# import package/module
import numpy as np
from PyCTPM import component

# model input
# eos model
eosModel = 'PR'

# temperature [K]
T = 50 + 273.15
# pressure [Pa]
P = 1*1e5
Ps = np.array([1, 100, 1000])*1e5

# define a molecule
comp1 = component("CO2", "g")

# molecular weight
# print(comp1.MW)

# thermo list
# print(comp1.thermo_data())

# T/Tc
# print(comp1.T_Tc_ratio(T))

# vapor-pressure
print(comp1.vapor_pressure(T))
# print(comp1.vapor_pressure(T, mode='eos'))


# molar-volume [m^3/mol]
# res1 = comp1.molar_volume(P, T)
# print("molar-volume: ", res1[0])
# print('eos-res: ', res1[1])


# fugacity [Pa] & fugacity coefficient
# res2 = comp1.fugacity(P, T)
# print("fugacity: ", res2[0])

# for i in Ps:
#     _res = comp1.fugacity(i, T)
#     print("fugacity: ", _res[0])
