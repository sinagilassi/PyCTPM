# TEST
# -----

# import package/module
import PyCTPM
from PyCTPM import thermo, comp

# version
print("PyCTPM version: ", PyCTPM.__version__)
# description
print("PyCTPM description: ", PyCTPM.__description__)

# component available
print(comp())
#
# components
compList = ["CO2, CO, H2O"]
#

modelInput = {
    "components": compList
}

# res = thermo("molecular-weight", 2, 3)
# print("res: ", res)
