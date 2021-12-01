# PACKAGE INFO
# -------------

# import modules/packages
from PyCTPM.core import comp as compList
from PyCTPM.core.info import packageName, packageShortName, __version__, __description__


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

        # set
        dash = '-' * 40

        for i in range(len(data)):
            if i == 0:
                print(dash)
                print('{:^20s}{:^20s}'.format(data[i][0], data[i][1]))
                print(dash)
            else:
                print('{:<20s}{:>0s}'.format(
                    data[i][0].capitalize(), data[i][1]))
