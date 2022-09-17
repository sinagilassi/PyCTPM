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
