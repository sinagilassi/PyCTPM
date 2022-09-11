# EQUILIBRIUM CLASS
# -------------------

# packages/modules
import numpy as np
from PyCTPM.docs.eosCore import eosCoreClass
from PyCTPM.docs.fugacity import FugacityClass
from PyCTPM.docs.dThermo import calMolarVolume, calVapourPressure


class EquilibriumClass:
    '''
    class list: 
        1. eos
        2. fugacity
    '''

    def __init__(self, compData, components):
        self.compData = compData
        self.components = components

        # set
        self.id = components['id']
        self.state = components['state']
        self.symbol = components['symbol']

        # data
        # -> thermo
        self.__thermoPropData = compData['thermo']
        # -> vapor-pressure
        self.__vaporPressureData = compData['vapor-pressure']

        self.componentsNo = len(self.id)

    def __database_set(self, id):
        '''
        select database
        '''
        try:
            _databaseSelect = self.compData.get(id, [])
            # check
            if len(_databaseSelect) == 0:
                raise Exception(f"database {id} not exist")
            else:
                return _databaseSelect
        except print(0):
            pass
        return

    def vaporPressure(self, T, mode):
        '''
        calculate vapor pressure at T using:
            1. Antoine equation (eq1)
            2. eos

        return:
            _Vp: vapor-pressure [Pa]
        '''
        try:
            # comp symbol
            _symbol = [self.symbol] if not isinstance(
                self.symbol, list) else self.symbol

            # check
            if mode == 1:
                _Vp = calVapourPressure(
                    _symbol, T, self.__vaporPressureData)
            elif mode == 2:
                _Vp = 0

            # res
            return _Vp
        except Exception as e:
            raise Exception("vapor-pressure calculation failed!, ", e)

    def vaporPressureEOS(self):
        '''
        find vapor-pressure of a fluid using eos
        '''
        try:
            print(0)
        except Exception as e:
            raise Exception("vapor-pressure estimation by eos failed!, ", e)

    def vpEOS(p):
        '''
        f(x) = 0
        '''
        try:
            print(0)
        except Exception as e:
            raise Exception("vapor-pressure function failed!, ", e)

    def compressibilityFactor(self, P, T, eos_model):
        '''
        find the roots of Z=f(P,T)

        args:
            P: pressure [Pa]
            T: temperature [K]
            eos_model: name of eos model
                1. van der Waals (VW)
                2. Redlich-Kwong and Soave (RKS)
                3. Peng-Robinson (PR)

        return:
            Z: compressibility coefficient [-]
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
                [self.__thermoPropData], [self.symbol], eos_model, [1], params)

            # * select method
            selectEOS = {
                "PR": lambda: _eosCoreClass._eosPR(),
                "VW": 1,
                "RKS": 1
            }

            return selectEOS.get(eos_model)()
        except Exception as e:
            raise Exception("compressibility factor failed!")

    def molarVolume(self, P, T, eos_model):
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
            Z: compressibility coefficient [-]
            eos-params: a,b,A,B,alpha,beta,gamma
        '''
        try:
            # eos
            eosRes = self.compressibilityFactor(P, T, eos_model)
            # ->
            Zs = eosRes['Zs']

            # check Zs
            if self.state == 'g':
                Z = np.amax(Zs)
            elif self.state == 'l':
                Z = np.amin(Zs)

            # res
            res = calMolarVolume(P, T, Z)

            return res, eosRes

        except Exception as e:
            raise Exception("molar-volume failed! ", e)

    def fugacities(self, P, T, phase, eos_model, pressure_correction):
        '''
        estimate fugacity at specified pressure and temperature

        args:
            P: pressure [Pa]
            T: temperature [K]
            eos_model: name of eos model
                1. van der Waals (VW)
                2. Redlich-Kwong and Soave (RKS)
                3. Peng-Robinson (PR)
            pressure_correction: estimate liquid/solid fugacity with:
                1. equation of state 
                2. the Poynting equation (default)

        return:
            f: fugacity [Pa]
            phi: fugacity coefficient [-]
        '''
        try:
            # T/Tc ratio
            T_Tc_ratio = T/float(self.__thermoPropData['Tc'])
            # P/Pc ratio
            P_Pc_ratio = P/float(self.__thermoPropData['Pc'])

            # eos params
            params = {
                "pressure": P,
                "temperature": T,
                "pressure_correction": pressure_correction,
                "T_Tc_ratio": T_Tc_ratio,
                "P_Pc_ratio": P_Pc_ratio
            }

            # ! check
            if phase == 'liquid' and pressure_correction == True:
                # REVIEW
                # vapor-pressure [Pa]
                _vaporPressure = self.vaporPressure(T, mode=1)

                # eos calculation
                _eosRes = self.molar_volume(_vaporPressure, T, eos_model)

                _eosResSet = {
                    "molar-volumes": _eosRes[0],
                    "eos-res": _eosRes[1],
                    'vapor-pressure': _vaporPressure
                }

                # * init fugacity class
                _fugacityClass = FugacityClass([self.__thermoPropData], [
                    self.symbol], _eosResSet, params)

                # res
                _fugacityRes = _fugacityClass.liquidFugacity()

            else:
                # eos calculation
                _eosRes = self.molar_volume(P, T, eos_model)

                _eosResSet = {
                    "molar-volumes": _eosRes[0],
                    "eos-res": _eosRes[1],
                }

                # * init fugacity class
                _fugacityClass = FugacityClass([self.__thermoPropData], [
                    self.symbol], _eosResSet, params)

                # select method
                selectFugacity = {
                    "PR": _fugacityClass.FugacityPR,
                    "VW": 1,
                    "RKS": 1
                }

                # res
                _fugacityRes = selectFugacity.get(eos_model)(phase)

            # return
            return _fugacityRes

        except Exception as e:
            raise Exception("fugacity failed!, ", e)
