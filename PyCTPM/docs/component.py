# ELEMENT (MOLECULE/ELECTROLYTE)
# -------------------------------

# package/module list
import string
import numpy as np
import pandas as pd
# local
from PyCTPM.core.package import PackInfo
from PyCTPM.core.utilities import loadGeneralDataV2, loadGeneralDataV3
from PyCTPM.docs.eosCore import eosCoreClass
from PyCTPM.docs.fugacity import FugacityClass


class Component:
    '''
    component class defines a molecule/electrolyte which provide:
        1. chemical/physical properties

    initialization:
        id: component name, symbol (default)
    '''

    # thermodynamic property list
    thermoPropList = [
        'molecular weight - MW [g/mol]',
        'critical temperature - Tc [K]',
        'critical pressure - Pc [bar]',
        'critical molar-volume - Vc [cm^3/mol]',
        'critical compressibility factor - Zc [-]',
        'acentric factor - w [-]',
        'standard enthalpy of formation - dHf25 [kJ/mol]',
        'standard Gibbs free energy of formation - dGf25 [kJ/mol]'
    ]

    _symbol = ''
    _MW = 0
    _Tc = 0
    _Pc = 0
    _Vc = 0
    _Zc = 0
    _w = 0
    _dHf25 = 0
    _dGf25 = 0
    _state = "g"

    # ! calculated
    _T_Tc_ratio = 0

    def __init__(self, id, state):
        self.id = str(id)
        self.state = state
        # * load data
        self.thermoPropData = self.__loadComponentData()
        # * set data
        self.__setThermoProp()

    # ! property list

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @property
    def MW(self):
        return self._MW

    @MW.setter
    def MW(self, value):
        self._MW = value

    @property
    def Tc(self):
        return self._Tc

    @Tc.setter
    def Tc(self, value):
        self._Tc = value

    @property
    def Pc(self):
        return self._Pc

    @Pc.setter
    def Pc(self, value):
        self._Pc = value

    @property
    def Vc(self):
        return self._Vc

    @Vc.setter
    def Vc(self, value):
        self._Vc = value

    @property
    def Zc(self):
        return self._Zc

    @Zc.setter
    def Zc(self, value):
        self._Zc = value

    @property
    def w(self):
        return self._w

    @w.setter
    def w(self, value):
        self._w = value

    @property
    def dHf25(self):
        return self._dHf25

    @dHf25.setter
    def dHf25(self, value):
        self._dHf25 = value

    @property
    def dGf25(self):
        return self._dGf25

    @dGf25.setter
    def dGf25(self, value):
        self._dGf25 = value

    # ! static methods

    @staticmethod
    def list():
        '''
        show a list of components available with their thermodynamic parameters such as:
            1. molecular weight
            2. critical temperature
            3. critical pressure
            4. critical molar-volume
            5. critical compressibility factor
            6. acentric factor
            7. enthalpy of formation
            8. Gibbs energy of formation
        '''
        try:
            PackInfo.components()
        except print(0):
            pass

    def __loadComponentData(self):
        '''
        load all thermodynamic properties
        '''
        try:
            # component id
            compId = self.id

            if isinstance(compId, str):
                # property list
                propList = loadGeneralDataV3([self.id], [self.state])
                # res
                return propList

            else:
                raise Exception(
                    "component id should be a string such as `CO2`")
        except Exception as e:
            raise Exception("load component data failed!")

    def __setThermoProp(self):
        '''
        set thermodynamic properties
        '''
        try:
            # symbol
            self.symbol = self.thermoPropData.get("component-symbol", "")
            # molecular weight
            self.MW = float(self.thermoPropData.get("MW", -1))
            # critical temperature
            self.Tc = float(self.thermoPropData.get("Tc", -1))
            # critical pressure
            self.Pc = float(self.thermoPropData.get("Pc", -1))
            # critical molar-volume
            self.Vc = float(self.thermoPropData.get("Vc", -1))
            # critical compressibility factor
            self.Zc = float(self.thermoPropData.get("Zc", -1))
            # acentric factor
            self.w = float(self.thermoPropData.get("w", -1))
            # enthalpy of formation
            self.dHf25 = float(self.thermoPropData.get("dHf25", -1))
            # Gibbs energy of formation
            self.dGf25 = float(self.thermoPropData.get("dGf25", -1))

        except Exception as e:
            raise Exception("set thermo prop failed!")

    def thermo_data(self):
        '''
        show a list of thermo properties
        '''
        try:
            df = pd.DataFrame(self.thermoPropData, index=[1])
            return df
        except Exception as e:
            raise Exception("thermo prop failed!")

    def T_Tc_ratio(self, T):
        '''
        calculate the ratio of T and Tc
        '''
        return T/self.Tc

    def molar_volume(self, P, T, eos_model='PR'):
        '''
        estimate molar-volume at specified pressure and temperature

        args:
            P: pressure [Pa]
            T: temperature [K]
            eos_model: name of eos model
                1. van der Waals (VW)
                2. Redlich-Kwong and Soave (RKS)
                3. Peng-Robinson (PR)

        return:
            Vms: molar-volume list for all Z [m^3/mol]
            Vmg: for the highest Z [m^3/mol]
            Vml: for the lowest Z [m^3/mol]
            Z: compressibility coefficient [-]
            P: fixed pressure [Pa]
            T: fixed temperature [K]
            eos-params: a,b,A,B,alpha,beta,gamma
        '''
        try:
            # eos params
            params = {
                "pressure": P,
                "temperature": T
            }

            # * init eos class
            _eosCoreClass = eosCoreClass(
                [self.thermoPropData], [self.symbol], eos_model, [1], params)

            # select method
            selectEOS = {
                "PR": lambda: _eosCoreClass._eosPR(),
                "VW": 1,
                "RKS": 1
            }

            return selectEOS.get(eos_model)()

        except Exception as e:
            raise Exception("fugacity failed!")

    def fugacity(self, P, T, eos_model='PR', phase='gas'):
        '''
        estimate fugacity at specified pressure and temperature

        args:
            P: pressure [Pa]
            T: temperature [K]
            eos_model: name of eos model
                1. van der Waals (VW)
                2. Redlich-Kwong and Soave (RKS)
                3. Peng-Robinson (PR)
            phase: component phase (solid/liquid/gas)

        return:
            f: fugacity [Pa]
            phi: fugacity coefficient [-]
        '''
        try:
            # eos params
            params = {
                "pressure": P,
                "temperature": T
            }

            # * init eos class
            _eosCoreClass = eosCoreClass(
                [self.thermoPropData], [self.symbol], eos_model, [1], params)

            # select method
            selectEOS = {
                "PR": lambda: _eosCoreClass._eosPR(),
                "VW": 1,
                "RKS": 1
            }

            _eosRes = selectEOS.get(eos_model)()

            _eosResSet = {
                "molar-volumes": _eosRes[0],
                "Z": _eosRes[1],
                "eos-params": _eosRes[2],
                "T_Tc_ratio": _eosRes[3],
            }

            # * init fugacity class
            _fugacityClass = FugacityClass([self.thermoPropData], [
                                           self.symbol], _eosResSet, params, phase)

            # select method
            selectFugacity = {
                "PR": lambda: _fugacityClass.FugacityPR(),
                "VW": 1,
                "RKS": 1
            }

            # res
            _fugacityRes = selectFugacity.get(eos_model)()

            # return
            return _fugacityRes

        except Exception as e:
            raise Exception("fugacity failed!")
