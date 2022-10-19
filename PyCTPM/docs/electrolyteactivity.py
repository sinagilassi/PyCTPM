# ELECTROLYTE ACTIVITY
# ----------------------

# packages/modules
import numpy as np


class ElectrolyteActivityClass:

    def __init__(self):
        pass

    @staticmethod
    def Debye_Huckel_model_activity_coefficient(MoIoSt, zi, SoDe, T, er):
        '''
        the Debye-Huckel limiting law:
        the long range and strength of Coulombic interaction between ions is considered to be primarily \ 
        responsible for the departure from ideality in ionic solutions

        args:
            MoIoSt: molal ionic strength
            zi: ion charge *** list ***
            SoDe: solvent density [g/cm^3]
            T: temperature [K]
            er: 


        '''
        try:
            print(0)
        except Exception as e:
            raise Exception("DH model failed!, ", e)

    def Pitzer_model_activity_coefficient(self):
        pass

    @staticmethod
    def Pitzer_model_activity_coefficient_parameter_estimation(xi, MoIoSt):
        '''
        Pitzer model for parameter estimation

        adjustable parameters:
            1. beta0_ij
            2. beta1_ij
            3. C_ij

        args:
            xi: adjustable parameters
            MoIoSt: molal ionic strength
        '''
        try:
            # set vars
            pass
        except Exception as e:
            raise Exception('Pitzer parameter estimation failed!')
