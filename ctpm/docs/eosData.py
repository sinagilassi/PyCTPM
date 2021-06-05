# ACCESS COMPONENT
# -----------------

# import packages/modules
import json
from core.store import storeData

#


class dbClass(storeData):
    #! init
    def __init__(self):
        #
        self.data2 = dict()
        super().__init__()

    #! load json data
    def loadData(self):
        """
        load data from data store 
        """
        return self.data

    #! get component data

    def loadItemData(self, componentName):
        # print(type(componentName))
        # print(componentName)
        # var
        res = []
        for i in componentName:
            resLoop = [item for item in self.data if item['symbol'] == i]
            #! check
            if len(resLoop) == 1:
                res.append(resLoop[0])
                print("resLoop {}".format(resLoop))
            else:
                print(f"component {i} not found")
        # return
        return res
