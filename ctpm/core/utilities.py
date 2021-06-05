# UTILITY FUNCTIONS
# ------------------

# import packages/modules
import numpy as np

# round a number, set decimal digit


def roundNum(value, ACCURACY=2):
    return np.round(value, ACCURACY)

 # remove duplicates


def removeDuplicatesList(value):
    print(value)
    return list(dict.fromkeys(value))
