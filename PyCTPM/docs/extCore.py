# EXTRACT DATA
# -------------

# import module/packages
import numpy as np
# internals
from PyCTPM.docs.dUtility import dUtilityClass
from PyCTPM.database import DATABASE_GENERAL_ITEMS, DATABASE_INFO
from PyCTPM.docs.gasTransPor import calGasDiffusivity
from PyCTPM.docs.dThermo import calHeatCapacityAtConstantPressure, calMeanHeatCapacityAtConstantPressure, \
    calMixtureHeatCapacityAtConstantPressure, calGasViscosity, calMixPropertySelection, calGasThermalConductivity


class ExtCoreClass:
    '''
    code for extracting data from database (csv, txt, ...)
    '''

    def __init__(self, data, compList, propName, modelInput, unit="SI"):
        '''
        data: all data csv
        propName: property name such as MW
        modelInput:
            components: component list
            params:
                P: pressure
                T: temperature
            unit: SI (default)
        '''
        self.data = data
        self.compList = compList
        self.propName = propName
        self.modelInput = modelInput
        self.unit = unit

    def dataSet(self, dataName="GENERAL"):
        '''
        load data from its name
        '''
        return self.data[dataName]

    def propSet(self):
        '''
        calculate the property for single and mixture cases
        '''
        # prop fun list
        propFunList = {
            "general-data": dUtilityClass.extractCompData,
            "molecular-weight-mix": dUtilityClass.mixtureMolecularWeight,
            "diffusivity-coefficient-mix": 1
        }

        # general prop name
        propNameList = DATABASE_GENERAL_ITEMS
        # prop name set
        propNameSet = self.propName

        # get info
        # component list
        compList = self.modelInput.get('components', -1)

        # check
        if propNameSet in propNameList:
            # NOTE
            # data
            setData = self.dataSet()
            return np.array(propFunList['general-data'](setData, propNameSet))
        elif propNameSet == "MW-MIX":
            # NOTE
            # data
            setData = self.dataSet()
            # component data
            MWi = np.array(
                propFunList['general-data'](setData, "MW"))
            MoFri = np.array(self.modelInput.get('MoFri'))
            return propFunList['molecular-weight-mix'](MoFri, MWi)
        elif propNameSet == "DiCo-MIX":
            # NOTE
            # diffusivity coefficient
            # data
            setData = self.dataSet()
            # molecular weight [g/mol]
            MWi = np.array(
                propFunList['general-data'](setData, "MW"))
            # critical temperature [K]
            Tci = np.array(
                propFunList['general-data'](setData, "Tc"))
            # critical pressure [Pa]
            Pci = np.array(
                propFunList['general-data'](setData, "Pc"))

            # params
            params = {
                "MoFri": self.modelInput['MoFri'],
                "T": self.modelInput['params']['T'],
                "P": self.modelInput['params']['P'],
                "MWi": MWi,
                "CrTei": Tci,
                "CrPri": Pci
            }

            # equation
            eqSet = self.modelInput.get('eq', -1)
            eq = 1 if eqSet == "DEFAULT" else eqSet

            # call
            DiCoi = calGasDiffusivity(compList, params, eq)
            # res
            return DiCoi
        elif propNameSet == "Cpp":
            # NOTE
            # load data
            setData = self.dataSet(DATABASE_INFO[1]['name'])
            # temp [K]
            T = self.modelInput['params']['T']

            # params
            params = {
                "setData": setData
            }

            # select calculation method
            # equation
            eqSet = self.modelInput.get('eq', -1)
            eq = 1 if eqSet == "DEFAULT" else eqSet

            # heat capacity at constant pressure [kJ/kmol.K]
            Cppi = calHeatCapacityAtConstantPressure(compList, T, params, eq)
            # res
            return Cppi
        elif propNameSet == "Cpp-MEAN":
            # NOTE
            # load data
            setData = self.dataSet(DATABASE_INFO[1]['name'])
            # temp [K]
            T = self.modelInput['params']['T']

            # params
            params = {
                "setData": setData
            }

            # select calculation method
            # equation
            eqSet = self.modelInput.get('eq', -1)
            eq = 1 if eqSet == "DEFAULT" else eqSet

            # mean heat capacity at constant pressure [kJ/kmol.K]
            CppiMean = calMeanHeatCapacityAtConstantPressure(
                compList, params, eq, T)
            # res
            return CppiMean
        elif propNameSet == "Cpp-MIX":
            # NOTE
            # load data
            setData = self.dataSet(DATABASE_INFO[1]['name'])
            # temp [K]
            T = self.modelInput['params']['T']

            # params
            params = {
                "setData": setData
            }

            # select calculation method
            # equation
            eqSet = self.modelInput.get('eq', -1)
            eq = 1 if eqSet == "DEFAULT" else eqSet

            # REVIEW
            # mean heat capacity at constant pressure [kJ/kmol.K]
            CppiMeanInput = self.modelInput.get('Cppi-MEAN', -1)
            # check user input
            if CppiMeanInput == -1:
                CppiMean = calMeanHeatCapacityAtConstantPressure(
                    compList, params, eq, T)
            else:
                CppiMean = np.array(CppiMeanInput)

            # mole fraction
            MoFri = np.array(self.modelInput.get('MoFri'))

            # mixture heat capacity at constant pressure [kJ/kmol.K]
            CppMix = calMixtureHeatCapacityAtConstantPressure(MoFri, CppiMean)
            # return
            return CppMix
        elif propNameSet == "Vi":
            # NOTE
            # load data
            setData = self.dataSet(DATABASE_INFO[3]['name'])
            # temp [K]
            T = self.modelInput['params']['T']
            # viscosity [Pa.s]
            Vi = calGasViscosity(compList, T, setData)
            # return
            return Vi
        elif propNameSet == "Vi-MIX":
            # NOTE
            # mixture viscosity [Pa.s]
            # load data
            setData = self.dataSet(DATABASE_INFO[3]['name'])
            setData_2 = self.dataSet()
            # temp [K]
            T = self.modelInput['params']['T']

            # REVIEW
            # viscosity [Pa.s]
            ViInput = self.modelInput.get('Vi', -1)
            # check user input
            if ViInput == -1:
                Vi = calGasViscosity(compList, T, setData)
            else:
                Vi = np.array(ViInput)

            # select calculation method
            # equation
            eqSet = self.modelInput.get('eq', -1)
            eq = 1 if eqSet == "DEFAULT" else eqSet

            # molecular weight [g/mol]
            MWi = np.array(
                propFunList['general-data'](setData_2, "MW"))

            # mole fraction
            MoFri = np.array(self.modelInput.get('MoFri'))

            # params
            params = {
                "Xi": Vi,
                "MWi": MWi,
                "MoFri": MoFri
            }

            # mixture
            ViMix = calMixPropertySelection(params, eq)
            # return
            return ViMix
        elif propNameSet == "ThCo":
            # NOTE
            # thermal conductivity [W/m.K]
            # load data
            setData = self.dataSet(DATABASE_INFO[2]['name'])
            # temp [K]
            T = self.modelInput['params']['T']
            # cal [W/m.K]
            ThCoi = calGasThermalConductivity(compList, T, setData)
            # return
            return ThCoi
            pass
        elif propNameSet == "ThCo-MIX":
            # NOTE
            # thermal conductivity [W/m.K]
            # load data
            setData = self.dataSet(DATABASE_INFO[2]['name'])
            setData_2 = self.dataSet()
            # temp [K]
            T = self.modelInput['params']['T']

            # REVIEW
            # thermal conductivity [W/m.K]
            ThCoiInput = self.modelInput.get('ThCoi', -1)
            # check user input
            if ThCoiInput == -1:
                ThCoi = calGasThermalConductivity(compList, T, setData)
            else:
                ThCoi = np.array(ThCoiInput)

            # select calculation method
            # equation
            eqSet = self.modelInput.get('eq', -1)
            eq = 1 if eqSet == "DEFAULT" else eqSet

            # molecular weight [g/mol]
            MWi = np.array(
                propFunList['general-data'](setData_2, "MW"))

            # mole fraction
            MoFri = np.array(self.modelInput.get('MoFri'))

            # params
            params = {
                "Xi": ThCoi,
                "MWi": MWi,
                "MoFri": MoFri
            }

            # mixture
            ThCoMIX = calMixPropertySelection(params, eq)
            # return
            return ThCoMIX
        else:
            raise Exception("property name is not valid!")
