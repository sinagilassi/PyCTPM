# TEST
# -----

# import package/module
import numpy as np
from PyCTPM import component, pool

# model input
# eos model
eosModel = 'PR'

# temperature [K]
T = 50 + 273.15
# pressure [Pa]
P = 1*1e5
Ps = np.array([1, 100, 1000])*1e5

# define a molecule
comp1 = component("C6H6", "g")
comp2 = component("C7H8", "l")

# molecular weight
# print(comp1.MW)

# properties
# print(comp1.thermo_properties_data)
# print(comp1.vapor_pressure_antoine_data)

# thermo list
# print(comp1.thermo_data())

# T/Tc
# print(comp1.T_Tc_ratio(T))

# vapor-pressure
# print(comp1.vapor_pressure(T))
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

# ! VLE
# define a binary system
compList1 = [comp1, comp2]
# mole fraction
moleFraction1 = [0.26, 0.74]
# system pressure [Pa]
P1 = 101.3*1e3
pool1 = pool(compList1)
# ->
# print(pool1.component_list[1].symbol)

# bubble temperature
bpt0 = pool1.bubble_temperature(moleFraction1, P1)
print("bubble temperature: ", bpt0)
