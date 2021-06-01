"""
Peng-Robinson (PR) equation of state
"""

from core import constants


# main


x = constants.R_CONST


def main():
    print("PR EOS")
    print(constants.R_CONST)

    return _eosPR(1)

# PR EOS


def _eosPR(x):
    """[summary]

    Args:
        x ([type]): [description]
    """

    y = x * constants.R_CONST
    print("PR result is: {}".format(y))

    return y*100


#
if __name__ == "__main__":
    main()
