# Python Chemical Thermodynamics for Process Modeling
# ----------------------------------------------------

# import packages/modules
import json
import os
# internals
import PyCTPM.core.constants as CONST
from PyCTPM.core import packageName, loadAllData, loadGeneralDataV1, \
    loadGeneralDataInfo, loadGeneralDataV2, checkUnitGeneralData, loadDataEOS
from PyCTPM.docs import ExtCoreClass, eosCoreClass, dUtilityClass
from PyCTPM.docs.fugacity import FugacityClass


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


def eos(modelInput):
    """
    # Estimation of molar-volume at fixed pressure and temperature using a EOS as:
        1. van der Waals
        2. Redlich-Kwong and Soave
        3. Peng-Robinson

        Z is determined thereby molar-volume is calculated.
        eosMode: pure/mixture 

    args:
        modelInput:
            eos-name: eos equation name
            compList: component list
            MoFr: mole fraction
            params: 
                pressure [Pa]
                temperature [K]
            unit: set unit (SI: default, cgs)

    output:
        pressure: fixed pressure [Pa]
        temperature: fixed temperature [K]
        molar-volumes: for all Z [m^3/mol]
        gas: for the highest Z [m^3/mol]
        liquid: for the lowest Z [m^3/mol]
        Z: compressibility coefficient [-]
        eos-params: a,b,A,B,alpha,beta,gamma

    """
    # get primary info
    compList = modelInput.get("components")
    # eos method
    eosModel = modelInput.get('eos-model')
    # ole fraction
    moleFraction = modelInput.get('MoFr', 1)
    # params
    params = modelInput.get('params')

    # check component list
    compListUnique = dUtilityClass.buildComponentList(compList)

    # load all data
    compData = loadDataEOS(compListUnique)

    # * init eos class
    _eosCoreClass = eosCoreClass(
        compData, compList, eosModel, moleFraction, params)
    # select method
    selectEOS = {
        "PR": lambda: _eosCoreClass._eosPR()
    }

    # return
    return selectEOS.get(eosModel)()


def fugacity(modelInput):
    '''
    # Calculate fugacity for gas/liquid/solid phase

    args:
        modelInput:
            eos-name: eos equation name
            phase: component phase (gas/liquid/solid)
            compList: component list
            MoFr: mole fraction
            params: 
                pressure [Pa]
                temperature [K]
            unit: set unit (SI: default, cgs)  
    '''
    try:
        # get primary info
        compList = modelInput.get("components")
        # eos method
        eosModel = modelInput.get('eos-model')
        # phase
        phase = modelInput.get("phase")
        # ole fraction
        moleFraction = modelInput.get('MoFr', 1)
        # params
        params = modelInput.get('params')

        # check component list
        compListUnique = dUtilityClass.buildComponentList(compList)

        # load all data
        compData = loadDataEOS(compListUnique)

        # * init eos class
        _eosCoreClass = eosCoreClass(
            compData, compList, eosModel, moleFraction, params)

        # select method
        selectEOS = {
            "PR": lambda: _eosCoreClass._eosPR()
        }
        # res
        _eosRes = selectEOS.get(eosModel)()

        # * init fugacity class
        _fugacityClass = FugacityClass(compData, compList, _eosRes, phase)

        # select method
        selectFugacity = {
            "PR": lambda: _fugacityClass.FugacityPR()
        }

        # res
        _fugacityRes = selectFugacity.get(eosModel)()

        # return
        return _fugacityRes
    except Exception as e:
        raise Exception("Fugacity calculation failed!, ", e)


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
