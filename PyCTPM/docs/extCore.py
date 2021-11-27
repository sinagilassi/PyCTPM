# EXTRACT DATA
# -------------

# import module/packages
import numpy as np
# internals
from PyCTPM.docs.dUtility import dUtilityClass


class ExtCoreClass:
    '''
    code for extracting data from database (csv, txt, ...)
    '''

    def __init__(self, dataGeneral, compList, propName, modelInput, unit="SI"):
        '''
        dataGeneral: general data
        propName: property name such as MW
        modelInput:
            components: component list
            params:
                P: pressure
                T: temperature
            unit: SI (default)
        '''
        self.dataGeneral = dataGeneral
        self.compList = compList
        self.propName = propName
        self.modelInput = modelInput
        self.unit = unit

    def propSet(self):
        # prop fun list
        propFunList = {
            "general-data": dUtilityClass.extractGenProp,
            "molecular-weight-mix": dUtilityClass.mixtureMolecularWeight
        }

        # general prop name
        propNameList = ["MW", "Tc", "Pc", "w", "dHf25", "dGf25"]
        # prop name set
        propNameSet = self.propName

        # check
        if propNameSet in propNameList:
            # NOTE
            return np.array(propFunList['general-data'](self.dataGeneral, propNameSet))
        elif propNameSet == "MW-MIX":
            # NOTE
            # component data
            MWi = np.array(
                propFunList['general-data'](self.dataGeneral, "MW"))
            MoFri = np.array(self.modelInput.get('MoFri'))
            return propFunList['molecular-weight-mix'](MoFri, MWi)
        else:
            raise Exception("property name is not valid!")
