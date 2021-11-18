# TEST
# -----

# import package/module
import PyCTPM
from PyCTPM import thermo

# version
print("PyCTPM version: ", PyCTPM.__version__)
# description
print("PyCTPM description: ", PyCTPM.__description__)

#
res = thermo("molecular-weight", 2, 3)
print("res: ", res)
