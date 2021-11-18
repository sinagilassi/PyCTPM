# EXTRACT DATA
# -------------

# import module/packages


class ExtCoreClass:
    '''
    code for extracting data from database (csv, txt, ...)
    '''

    def __init__(self, propName, compList, modelInput, unit="SI"):
        self.propName = propName
        self.compList = compList
        self.modelInput = modelInput
        self.unit = unit

    def propSet(self):
        return self.propName
