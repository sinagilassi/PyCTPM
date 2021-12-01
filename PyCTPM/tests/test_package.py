# TEST
# -----

# import package/module
import PyCTPM
from PyCTPM import PackInfo

# version
print("PyCTPM version: ", PyCTPM.__version__)
# description
print("PyCTPM description: ", PyCTPM.__description__)


# components
PackInfo.components()
