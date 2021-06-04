# ACCESS COMPONENT
# -----------------

# import packages/modules
import json
from core.store import storeData

#


class dbClass(storeData):
    #! init
    def __init__(self) -> None:
        #
        self.data2 = dict()
        super.__init__(self)

    #! load json data
    def loadData(self):
        print(self.data)
        # return self.data
