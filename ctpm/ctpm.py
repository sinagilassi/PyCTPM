# Chemical Thermodynamics for Process Modeling in Python (CTPMPy)
# ---------------------------------------------------------------

# import packages/modules
import docs
import json
import os
import core.constants as CONST

# main


def main():
    print("Chemical Thermodynamics for Process Modeling")


def eosExe(modelInput):
    """
    eos init

    Args:
        modelInput ([type]): model input data

    Returns:
        [type]: [description]
    """
    # print(f"modelInput {modelInput}")
    # eos method
    eosNameSet = modelInput['eos']
    print(f"eosNameSet: {eosNameSet}")
    # model input
    pressureSet = modelInput['pressure']
    print(f"pressureSet: {pressureSet}")
    temperatureSet = modelInput['temperature']
    print(f"temperatureSet: {temperatureSet}")
    componentsSet = modelInput['components']
    print(f"componentsSet: {componentsSet}")
    moleFractionSet = modelInput['moleFraction']
    print(f"moleFractionSet: {moleFractionSet}")

    # * init eos class
    _eosCoreClass = docs.eosCoreClass(
        pressureSet, temperatureSet, componentsSet, eosNameSet, moleFractionSet)
    # select method
    selectEOS = {
        "PR": lambda: _eosCoreClass._eosPR()
    }

    # return
    return selectEOS.get(eosNameSet)()


#! test json
def showJson():
    appPath = "database\component.json"
    print(appPath)
    with open(appPath) as f:
        data = json.load(f)
        print(data)
    #  lookup
    res = data["payload"]
    print(res)
    return res


if __name__ == "__main__":
    main()
