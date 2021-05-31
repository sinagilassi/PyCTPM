
import docs.eosPR as myFun


# from ctpm.ctpm import

import numpy as np

# from docs.eosPR import _eosPR

"""
Chemical Thermodynamics for Process Modeling
"""

x = 2


def main():
    y = np.array([1, 2, 3])
    print(y)
    res = eosPR_import()
    # res = 10
    print("ctpm package is running!, res: {}".format(res))
    return res


def eosPR_import():
    return myFun._eosPR(2)
    # return eosPR._eosPR(2)
    print("eosPR_import")
    # return 10


if __name__ == "__main__":
    main()
