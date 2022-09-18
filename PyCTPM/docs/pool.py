# POOL
# -----

# packages/modules
import numpy as np
# local
from PyCTPM.docs.vle import VLEClass


class Pool(VLEClass):
    '''
    define a multi-component system 
    '''

    def __init__(self, componentList):
        self.componentList = componentList
        #
        VLEClass.__init__(self, componentList)

    @property
    def component_list(self):
        return self.componentList

    def bubble_temperature(self, mole_fractions, pressure, guess_temperature=350, vapor_pressure_method='antoine'):
        '''
        bubble temperature calculation

        args:
            mole_fraction: feed mole fraction (zi=xi)
            pressure: system pressure [Pa]
        '''
        # params
        params = {
            "zi": np.array(mole_fractions),
            "P": pressure
        }

        # config
        config = {
            "Tg0": guess_temperature,
            "VaPeCal": vapor_pressure_method
        }

        # cal
        _res = self.bubbleTemperature(params, config)

        # res
        return _res

    def dew_temperature(self, mole_fractions, pressure, guess_temperature=350, vapor_pressure_method='antoine'):
        '''
        bubble temperature calculation

        args:
            mole_fraction: feed mole fraction (zi=xi)
            pressure: system pressure [Pa]
        '''
        # params
        params = {
            "zi": np.array(mole_fractions),
            "P": pressure
        }

        # config
        config = {
            "Tg0": guess_temperature,
            "VaPeCal": vapor_pressure_method
        }

        # cal
        _res = self.dewTemperature(params, config)

        # res
        return _res

    def flash_isothermal(self, mole_fractions, pressure_in, temperature_in, flash_pressure, guess_V_F_ratio=0.5, vapor_pressure_method='antoine'):
        '''
        isothermal flash calculation

        args:

        notes:
            flash case: P[bubble]>P[flash]>P[dew]
            cases:
                1. P[bubble]<P[flash] results in the liquid phase feed
                2. P[dew]>P[flash] results in the vapor phase feed
        '''
        # vapor pressure at inlet temperature
        VaPe = self.vaporPressureMixture(temperature_in, vapor_pressure_method)

        # bubble pressure [Pa]
        BuPr = self.calBubblePressure(mole_fractions, VaPe)

        # dew pressure
        DePr = self.calDewPressure(mole_fractions, VaPe)

        # check flash
        flashState = False
        if BuPr > flash_pressure and flash_pressure > DePr:
            # two phase exists
            flashState = True
        else:
            # one phase exist (liquid)
            flashState = False

        # params
        params = {
            "zi": np.array(mole_fractions),
            "P": flash_pressure,
            "T": temperature_in
        }

        # config
        config = {
            "guess_V_F_ratio": guess_V_F_ratio,
            "VaPeCal": vapor_pressure_method
        }

        # flash calculation

        # res
        return flashState, BuPr, DePr, VaPe
