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

    def calMolalIonicStrength(self, Moli):
        '''
        molal ionic strength

        args:
            Moli: molality of ions 
        '''
        try:
            Ii = np.zeros(self.ionNo)
            for i in range(self.ionNo):
                _ion = self.ions[i]
                Ii[i] = Moli[i]*(_ion.charge**2)

            # res
            return 0.5*np.sum(Ii)
        except Exception as e:
            raise Exception('molal ionic strength failed!')
