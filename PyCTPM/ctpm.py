# Python Chemical Thermodynamics for Process Modeling
# ----------------------------------------------------

# import packages/modules
import json
import os
# internals
import PyCTPM.core.constants as CONST
from PyCTPM.core import packageName, loadAllData, loadGeneralDataV1, loadGeneralDataInfo, loadGeneralDataV2, checkUnitGeneralData
from PyCTPM.docs import ExtCoreClass, eosCoreClass, dUtilityClass


def main():
    """ 
    Python Chemical Thermodynamics for Process Modeling
    """
    print(packageName)


def thermo(propName, modelInput, unit="SI"):
    '''
    estimate thermodynamic properties
    args:
        propName: property name
        modelInput:
            compList: component list
            MoFr: mole fraction
            params: 
                pressure
                temperature
            unit: set unit (SI, cgs)
    '''
    # try/except
    try:
        # get primary info
        compList = modelInput.get("components")

        # check component list
        compListUnique = dUtilityClass.buildComponentList(compList)

        # check property list
        propNameCheck = dUtilityClass.checkAppPropList(propName)

        # load all data
        dataLoaded = loadAllData(compListUnique)

        # class init
        ExtCoreClassSet = ExtCoreClass(
            dataLoaded, compListUnique, propNameCheck, modelInput, unit)

        # cal
        res = ExtCoreClassSet.propSet()
        return res
    except Exception as e:
        raise


def thermoInfo(propName='ALL'):
    '''
    display the property unit stored in general database such as Cp, Tc, ...
    args:
        propName: name of property
    '''
    try:
        # load general data info
        infoDataGeneral = loadGeneralDataInfo()[0]
        # get unit
        getUnit = checkUnitGeneralData(infoDataGeneral, propName)
        # res
        return getUnit
    except Exception as e:
        raise


def eosExe(modelInput):
    """
        eos init
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
    _eosCoreClass = eosCoreClass(
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
