# TEST
# -----

# import package/module
import numpy as np
from PyCTPM import component, ion, pool, solution, is_component_available, ExcessProperties

# check ions available in database

# define salt
# salt1 = component('')

# define ions
ion1 = ion('K(1+)')
ion2 = ion('Cl(1-)')

print('ion1 info: ', ion1.symbol, ion1.ion_type, ion1.charge)
print('ion2 info: ', ion2.symbol, ion2.ion_type, ion2.charge)


# FIXME
# define equilibrium reaction to set stoichiometric params
# solution
ions1 = [ion1, ion2]
# molality of ions
Moi1 = [5e-3, 5e-3]
# temperature [K]
T1 = 25 + 273.15
# solvent
solvent1 = 'water'
# solvent molality
SoMol1 = 5e-3
# reaction stoichiometric
ReSt = [1, 1, 1]

solution1 = solution(ions1, Moi1, solvent1, SoMol1, ReSt)

# ! mole fraction
# res0 = solution1.electrolyte_solution_mole_fraction()
# print("mole fraction : ", res0, np.sum(res0))

# calculate molal ionic strength
# res1 = solution1.calMolalIonicStrength(Moi1)
# print(f"molal ionic strength: {res1}")

#! calculate activity coefficient
res2 = solution1.activity_coefficient(T1, model='Pitzer')
print("res2: ", res2)
