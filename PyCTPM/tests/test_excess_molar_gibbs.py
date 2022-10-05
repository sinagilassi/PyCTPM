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

# csvFile
comp1 = component("di-isopropyl-ether")
comp2 = component("1-propanol")

# csvFile2
# comp1 = component("ethanol")
# comp2 = component("methylbutyl-ether")

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
T = 303.15

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
csvFile2 = r'E:\Web App\CTPM\data\Pxy2.csv'
#! Margules two-parameter
# res0 = pool1.Margules_parameter_estimation(csvFile, mode='2-parameter')
# print(res0)

#! Wilson equation
# res0 = pool1.Wilson_parameter_estimation(csvFile2, plot_result=True)
# print(res0)

#! NRTL equation
boundSet = [[0, 2], [0, 2]]
res0 = pool1.NRTL_parameter_estimation(
    csvFile, bounds=boundSet, plot_result=True)
print(res0)

# define activity coefficient model
# AcCoModel = {
#     'name': 'wilson',
#     'params': res0
# }
# res2 = pool1.Pxy_binary(T, model='modified-raoult',
#                         activity_coefficient_model=AcCoModel)
# print(res2)

# activity coefficient at different temperature
# res1 = pool1.wilson_activity_coefficient()
