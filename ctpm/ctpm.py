# Chemical Thermodynamics for Process Modeling
# ----------------------------------------------

# import packages/modules
import docs
import json
import os

# main


def main():
    print("Chemical Thermodynamics for Process Modeling")

# eos init


def eosExe(modelInput):
    print(f"modelInput {modelInput}")
    # eos method
    eosNameSet = modelInput['eos']
    # model input
    pressureSet = modelInput['pressure']
    temperatureSet = modelInput['temperature']
    componentsSet = modelInput['components']

    # select method
    selectEOS = {
        "PR": lambda P, T, components: docs._eosPR(P, T, components)
    }

    # return
    return selectEOS.get(eosNameSet)(pressureSet, temperatureSet, componentsSet)


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
