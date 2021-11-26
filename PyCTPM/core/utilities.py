# UTILITY FUNCTIONS
# ------------------

# import packages/modules
import os
import numpy as np
import pandas as pd
# internal
from PyCTPM.core.config import ROUND_FUN_ACCURACY
from PyCTPM.database import DATABASE_INFO
from PyCTPM.core.info import packageShortName


def roundNum(value, ACCURACY=ROUND_FUN_ACCURACY):
    '''
    round a number, set decimal digit
    '''
    return np.round(value, ACCURACY)


def removeDuplicatesList(value):
    ''' 
    remove duplicates from a list
    '''
    print(value)
    return list(dict.fromkeys(value))


def database():
    '''
    list of database name
    '''
    databaseNameList = [item['name'] for item in DATABASE_INFO]
    return databaseNameList


def comp():
    '''
    list of available components in the database
    '''
    try:
        # data path
        dataMainDir = packageShortName + '\database'
        dataFile = DATABASE_INFO[0]['file']
        dataPath = os.path.join(dataMainDir, dataFile)
        print("dataPath: ", dataPath)

        with open(dataPath, 'r') as file:
            reader = pd.read_csv(dataPath)
            # print("reader shape: ", reader.shape)
            print(reader.to_string())
    except Exception as e:
        raise


def csvLoader(databaseName, compList):
    '''
    load database
    args:
        databaseName: name of database
    return:
        array of data
    '''
    try:
        print(0)
    except Exception as e:
        raise
