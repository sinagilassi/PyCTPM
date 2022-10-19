# SOLUTION (SOLUTE AND SOLVENT)
# -------------------------------

# packages/modules
import numpy as np
# local
from PyCTPM.docs.electrolyte import ElectrolytesClass
from PyCTPM.docs.electrolyteactivity import ElectrolyteActivityClass


class Solution(ElectrolytesClass):
    def __init__(self, ions, solvent='water'):
        self.ions = ions
        self.solvent = solvent

        # * init class
        ElectrolytesClass.__init__(self, ions, solvent)

    def activity_coefficient(self, model='DH'):
        '''
        calculate activity coefficient for the solution
            1. ions
            2. solvent

        args:
            ions_molality: molality of ions *** list ***  
            model: activity coefficient model name (Debye_Huckel: default)
        '''
        try:
            modelSelection = {
                'DH': ElectrolyteActivityClass.Debye_Huckel_model_activity_coefficient,
                'Pitzer': ElectrolyteActivityClass.Pitzer_model_activity_coefficient
            }

            # call
            res = modelSelection.get(model)()

            return res
        except Exception as e:
            raise Exception("activity coefficient failed! ", e)
