# FUGACITY CALCULATION FOR GAS/LIQUID/SOLID PHASE
# ------------------------------------------------

# import packages/modules
import numpy as np
import math
# local
from PyCTPM.docs.eos import eosClass


class FugacityClass:
    '''
    fugacity calculation
    '''

    def __init__(self):
        pass

    def _gasFugacityPR(self, eosParams, Z, P, T):
        '''
        estimation of gas fugacity using a EOS

        args:
            eosParams: eos params
                A: PR constant
                B: PR constant
            Z: compressibility factor (max value)
            P: pressure [Pa]
            T: temperature [K]
        '''
        try:
            # set
            A = eosParams.get("A")
            B = eosParams.get("B")
            # fugacity coefficient
            phi0 = (Z-1) - math.log(Z-B) - (A/(2*B*math.sqrt(2))) * \
                math.log((Z+(1+math.sqrt(2)*B))/(Z+(1-math.sqrt(2)*B)))
            phi = math.exp(phi0)
            # fugacity
            fugacity = phi*P

            # return
            return fugacity

        except print(0):
            pass
