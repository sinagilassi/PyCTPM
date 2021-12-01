# PACKAGE INFO
# -------------

# import modules/packages

# internals
from PyCTPM.core import comp as compList
from PyCTPM.core.info import packageName, packageShortName, __version__, __description__
from PyCTPM.database.dataInfo import DATABASE_GENERAL_ITEMS_FULL


class PackInfo:
    '''
    load component list available in the package
    '''
    # component
    _comp = ["NA"]

    def __init__(self):
        pass

    def __str__(self):
        compListSet = compList()
        compListSetStr = ' '.join(map(str, compListSet))
        return compListSetStr

    def __call__(self):
        '''
        call when a new class is initialted 
        '''
        compListSet = compList()
        compListSetStr = ' '.join(map(str, compListSet))
        print(compListSetStr)

    @property
    def comp(cls):
        return cls._comp

    @comp.setter
    def comp(cls, value):
        cls._comp = value
        cls._comp = compList()

    @staticmethod
    def components():
        compListSet = compList()
        # add header
        data = [['COMPONENT-NAME', 'SYMBOL'], *compListSet]
        # log
        PackInfo.logData(data)

    @staticmethod
    def properties():
        propertySet = DATABASE_GENERAL_ITEMS_FULL
        # largest
        propertyNames = max([len(item[0]) for item in propertySet]) + 5
        # add header
        data = [['PROPERTY-NAME', 'SYMBOL', 'UNIT'], *propertySet]
        # log
        PackInfo.logProperties(data, colCenterLen=propertyNames)

    def logData(data, colCenterLen=20):
        # set
        dash = '-' * (colCenterLen*2)

        for i in range(len(data)):
            if i == 0:
                print(dash)
                print('{:^{colCenterLen}s}{:^{colCenterLen}s}'.format(
                    data[i][0], data[i][1], colCenterLen=colCenterLen))
                print(dash)
            else:
                print('{:<{colCenterLen}s}{:>0s}'.format(
                    data[i][0].capitalize(), data[i][1], colCenterLen=colCenterLen))

    def logProperties(data, colCenterLen=20):
        # set
        dash = '-' * (colCenterLen*2)

        # col length set
        colLenManualSet = round(colCenterLen/2)

        for i in range(len(data)):
            if i == 0:
                print(dash)
                print('{:^{colCenterLen}s}{:^{colLenManualSet}s}{:^{colLenManualSet}s}'.format(
                    data[i][0], data[i][1], data[i][2], colCenterLen=colCenterLen, colLenManualSet=colLenManualSet))
                print(dash)
            else:
                print('{:<{colCenterLen}s}{:<{colLenManualSet}s}{:>0s}'.format(
                    data[i][0].capitalize(), data[i][1], data[i][2], colCenterLen=colCenterLen, colLenManualSet=colLenManualSet))
