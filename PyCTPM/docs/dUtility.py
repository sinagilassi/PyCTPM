# DOCS UTILITY
# -------------

# import packages/modules
import numpy as np
# internals
from PyCTPM.core import removeDuplicatesList


class dUtilityClass:
    def __init__(self):
        pass

    @staticmethod
    def buildComponentList(compList):
        """ 
        build component list participated in 
        this list is used for component availability in the app database
        """
        # try/except
        try:
            # all
            compList0 = []
            # check availability of selected components

            compListUnique = removeDuplicatesList(compList)
            return compListUnique

        except Exception as e:
            raise
