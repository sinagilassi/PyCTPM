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

# solution
ions1 = [ion1, ion2]
# molality
Moi1 = [5e-3, 5e-3]
solvent1 = 'water'
solution1 = solution(ions1, solvent1)
res1 = solution1.calMolalIonicStrength(Moi1)
print(f"molal ionic strength: {res1}")
