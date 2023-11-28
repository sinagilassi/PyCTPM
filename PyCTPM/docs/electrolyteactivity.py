# ELECTROLYTE ACTIVITY
# ----------------------

# packages/modules
from math import pi, sqrt, pow, log, exp
import numpy as np


class ElectrolyteActivityClass:

    def __init__(self):
        pass

    def Debye_Huckel_model_activity_coefficient(self, params):
        '''
        the Debye-Huckel limiting law:
        the long range and strength of Coulombic interaction between ions is considered to be primarily \ 
        responsible for the departure from ideality in ionic solutions

        args:
            MoIoSt: molal ionic strength
            zi: ion charge *** list ***
            SoDe: solvent density [g/cm^3]
            T: temperature [K]
            er: dielectric constant [-]

        return:
            AcCoIon: activity coefficient of ions [molal], [mole-fraction] base
        '''
        try:
            # params
            MoIoSt, zi, SoDe, T, er = params

            # density conversion [kg/m^3] -> [g/cm^3]
            SoDe = SoDe*1e-3
            # A Gamma [(kg/mol)^0.5]
            A_Gamma = 1.8249e6*(sqrt(SoDe))/(pow(er*T, 1.5))

            # beta

            # charge effect
            _c0 = abs(np.array(zi).prod())
            # activity coefficient of ions
            _c1 = -1*A_Gamma*_c0*sqrt(MoIoSt)
            AcCoIon = pow(10, _c1)

            # mole fraction base
            AcCoIon_mf = AcCoIon*(1 + 1)
            # return
            return AcCoIon
        except Exception as e:
            raise Exception("DH model failed!, ", e)

    def Debye_Huckel_extended_model_activity_coefficient(self, params):
        '''
        the extended Debye-Huckel model:
        the long range and strength of Coulombic interaction between ions is considered to be primarily \ 
        responsible for the departure from ideality in ionic solutions

        args:
            params:
                MoIoSt: molal ionic strength
                zi: ion charge *** list ***
                SoDe: solvent density [g/cm^3]
                T: temperature [K]
                er: dielectric constant [-]

        return:
            AcCoIon
        '''
        try:
            # params
            MoIoSt, zi, SoDe, T, er = params

            # density conversion [kg/m^3] -> [g/cm^3]
            SoDe = SoDe*1e-3

            # Avogadro number [1/mol]
            Nav = 6.023e23
            # electronic charge [C]
            e = 1.60206e-19
            # Boltzmann constant [J/K]
            kb = 1.380649e-23

            # A [(kg/mol)^0.5]
            A = sqrt(2*pi*Nav*SoDe)*(e**2/(4*pi*er*kb*T))

            # B
            B = e*((2*Nav*SoDe)/(er*kb*T))

            AcCoIon = 1

            # return
            return AcCoIon
        except Exception as e:
            raise Exception("DH model failed!, ", e)

    def Debye_Huckel_parameters(self, params):
        '''
        Debye-Huckel parameters

        args:
            params:
                MoIoSt: molal ionic strength
                zi: ion charge *** list ***
                SoDe: solvent density [g/cm^3]
                T: temperature [K]
                er: dielectric constant [-]
        '''
        # params
        MoIoSt, zi, SoDe, T, er = params

        # density conversion [kg/m^3] -> [g/cm^3]
        SoDe = SoDe*1e-3

        # A Gamma [(kg/mol)^0.5]
        A_Gamma = 1.8249e6*(sqrt(SoDe))/(pow(er*T, 1.5))

        # res
        return A_Gamma

    def Pitzer_model_activity_coefficient(self, params):
        '''
        Pitzer model for *** single electrolyte ***

        adjustable parameters:
            1. beta0_ij
            2. beta1_ij
            3. beta2_ij
            4. C_ij

        args:
            params:
                MoIoSt: molal ionic strength
                zi: ion charge *** list ***
                SoDe: solvent density [g/cm^3]
                T: temperature [K]
                er: dielectric constant [-]
                SoMo: solvent molality [mol/kg]
                ReSt: reaction stoichiometric *** list ***
        '''
        try:
            # set vars
            MoIoSt, zi, SoDe, T, er, SoMo, ReSt, adj_params = params
            beta_0, beta_1, C_phi = adj_params

            # other parameters
            b = 1.2
            alpha = 2

            # Debye-Huckel parameters
            params_A_DH = MoIoSt, zi, SoDe, T, er
            A_DH = self.Debye_Huckel_parameters(params_A_DH)

            # f gamma
            f_gamma_0 = sqrt(MoIoSt)/(1+b*sqrt(MoIoSt))
            f_gamma_1 = (2/b)*log(1+b*sqrt(MoIoSt))
            f_gamma = -1*(1/3)*A_DH*(f_gamma_0 + f_gamma_1)

            # C gamma
            C_gamma = (3/2)*C_phi

            # B gamma
            _c0 = (2*beta_1)*(1/((alpha**2)*MoIoSt))
            _c1 = 1 + alpha*sqrt(MoIoSt) - 0.5*(alpha**2)*MoIoSt
            _c2 = exp(-1*alpha*sqrt(MoIoSt))

            B_gamma = 2*beta_0 + _c0*(1 - _c1*_c2)

            # charge effect
            _c3 = abs(np.array(zi).prod())

            # stoichiometric
            ReSt = np.array(ReSt)

            v = ReSt[0] + ReSt[1]

            _c4 = SoMo*(2*ReSt[0]*ReSt[1]/v)*B_gamma
            _c5 = (SoMo**2)*(2*pow(ReSt[0]*ReSt[1], 3/2)/v)*C_gamma

            # mean molal activity coefficient
            _c6 = _c3*f_gamma + _c4 + _c5
            MoAcCo = exp(_c6)

            #! water activity coefficient

            # f phi
            f_phi = -1*(1/3)*A_DH*(sqrt(MoIoSt)/(1+b*sqrt(MoIoSt)))

            # B phi
            B_phi = beta_0 + beta_1*_c2

            _c7 = SoMo*(2*ReSt[0]*ReSt[1]/v)*B_phi
            _c8 = (SoMo**2)*(2*pow(ReSt[0]*ReSt[1], 3/2)/v)*C_phi

            # osmotic coefficient
            OsCo = 1 + (_c3*f_phi + _c7 + _c8)

            # water molecular weight [kg/mol]
            WaMoWe = 18.01528*1e-3

            # water activity coefficient
            _WaAcCo0 = OsCo*WaMoWe*v*SoMo
            WaAcCo = exp(-1*_WaAcCo0)

            # res
            return MoAcCo, WaAcCo

        except Exception as e:
            raise Exception('Pitzer parameter estimation failed!', e)

    def ENRTL_activity_coefficient():
        '''

        '''
