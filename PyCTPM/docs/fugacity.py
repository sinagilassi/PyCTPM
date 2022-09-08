# FUGACITY CALCULATION FOR GAS/LIQUID/SOLID PHASE
# ------------------------------------------------

# import packages/modules
import numpy as np
import math
# local
from PyCTPM.core import Tref, R_CONST
from PyCTPM.docs.dThermo import RackettEquation


class FugacityClass:
    '''
    # Fugacity calculation in gas, liquid, and solid phases using an EOS

    for a liquid phase, the Poynting correction factor is used 
    '''

    def __init__(self, compData, components, eosRes, params, phase='gas'):
        self.compData = compData
        self.components = components
        self.eosRes = eosRes
        self.phase = phase
        self.P = params.get("pressure", 0)
        self.T = params.get("temperature", 0)
        # set
        self.Z = eosRes.get("Z")
        self.T_Tc_Ratio = eosRes.get("T_Tc_ratio")
        self.componentsNo = len(self.components)

    def FugacityPR(self):
        '''
        set fugacity equation based on a phase (gas/liquid/solid)
        '''
        try:
            # phase equation selection
            phaseEqSelection = {
                'gas': lambda: self._gasFugacityPR(),
                'liquid': lambda: self._liquidFugacityPR()
            }

            # set
            res = phaseEqSelection.get(self.phase)()

            # res
            return res
        except Exception as e:
            raise Exception("PR fugacity failed!")

    def _eqPR(self, Z):
        '''
        calculate PR fugacity coefficient

        args:
            Z: compressibility coefficient
        '''
        try:
            # set
            eosParams = self.eosRes.get("eos-params", 0)
            # A/B
            A = eosParams.get("A")
            B = eosParams.get("B")

            # fugacity coefficient
            phi0 = (Z-1) - np.log(Z-B) - (A/(2*B*np.sqrt(2))) * \
                np.log((Z+(1+np.sqrt(2))*B)/(Z+(1-np.sqrt(2))*B))
            phi = np.exp(phi0)

            # res
            return phi
        except Exception as e:
            raise Exception("PR fugacity failed! ", e)

    def _gasFugacityPR(self):
        '''
        estimation of gas fugacity using a EOS

        return:
            fugacity
            fugacity coefficient
        '''
        try:
            # Z (the highest value)
            Z = self.Z  # np.amax(self.Z)

            # calculate fugacity coefficient
            _fugCoefficient = self._eqPR(Z)
            # fugacity
            fugacity = _fugCoefficient*self.P

            # return
            return fugacity, _fugCoefficient, self.T_Tc_Ratio

        except Exception as e:
            raise Exception("Gas fugacity failed!, ", e)

    def _liquidFugacityPR(self, mode=True, vapor_pressure=1):
        '''
        estimation of liquid fugacity using a EOS

        liquid fugacity is then estimated using a saturated fugacity while

            fugacity[V] = fugacity[L] = fugacity[sat]

            fugacity[V] is calculated with a pure species vapor pressure which is substituted to the given pressure and temperature

            thus:
                fugacity[V,sat] = eos(P,T) while P=P* and Z is the highest

                fugacity[sat] = fugacity-coefficient[sat] x vapor-pressure[sat] = phi* x P*

                fugacity[L] = fugacity[sat] x exp(molar-volume[L] x (P-P*)/RT)

                as liquids are fairly incompressible for Tr<0.9, the molar-volume is assumed to be constant

        args:
            mode: Poynting equation is chosen (default=True)
            vapor_pressure: vapor pressure at which saturated fugacity is calculated for Poynting equation
        '''
        try:
            # check mode
            # -> use poynting equation to modify fugacity
            if mode is True:
                # Z (the highest value)
                Z = np.amax(self.Z)
            else:
                # Z (the lowest value)
                Z = np.amin(self.Z)

            # calculate fugacity coefficient
            _fugCoefficient = self._eqPR(Z)
            # fugacity
            fugacity = _fugCoefficient*self.P

            # check mode
            if mode is True:
                # critical molar-volume [m^3/mol]
                Vc = self.calCriticalMolarVolume()

                # saturated molar-volume [m^3/mol]
                # -> Rackett equation
                Vsat = self.calSaturatedLiquidVolume(Vc)

                # saturated fugacity
                fugacitySat = _fugCoefficient*vapor_pressure
                fugacity = fugacitySat * \
                    np.exp(Vsat*(self.P - vapor_pressure)/(R_CONST*self.T))

            # return
            return fugacity
        except Exception as e:
            raise Exception("Gas fugacity failed!, ", e)

    def calCriticalMolarVolume(self):
        '''
        estimate critical molar-volume [m^3/mol]
        '''
        try:
            # component data
            componentsData = self.compData

            # sorted data
            # Pc [bar], Tc [K], w [-]
            # ! Pc [bar] => [Pa]
            componentsDataSorted = [
                [float(item['Pc'])*1e5, float(item['Tc']), float(item['Zc'])] for item in componentsData]

            # critical molar-volume [m^3/mol]
            Vc = np.zeros(self.componentsNo)

            count = 0
            for item in componentsDataSorted:
                # Pc,Tc,Zc
                # item[0], item[1], item[2]
                Vc[count] = item[2] * ((R_CONST * item[1]) / item[0])
                count += 1

            # res
            return Vc

        except Exception as e:
            raise Exception("critical molar-volume failed!")

    def calSaturatedLiquidVolume(self, Vc):
        '''
        estimate saturated liquid volume using the Rackett equation
        '''
        try:
            # component data
            componentsData = self.compData

            # sorted data
            # Pc [bar], Tc [K], w [-]
            # ! Pc [bar] => [Pa]
            componentsDataSorted = [
                [float(item['Pc'])*1e5, float(item['Tc']), float(item['Zc'])] for item in componentsData]

            # saturated molar-volume [m^3/mol]
            Vsat = np.zeros(self.componentsNo)

            i = 0
            for item in componentsDataSorted:
                # Pc,Tc,Zc
                # item[0], item[1], item[2]
                # Tr
                _Tr = item[1]/self.T
                # saturated molar-volume
                Vsat[i] = RackettEquation(Vc[i], item[2], _Tr)
                i += 1

            # res
            return Vsat

        except Exception as e:
            raise Exception("saturated liquid volume failed!")
