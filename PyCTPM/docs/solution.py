# SOLUTION (SOLUTE AND SOLVENT)
# -------------------------------

# packages/modules
import numpy as np
# local
from PyCTPM.docs.electrolyte import ElectrolytesClass
from PyCTPM.docs.electrolyteactivity import ElectrolyteActivityClass


class Solution(ElectrolytesClass, ElectrolyteActivityClass):

    # !constants
    # solvent
    _solvent_id = 'H2O'
    _solvent_MW = 18.01528  # g/mol

    def __init__(self, ions, molalities, solvent, solvent_molality, reaction_stoichiometric):
        self.ions = ions
        self.molalities = molalities
        self.solvent = solvent
        self.solvent_molality = solvent_molality
        self.reaction_stoichiometric = reaction_stoichiometric

        # set
        self.ionNo = len(ions)

        # * init class
        ElectrolytesClass.__init__(self, ions, solvent)
        ElectrolyteActivityClass.__init__(self)

    def electrolyte_solution_mole_fraction(self):
        '''
        calculate mole fraction of electrolyte solution

        return:
            MoFri: mole fraction *** narray ***
        '''
        try:
            # REVIEW
            _c0 = np.array(self.molalities).sum() + (1/(self._solvent_MW*1e-3))
            # mole fraction
            MoFri = np.zeros(self.ionNo+1)
            for i in range(self.ionNo):
                MoFri[i] = self.molalities[i]/_c0

            # solvent (water)
            MoFri[-1] = 1 - np.sum(MoFri)

            # res
            return MoFri

        except Exception as e:
            raise Exception("mole fraction calculation error!")

    def activity_coefficient(self, T, model='Debye_Huckel'):
        '''
        calculate activity coefficient for the solution
            1. ions
            2. solvent

        Debye-Huckel model

        input:
            SoDe: solvent density (water)
            T: temperature [K]
            er: dielectric constant (from database)
            MoIoSt: molal ionic strength
            zi: charge list

        args:
            ions_molality: molality of ions *** list ***  
            model: activity coefficient model name (Debye_Huckel: default)
        '''
        try:
            # model selection
            modelSelection = {
                'Debye_Huckel': self.Debye_Huckel_model_activity_coefficient,
                'Pitzer': self.Pitzer_model_activity_coefficient
            }

            # FIXME
            Pitzer_adjParams = (0.04835, 0.2122, -0.00084)

            # params
            paramsSelection = {
                "Debye_Huckel": (self.calMolalIonicStrength(self.molalities), self.ionsCharge(),
                                 self.WaterDensity(T), T, self.WaterDielectric(T)),
                "Pitzer": (self.calMolalIonicStrength(self.molalities), self.ionsCharge(),
                           self.WaterDensity(T), T, self.WaterDielectric(
                               T), self.solvent_molality,
                           self.reaction_stoichiometric, Pitzer_adjParams)
            }

            # call
            res = modelSelection.get(model)(paramsSelection.get(model))

            return res
        except Exception as e:
            raise Exception("activity coefficient failed! ", e)
