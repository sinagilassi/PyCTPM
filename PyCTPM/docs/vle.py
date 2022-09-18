# VAPOR-LIQUID EQUILIBRIUM (VLE) CALCULATIONS
# --------------------------------------------

# packages/modules
import numpy as np
from scipy import optimize


class VLEClass:
    '''
    vapor-liquid equilibrium calculation
    '''

    def __init__(self, pool):
        self.pool = pool
        # set
        self.compNo = len(pool)

    def bubblePressure(self, params, config):
        '''
        bubble pressure calculation

        knowns:
            1. T
            2. z[i] = x[i]

        unknowns:
            1. P
            2. y[i]    

        solutions:
            1. cal P[i,sat] at T
            2. cal bubble pressure 
            3. cal y[i]
        '''
        try:
            # params
            T, zis = params

            # config
            VaPeCal = config['VaPeCal']

            # compo no
            compNo = zis.size

            # vapor pressure [Pa]
            VaPe = np.zeros(compNo)
            for i in range(compNo):
                # REVIEW
                VaPe[i] = self.pool[i].vapor_pressure(T, mode=VaPeCal)

            # bubble pressure [Pa]
            BuPr = np.multiply(zis, VaPe)

            # vapor mole fraction
            yis = np.zeros(compNo)
            for i in range(compNo):
                yis[i] = zis[i]*VaPe[i]/BuPr

            # res
            return yis, BuPr
        except Exception as e:
            raise Exception(e)

    def dewPressure(self, params, config):
        '''
        dew pressure calculation

        knowns:
            1. T
            2. z[i] = y[i]

        unknowns:
            1. P
            2. x[i]    

        solutions:
            1. cal P[i,sat] at T
            2. cal bubble pressure 
            3. cal x[i]
        '''
        try:
            # params
            T, zis = params

            # config
            VaPeCal = config['VaPeCal']

            # compo no
            compNo = zis.size

            # vapor pressure [Pa]
            VaPe = np.zeros(compNo)
            for i in range(compNo):
                # REVIEW
                VaPe[i] = 1

            # dew pressure [Pa]
            DePr = 1/np.multiply(zis, 1/VaPe)

            # liquid mole fraction
            xis = np.zeros(compNo)
            for i in range(compNo):
                xis[i] = zis[i]*DePr/VaPe[i]

            # res
            return xis, DePr
        except Exception as e:
            raise Exception(e)

    def bubbleTemperature(self, params, config):
        '''
        bubble temperature calculation

        args:
            params:
                1. feed mole fraction *** array *** (zi=xi)
                2. system pressure [Pa]
            config:
                1. Tg0: initial guess temperature
                2. VaPeCal: vapor-pressure calculation method (default: antoine)

        knowns:
            1. P
            2. z[i] = x[i]

        unknowns:
            1. T
            2. y[i]    

        solutions:
            1. guess Tg
            2. cal P[i,sat] at Tg
            3. cal bubble pressure Pb at Tg
            4. check Pb equals P
            4. cal y[i]
        '''
        try:
            # params
            zi = params.get('zi', [])
            P = params.get('P', 0)

            # config
            VaPeCal = config.get('VaPeCal', 'antoine')
            Tg0 = config.get('Tg0', 295)

            # params
            _params = (self.compNo, zi, P, VaPeCal)
            # bubble pressure [Pa]
            _res0 = optimize.fsolve(self.btFunction, Tg0, args=(_params,))
            # ->
            # REVIEW
            Tg = _res0[0]

            # vapor pressure [Pa]
            # at T (Tg)
            VaPe = np.zeros(self.compNo)
            for i in range(self.compNo):
                # REVIEW
                VaPe[i] = self.pool[i].vapor_pressure(Tg, VaPeCal)

            # vapor mole fraction
            yis = np.zeros(self.compNo)
            for i in range(self.compNo):
                yis[i] = zi[i]*VaPe[i]/P

            # res
            return Tg, yis, VaPe
        except Exception as e:
            raise Exception(e)

    def btFunction(self, x, params):
        '''
        args:
            x: guess temperature *** array *** [K]
        '''
        # Tg
        Tg = x[0]
        # params
        compNo, zi, P, VaPeCal = params
        # calculate vapor-pressure

        # vapor pressure [Pa]
        VaPe = np.zeros(compNo)
        for i in range(compNo):
            # REVIEW
            VaPe[i] = self.pool[i].vapor_pressure(Tg, VaPeCal)

        # bubble pressure [Pa]
        BuPr = np.dot(zi, VaPe)

        # loss
        loss = abs((P/BuPr) - 1)

        return loss

    def dewTemperature(self, params, config):
        '''
        dew temperature calculation

        args:
            params:
                1. feed mole fraction *** array *** (zi=xi)
                2. system pressure [Pa]
            config:
                1. Tg0: initial guess temperature
                2. VaPeCal: vapor-pressure calculation method (default: antoine)

        knowns:
            1. P
            2. z[i] = y[i]

        unknowns:
            1. T (dew temperature)
            2. y[i]    

        solutions:
            1. guess Tg
            2. cal P[i,sat] at Tg
            3. cal bubble pressure Pb at Tg
            4. check Pb equals P
            4. cal x[i]
        '''
        try:
            # params
            zi = params.get('zi', [])
            P = params.get('P', 0)

            # config
            VaPeCal = config.get('VaPeCal', 'antoine')
            Tg0 = config.get('Tg0', 295)

            # params
            _params = (self.compNo, zi, P, VaPeCal)
            # bubble pressure [Pa]
            _res0 = optimize.fsolve(self.dtFunction, Tg0, args=(_params,))
            # ->
            # REVIEW
            Tg = _res0[0]

            # vapor pressure [Pa]
            # at T (Tg)
            VaPe = np.zeros(self.compNo)
            for i in range(self.compNo):
                # REVIEW
                VaPe[i] = self.pool[i].vapor_pressure(Tg, VaPeCal)

            # vapor mole fraction
            xi = np.zeros(self.compNo)
            for i in range(self.compNo):
                xi[i] = zi[i]*P/VaPe[i]

            # res
            return Tg, xi, VaPe
        except Exception as e:
            raise Exception(e)

    def dtFunction(self, Tg, params):
        '''
        args:
            Tg: guess temperature [K]
        '''
        # params
        compNo, zi, P, VaPeCal = params
        # calculate vapor-pressure

        # vapor pressure [Pa]
        VaPe = np.zeros(compNo)
        for i in range(compNo):
            # REVIEW
            VaPe[i] = self.pool[i].vapor_pressure(Tg, VaPeCal)

        # dew pressure [Pa]
        DePr = np.dot(zi, VaPe)

        # loss
        loss = abs((P/DePr) - 1)

        return loss

    def vaporPressureMixture(self, T, mode):
        '''
        calculate mixture vapor-pressure
        '''
        # vapor pressure [Pa]
        VaPe = np.zeros(self.compNo)
        for i in range(self.compNo):
            # REVIEW
            VaPe[i] = self.pool[i].vapor_pressure(T, mode)

        # res
        return VaPe

    def calBubblePressure(self, xi, VaPe):
        '''
        calculate bubble pressure

        args:
            xi: liquid mole fraction
            VaPe: vapor-pressure [Pa]
        '''
        # bubble pressure
        BuPr = np.dot(xi, VaPe)

        # res
        return BuPr

    def calDewPressure(self, yi, VaPe):
        '''
        calculate dew pressure
        '''
        # dew-point pressure
        DePr = 1/np.dot(yi, 1/VaPe)

        # res
        return DePr

    def flashIsothermal(self, params, config):
        '''
        isothermal flash calculation

        knowns:
            1. zi
            2. P
            3. T

        unknowns:
            1. xi
            2. yi
            3. V
            4. L
        '''
        try:
            # params
            zi = params.get('zi', [])
            P = params.get('P', 0)
            T = params.get('T', 0)

            # config
            VaPeCal = config.get('VaPeCal', 'antoine')
            V_F_ratio_g0 = config.get('guess_V_F_ratio', 0.5)

            # vapor-pressure
            VaPri = self.vaporPressureMixture(T)

            # ki ratio (Raoult's law)
            ki = VaPri/P

        except Exception as e:
            raise Exception("flash isothermal failed!")
