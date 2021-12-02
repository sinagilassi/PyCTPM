# Python Chemical Thermodynamics for Process Modeling

![PyPI - License](https://img.shields.io/pypi/l/PyCTPM) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/PyCTPM) ![PyPI](https://img.shields.io/pypi/v/PyCTPM) ![PyPI - Downloads](https://img.shields.io/pypi/dm/PyCTPM)

Python Chemical Thermodynamics for Process Modeling (PyCTPM) is an open-source package which can be used to estimate thermodynamic properties in a typical process modeling.
The current version consists of methods for estimation of gas properties as:

1. Diffusivity coefficient (DiCo)
2. Heat capacity at constant pressure (Cpp)
3. Thermal conductivity (ThCo)
4. Viscosity (Vi)

The above thermodynamic properties can be estimate for single and multi-component systems.

Note:

DiCo-MIX is the Diffusivity coefficient for a multi-component system

# Example

You can also run PyCTPM on Google Colaboratory as:

1. [Example 1](https://colab.research.google.com/drive/1vyWxL_OKn304sb-yPLKisKc70lDozwtl?usp=sharing)
2. [Example 2: mixture properties](https://colab.research.google.com/drive/1ZbMuwkVkTxYNhVCnyfBkEvDrez_aH8bx?usp=sharing)

# Getting started

You can install this package

```bash
pip install PyCTPM
```

## Documentation

PyCTPM can be initialized as follows:

1- COMPONENT SELECTION

In order to define these components: H2; CO2; H2O; CO; CH3OH; DME

this code is automatically converted to python as:

```python
# component list
compList = ["H2","CO2","H2O","CO","CH4O","C2H6O"]
```

2- OTHER PROPERTIES

```python
# Mole fraction of each component is defined as an element in a python list as:
MoFri = [0.50, 0.25, 0.0001, 0.25, 0.0001, 0.0001]

# temperature [K]
T = 523

# pressure [Pa]
P = 3500000

# model input
modelInput = {
    "components": compList,
    "MoFri": MoFri,
    "params": {
        "P": P,
        "T": T,
    },
    "unit": "SI",
    "eq": 'DEFAULT'
}
```

Note:

The modelInput keys, unit and eq, they should be set as above in the current version.

3- ESTIMATE PROPERTIES

```python

# import package/module
import PyCTPM
from PyCTPM import thermo, thermoInfo, PackInfo

# version
print("PyCTPM version: ", PyCTPM.__version__)

# description
print("PyCTPM description: ", PyCTPM.__description__)

# component available in the database
PackInfo.components()

# property
PackInfo.properties()

# property list
propNameList = ["MW", "Tc", "Pc", "w", "dHf25", "dGf25"]

for i in range(len(propNameList)):
    print(thermo(propNameList[i], modelInput))

# property info
# all property info
print(thermoInfo('ALL'))

# one property
for i in range(len(propNameList)):
    print(thermoInfo(propNameList[i]))

# diffusivity coefficient of components in the mixture
res = thermo("DiCo-MIX", modelInput)
# log
print("Dij: ", res)

# heat capacity of components at desired temp [kJ/kmol.K]
res = thermo("Cpp", modelInput)
# log
print("Cpp: ", res)

# mean heat capacity of components at desired temp (Tref = 25 C) [kJ/kmol.K]
res = thermo("Cpp-MEAN", modelInput)
# log
print("Cpp-MEAN: ", res)

# mixture heat capacity of components at desired temp (Tref = 25 C) [kJ/kmol.K]
res = thermo("Cpp-MIX", modelInput)
# log
print("Cpp-MIX: ", res)

# thermal conductivity of components in the mixture [W/m.K]
res = thermo("ThCo", modelInput)
# log
print("ThCoi: ", res)

# thermal conductivity in the mixture [W/m.K]
res = thermo("ThCo-MIX", modelInput)
# log
print("ThCo-MIX: ", res)

# viscosity of components [Pa.s]
res = thermo("Vi", modelInput)
# log
print("Vi: ", res)

# viscosity mixture [Pa.s]
res = thermo("Vi-MIX", modelInput)
# log
print("Vi-MIX: ", res)

```

## FAQ

For any question, you can contact me on [LinkedIn](https://www.linkedin.com/in/sina-gilassi/) or [Twitter](https://twitter.com/sinagilassi).

## Authors

- [@sinagilassi](https://www.github.com/sinagilassi)
