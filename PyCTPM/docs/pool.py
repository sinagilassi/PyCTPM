# POOL
# -----

# packages/modules
from typing import List
import numpy as np
from matplotlib import pyplot as plt
# local
from PyCTPM.docs.vle import VLEClass
from PyCTPM.results import Display
from PyCTPM.core import roundNum
from PyCTPM.results import Visual


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

    def bubble_pressure(self, mole_fractions, temperature, vapor_pressure_method='antoine', model='raoult', activity_coefficient_model='van-laar'):
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
            model: vle thermodynamic model
                1. raoult
                2. modified-raoult
        '''
        # params
        params = {
            "zi": np.array(mole_fractions),
            "T": temperature
        }

        # config
        config = {
            "VaPeCal": vapor_pressure_method,
            "model": model
        }

        # cal
        yi, BuPr, VaPe, Ki, AcCo = self.bubblePressure(params, config)

        # res
        return yi, BuPr, VaPe, Ki, AcCo

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

    def flash_isothermal(self, mole_fractions, flash_pressure, flash_temperature, feed_pressure, feed_flowrate=1, guess_V_F_ratio=0.5, vapor_pressure_method='antoine', model="raoult", activity_coefficient_model='van-laar'):
        '''
        isothermal flash calculation

        args:
            mole_fractions: feed mole fraction [-]
            flash_pressure: flash pressure [Pa]
            flash_temperature: flash temperature [K] - isothermal condition T[in]=T[out]
            feed_pressure: feed pressure to check the current state of the feed
            feed_flowrate: feed flowrate (mole basis) [mol/s]
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
        VaPr = self.vaporPressureMixture(
            flash_temperature, vapor_pressure_method)

        # bubble pressure [Pa]
        BuPr = self.calBubblePressure(mole_fractions, VaPr)

        # dew pressure
        DePr = self.calDewPressure(mole_fractions, VaPr)

        # check flash
        flashState = False
        if BuPr > flash_pressure and flash_pressure > DePr:
            # two phase exists
            flashState = True
        else:
            # one phase exist (liquid)
            flashState = False

        # check current state of the feed
        feedState = True
        if feed_pressure < BuPr:
            feedState = False

        # params
        params = {
            "F": feed_flowrate,
            "zi": np.array(mole_fractions),
            "P_flash": flash_pressure,
            "T_flash": flash_temperature,
            "VaPe": VaPr
        }

        # config
        config = {
            "guess_V_F_ratio": guess_V_F_ratio,
            "VaPeCal": vapor_pressure_method,
            "model": model
        }

        # flash calculation
        V_F_ratio, L_F_ratio, xi, yi = self.flashIsothermalV2(params, config)

        # NOTE
        # ! display results
        # vapor pressure
        _display = []

        # header
        _display.append(['Parameter', 'Value', 'Unit'])

        for i in range(self.compNo):
            _display.append(
                [self.componentList[i].symbol+' vapor-pressure [P*]', roundNum(VaPr[i], 3), 'Pa'])

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
        return flashState, BuPr, DePr, VaPr, V_F_ratio, L_F_ratio, xi, yi

    def Txy_binary(self, pressure, guess_temperature=350, vapor_pressure_method='antoine', model="raoult", zi_no=10):
        '''
        bubble temperature calculation

        args:
            mole_fraction: feed mole fraction (zi=xi)
            pressure: system pressure [Pa]
            guess_temperature: 
            vapor_pressure_method: vapor-pressure calculation method (default: antoine)
            model: thermodynamic model for equilibrium system (default: raoult)
            zi_no: number of mole fractions
        '''
        #  feed mole fraction
        x1 = np.linspace(0.001, 0.999, zi_no)
        x2 = 1 - x1
        #
        mole_fractions = np.array([x1, x2])

        # res
        _res = []

        for i in range(zi_no):
            # params
            params = {
                "zi": np.array(mole_fractions[:, i]),
                "P": pressure
            }

            # config
            config = {
                "Tg0": guess_temperature,
                "VaPeCal": vapor_pressure_method
            }

            # cal
            _btRes = self.bubbleTemperature(params, config)
            _res.append(_btRes)

        # Ts
        Ts = [item['T'] for item in _res]
        # xi
        xi = [item['xi'][0] for item in _res]
        # yi
        yi = [item['yi'][0] for item in _res]
        # set
        bubbleLine = [[xi], [Ts]]
        dewLine = [[yi], [Ts]]

        # ! plot setting
        # XYList = Visual.plots2DSetXYList(dataX, dataYs)
        # -> label
        # dataList = Visual.plots2DSetDataList(XYList, labelList)
        # Visual.plot2D(xi, Ts)
        # Visual.plot2D(yi, Ts)

        plt.plot(xi, Ts, 'r-', yi, Ts, 'b-')
        plt.show()

        # res
        return _res

    def Pxy_binary(self, temperature,  vapor_pressure_method='antoine', model="modified-raoult", zi_no=10):
        '''
        bubble temperature calculation

        args:
            mole_fraction: feed mole fraction (zi=xi)
            temperature: system (fixed) temperature [K]
            vapor_pressure_method: vapor-pressure calculation method (default: antoine)
            model: thermodynamic model for equilibrium system (default: raoult)
            zi_no: number of mole fractions
        '''
        #  feed mole fraction
        x1 = np.linspace(0.001, 0.999, zi_no)
        x2 = 1 - x1
        #
        mole_fractions = np.array([x1, x2])

        # res
        _res = []

        for i in range(zi_no):
            # params
            params = {
                "zi": np.array(mole_fractions[:, i]),
                "T": temperature
            }

            # config
            config = {
                "VaPeCal": vapor_pressure_method,
                "model": model
            }

            # ! check vle model
            # cal
            _btRes = self.bubblePressure(params, config)
            _res.append(_btRes)

        # pressure series (Ps)
        Ps = [item['P'] for item in _res]
        # xi
        xi = [item['xi'][0] for item in _res]
        # yi
        yi = [item['yi'][0] for item in _res]
        # set
        bubbleLine = [[xi], [Ps]]
        dewLine = [[yi], [Ps]]

        # ! plot setting
        # XYList = Visual.plots2DSetXYList(dataX, dataYs)
        # -> label
        # dataList = Visual.plots2DSetDataList(XYList, labelList)
        # Visual.plot2D(xi, Ts)
        # Visual.plot2D(yi, Ts)

        plt.plot(xi, Ps, 'r-', yi, Ps, 'b-')
        plt.show()

        # res
        return _res

    def Margules_1Parameter(self, liquid_mole_fraction, vapor_mole_fraction, pressure, temperature,  vapor_pressure_method='antoine'):
        '''
        find Margules 1-parameter based on experimental results for a binary system

        args:
            liquid_mole_fraction: liquid mole fraction as [x1,x2]
            vapor_mole_fraction: vapor mole fraction as [y1,y2]
            pressure: system pressure as P

        return:
            A12: Margules 1-parameter 
        '''
        try:
            # vapor pressure at inlet temperature
            VaPr = self.vaporPressureMixture(
                temperature, vapor_pressure_method)

            # calculate excess molar gibbs energy
            #! check
            if len(liquid_mole_fraction) == 1 and len(vapor_mole_fraction) == 1:
                # activity coefficient from experimental data
                AcCoExp = self.activityCoefficientUsingModifiedRaoult(
                    liquid_mole_fraction[0], vapor_mole_fraction[0], pressure[0], VaPr)

                # one algebraic equation (A(12)*x1*x2)
                ExMoGiEn = self.ExcessMolarGibbsFreeEnergy(
                    liquid_mole_fraction[0], AcCoExp)

                # A12 parameter
                A12 = ExMoGiEn / \
                    (liquid_mole_fraction[0][0]*liquid_mole_fraction[0][1])

                return A12
            else:
                # solve a system of non-linear equation
                pass

        except Exception as e:
            pass
