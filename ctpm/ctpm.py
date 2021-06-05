# Chemical Thermodynamics for Process Modeling
# ----------------------------------------------

# import packages/modules
import docs
import json
import os
import core.constants as CONST

# main


def main():
    print("Chemical Thermodynamics for Process Modeling")

# eos init


def eosExe(modelInput):
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

    # * init eos class
    _eosCoreClass = docs.eosCoreClass(
        pressureSet, temperatureSet, componentsSet, eosNameSet)
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
