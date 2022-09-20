# POOL
# -----

# packages/modules
import numpy as np
# local
from PyCTPM.docs.vle import VLEClass
from PyCTPM.results import Display
from PyCTPM.core import roundNum


class Pool(VLEClass, Display):
    '''
    define a multi-component system 
    '''

    def __init__(self, componentList):
        self.componentList = componentList
        self.compNo = len(componentList)
        #
        VLEClass.__init__(self, componentList)
        Display.__init__(self)

    @property
    def component_list(self):
        return self.componentList

    def bubble_pressure(self, mole_fractions, temperature, vapor_pressure_method='antoine', activity_coefficient_config=[]):
        '''
        bubble pressure calculation

        args:
            mole_fraction: feed mole fraction (zi=xi)
            temperature: flash temperature [K]
            vapor_pressure_method: vapor-pressure method (default: antoine)
            activity_coefficient_config: 
                1. model name 
                    a) Margules equation
                2. model parameters
        '''
        # params
        params = {
            "zi": np.array(mole_fractions),
            "T": temperature
        }

        # config
        config = {
            "VaPeCal": vapor_pressure_method
        }

        # cal
        yi, BuPr, VaPe, Ki = self.bubblePressure(params, config)

        # res
        return yi, BuPr, VaPe, Ki

    def dew_pressure(self):
        pass

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

    def flash_isothermal(self, mole_fractions, flash_pressure, flash_temperature, guess_V_F_ratio=0.5, vapor_pressure_method='antoine', model="raoult"):
        '''
        isothermal flash calculation

        args:
            mole_fractions: feed mole fraction [-]
            flash_pressure: flash pressure [Pa]
            flash_temperature: flash temperature [K] - isothermal condition T[in]=T[out]
            guess_V_F_ratio: 
            vapor_pressure_method: 
            model: "raoult"

        notes:
            flash case: P[bubble]>P[flash]>P[dew]
            cases:
                1. P[bubble]<P[flash] results in the liquid phase feed
                2. P[dew]>P[flash] results in the vapor phase feed
        '''
        # vapor pressure at inlet temperature
        VaPe = self.vaporPressureMixture(
            flash_temperature, vapor_pressure_method)

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
            "P_flash": flash_pressure,
            "T_flash": flash_temperature,
            "VaPe": VaPe
        }

        # config
        config = {
            "guess_V_F_ratio": guess_V_F_ratio,
            "VaPeCal": vapor_pressure_method,
            "model": model
        }

        # flash calculation
        V_F_ratio, L_F_ratio, xi, yi = self.flashIsothermal(params, config)

        # NOTE
        # ! display results
        # vapor pressure
        _display = []

        # header
        _display.append(['Parameter', 'Value', 'Unit'])

        for i in range(self.compNo):
            _display.append(
                [self.componentList[i].symbol+' vapor-pressure [P*]', roundNum(VaPe[i], 3), 'Pa'])

        for i in range(self.compNo):
            _display.append([self.componentList[i].symbol +
                            ' liquid mole fraction [x]', roundNum(xi[i], 4), '-'])

        for i in range(self.compNo):
            _display.append([self.componentList[i].symbol +
                            ' vapor mole fraction [y]', roundNum(yi[i], 4), '-'])

        #
        _display.extend(
            [['bubble pressure', roundNum(BuPr, 2), 'Pa'],
             ['dew pressure', roundNum(DePr, 2), 'Pa'],
             ['feed flowrate', 1, 'mol/s'],
             ['liquid flowrate', roundNum(L_F_ratio, 3), 'mol/s'],
             ['vapor flowrate', roundNum(V_F_ratio, 3), 'mol/s']]
        )

        # log
        self.colDisplay(_display)

        # res
        return flashState, BuPr, DePr, VaPe, V_F_ratio, L_F_ratio, xi, yi
