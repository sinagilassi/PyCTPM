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
            zi = params.get('zi', [])
            T = params.get('T', 0)

            # config
            VaPeCal = config['VaPeCal']

            # vapor pressure [Pa]
            VaPe = np.zeros(self.compNo)
            for i in range(self.compNo):
                # REVIEW
                VaPe[i] = self.pool[i].vapor_pressure(T, mode=VaPeCal)

            # bubble pressure [Pa]
            BuPr = np.multiply(zi, VaPe)

            # vapor mole fraction
            yi = np.zeros(self.compNo)
            for i in range(self.compNo):
                yi[i] = zi[i]*VaPe[i]/BuPr

            # Ki ratio
            Ki = np.multiply(yi, 1/zi)

            # res
            return yi, BuPr, VaPe, Ki
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
            # bubble temperature [K]
            _res0 = optimize.fsolve(self.btFunction, Tg0, args=(_params,))
            # ->
            # REVIEW
            T = _res0[0]

            # vapor pressure [Pa]
            # at T (Tg)
            VaPe = np.zeros(self.compNo)
            for i in range(self.compNo):
                # REVIEW
                VaPe[i] = self.pool[i].vapor_pressure(T, VaPeCal)

            # vapor mole fraction
            yi = np.zeros(self.compNo)
            for i in range(self.compNo):
                yi[i] = zi[i]*VaPe[i]/P

            _res = {
                "T": T,
                "yi": yi,
                'xi': zi,
                "VaPe": VaPe
            }

            # res
            return _res
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
            P_flash = params.get('P_flash', 0)
            T_flash = params.get('T_flash', 0)
            VaPri = params.get('VaPe', [])

            # config
            VaPeCal = config.get('VaPeCal', 'antoine')
            V_F_ratio_g0 = config.get('guess_V_F_ratio', 0.5)

            # ki ratio (Raoult's law)
            Ki = VaPri/P_flash

            # params
            _params = (self.compNo, zi, Ki)
            # V/F
            _res0 = optimize.fsolve(
                self.fitFunction, V_F_ratio_g0, args=(_params,))
            # ->
            V_F_ratio = _res0[0]

            # liquid/vapor mole fraction
            xi, yi = self.xyFlash(self.compNo, V_F_ratio, zi, Ki)

            # L/F
            L_F_ratio = 1 - V_F_ratio

            # res
            return V_F_ratio, L_F_ratio, xi, yi

        except Exception as e:
            raise Exception("flash isothermal failed!")

    def fitFunction(self, x, params):
        '''
        flash isothermal function

        args:
            x: V/F guess
            params: 
                zi: feed mole fraction
                Ki: K ratio
        '''
        # V/F
        V_F_ratio = x[0]

        # params
        compNo, zi, Ki = params

        fi = np.zeros(compNo)
        for i in range(compNo):
            fi[i] = (zi[i]*(1-Ki[i]))/(1+(V_F_ratio)*(Ki[i]-1))

        f = np.sum(fi)

        return f

    def xyFlash(self, compNo, V_F_ratio, zi, Ki):
        '''
        calculate liquid/vapor mole fraction
        '''
        xi = np.zeros(compNo)
        yi = np.zeros(compNo)

        for i in range(compNo):
            xi[i] = (zi[i])/(1+(V_F_ratio)*(Ki[i]-1))
            yi[i] = Ki[i]*xi[i]

        # res
        return xi, yi

    def flashIsothermalV2(self, params, config):
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
            F = params.get('F', 0)
            zi = params.get('zi', [])
            P_flash = params.get('P_flash', 0)
            T_flash = params.get('T_flash', 0)
            VaPri = params.get('VaPe', [])

            # config
            VaPeCal = config.get('VaPeCal', 'antoine')

            # ki ratio (Raoult's law)
            Ki = VaPri/P_flash

            # unknown no
            unknownNo = self.compNo + 2

            # initial guess
            L0 = 0.001
            V0 = 0.001
            xi0 = np.zeros(self.compNo)
            for i in range(self.compNo):
                xi0[i] = 0.01
            # set
            _var0 = [L0, V0, *xi0]

            # bounds
            bU = []
            bL = []
            bounds = []
            # lower
            for i in range(unknownNo):
                _bl = 0
                bL.append(_bl)

            # upper
            for i in range(unknownNo):
                _bu = 0.99
                bU.append(_bu)

            bounds = [bL, bU]

            # params
            _params = (self.compNo, zi, F, Ki)
            # a system of non-linear equation
            # _res0 = optimize.fsolve(
            #     self.fitSystemFunction, _var0, args=(_params,))

            _res0 = optimize.least_squares(
                self.fitSystemFunction, _var0, args=(_params,), bounds=bounds)

            # ! check
            if _res0.success is False:
                raise Exception('root not found!')

            # sol
            x = _res0.x
            # ->
            L_sol = x[0]
            V_sol = x[1]
            V_F_ratio = V_sol/F

            # liquid/vapor mole fraction
            xi, yi = self.xyFlash(self.compNo, V_F_ratio, zi, Ki)

            # L/F
            L_F_ratio = 1 - V_F_ratio

            # res
            return V_F_ratio, L_F_ratio, xi, yi

        except Exception as e:
            raise Exception("flash isothermal failed!")

    def fitSystemFunction(self, x, params):
        '''
        flash isothermal function (nonlinear equations)

        unknowns:
            1. L
            2. V
            3. x[i]

        args:
            x: 
                1. L
                2. V
                3. x[i]
            params: 
                compNo: component number
                zi: feed mole fraction
                F: feed flowrate

        '''
        # params
        compNo, zi, F, Ki = params

        # xi
        xi = np.zeros(compNo)

        # set x
        L = x[0]
        V = x[1]
        for i in range(compNo):
            xi[i] = x[i+2]

        # system of nonlinear equations (NLE)
        fi = np.zeros(compNo+2)
        # overall mole balance
        fi[0] = F - (L + V)
        # component mole balance (without reaction)
        for i in range(compNo):
            # solve the second NLE
            fi[i+1] = F*zi[i] - (L*xi[i] + V*xi[i]*Ki[i])
        # constraint
        fi[-1] = np.sum(xi) - 1

        return fi
