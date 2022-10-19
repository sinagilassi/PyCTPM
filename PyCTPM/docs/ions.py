# ELECTROLYTE IONS
# ------------------

# packages/modules
import re
# local


class Ion():
    '''
    ion class defines ions and properties

    initialization:
        id: symbol(charge)
    '''

    # ! vars
    # ion charge
    _charge = 0
    _ion_type = ''
    _symbol = ''

    def __init__(self, id):
        self.id = id

        # * set
        self.ionCharge()

        # ion
        ion = {
            "symbol": self.symbol,
            "charge": self.charge,
            "ion_type": self.ion_type
        }

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @property
    def charge(self):
        return self._charge

    @charge.setter
    def charge(self, value):
        self._charge = value

    @property
    def ion_type(self):
        return self._ion_type

    @ion_type.setter
    def ion_type(self, value):
        self._ion_type = value

    def ionCharge(self):
        '''
        interpret ion charge
        '''
        _ion = re.search(
            r"([a-zA-Z0-9.]+)\(([0-9])*(\-|\+)\)", str(self.id))

        # ! check
        if _ion:
            self.symbol = _ion.group(1)
            self.charge = float(_ion.group(3) + _ion.group(2))
            self.ion_type = 'cation' if _ion.group(3) == '+' else 'anion'
