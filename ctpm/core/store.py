# STORE - STATE MANAGEMENT
# ------------------------

# import packages/modules
import json

#


class storeData:
    #! init
    def __init__(self) -> None:
        """ load json data """
        # * rest
        self.data = dict()
        # * set
        self.initData(self)

    #! init json data
    def initData(self):
        # var
        payload = {}
        # try/except
        try:
            # database file
            appPath = "database\component.json"
            with open(appPath) as f:
                payload = json.load(f)
                self.data = payload.copy()
        except NameError:
            print(NameError)
            self.data.clear()

    #! get data
    def getData(self):
        return self.data
