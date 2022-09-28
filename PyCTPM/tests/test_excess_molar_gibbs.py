# TEST
# -----

# import package/module
import numpy as np
from PyCTPM import component, pool, is_component_available, ExcessProperties

# check component available in database
# ids = ["n-pentane", "benzene"]
# res0 = is_component_available(ids)

# define a molecule
# comp1 = component("water")
# comp2 = component("ethanol")

comp1 = component("di-isopropyl-ether")
comp2 = component("1-propanol")


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

#! activity coefficient
# res1 = ExcessProperties(compList1, MoFr)
# res1 = pool1.bubble_pressure(MoFr, T, model='modified-raoult')
# print(res1)

#! Pxy
# res2 = pool1.Pxy_binary(T, model='modified-raoult')
# print(res2)

#! Margules one-parameter
# mole fraction
xi_exp = [[0.3, 1-0.3]]
yi_exp = [[0.23, 1-0.23]]
# pressure [Pa]
P_exp = [10.1e3]
# temperature [K]
T_exp = 30 + 273.15
# find Margules one-parameter
# res3 = pool1.Margules_1Parameter(xi_exp, yi_exp, P_exp, T_exp)
# print(res3)
# activity coefficient
xi_exp_2 = [0.2, 1-0.2]
# res4 = pool1.Margules_activity_coefficient(xi_exp_2, res3)
# print(res4)

#! load csv data (P,xi,y1) for binary system
csvFile = r'E:\Web App\CTPM\data\Pxy1.csv'
res0 = pool1.Margules_parameter_estimation(csvFile, mode='2-parameter')
print(res0)

#! Margules two-parameter
