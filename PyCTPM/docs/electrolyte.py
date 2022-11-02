# ELECTROLYTE
# ------------

# packages/modules
import numpy as np


class ElectrolytesClass:
    def __init__(self, ions, solvent):
        self.ions = ions
        self.solvent = solvent
        # ion no
        self.ionNo = len(ions)

    def ionsCharge(self):
        '''
        return a list of charge of ions
        '''
        ionCharge = np.zeros(self.ionNo)
        for i in range(self.ionNo):
            _ion = self.ions[i]
            ionCharge[i] = _ion.charge

        # res
        return ionCharge

    def calMolalIonicStrength(self, Moli):
        '''
        molal ionic strength

        args:
            Moli: molality of ions 
        '''
        try:
            # ion charge
            _ionChargei = self.ionsCharge()

            Ii = np.zeros(self.ionNo)
            for i in range(self.ionNo):
                Ii[i] = Moli[i]*(_ionChargei[i]**2)

            # res
            return 0.5*np.sum(Ii)
        except Exception as e:
            raise Exception('molal ionic strength failed!')

    def RelativePermittivity(self, em, e0):
        '''
        relative permittivity defined as a ratio of permittivity of the material and permittivity of vacuum

        k = er = em/e0

        k/er: dielectric constant

        args: 
            em: permittivity of the material
            e0: permittivity of vacuum (8.85419E-12 [C^2/N.m^2])
        '''
        return em/e0

    def WaterDielectric(self, T):
        '''
        calculate water dielectric according to a temperature

        args:
            T: temperature [K]
        '''
        # T conversion [C]
        T = T - 273.15

        # dielectric
        H2O_dielectric = 87.8-0.396*T+0.000745*(T**2)

        # res
        return H2O_dielectric

    def WaterDensity(self, T):
        '''
        calculate water density at a desired temperature while neglecting pressure effect


        args:
            T: temperature [K]

        return:
            rho: water density [kh/m^3]
        '''
        # parameter
        Ai = np.array([-13.418392, 0.6884103, -2.44970115e-3,
                      3.7060667e-6, -2.11062995e-9, -1.12273895e-13])

        AiT = np.zeros(6)
        for i in range(6):
            AiT[i] = Ai[i]*(T**i)

        rho = 18.015*np.sum(AiT)

        # res
        return rho
