"""
Peng-Robinson (PR) equation of state
"""

from core import constants


# main


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
    print("PR result is: {}".format(x))

    return x*100


#
if __name__ == "__main__":
    main()
