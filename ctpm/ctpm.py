# import docs.eosPR as myFun
# from ctpm.ctpm import


"""
Chemical Thermodynamics for Process Modeling
"""

x = 2


def main():
    res = eosPR_import()
    # res = 10
    print("ctpm package is running!, res: {}".format(res))
    return res


def eosPR_import():
    # return myFun._eosPR(2)
    return eosPR._eosPR(2)
    print("eosPR_import")
    # return 10


if __name__ == "__main__":
    main()
