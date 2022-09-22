# DATASOURCE
# -----------

# packages/modules


class DataSource:
    def __init__(self):
        pass

    @staticmethod
    def dbSearch(id, state, fn, db):
        '''
        general data

        args:
            id:
            state:
        '''

        # loop db
        for dbRecord in db:
            _csv = dbRecord['file']
            _res = fn([id], [state], _csv)
            # ! check data exists
            if _res:
                return _res

        return -1
