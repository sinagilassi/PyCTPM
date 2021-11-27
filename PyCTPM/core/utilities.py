# UTILITY FUNCTIONS
# ------------------

# import packages/modules
import os
import numpy as np
import pandas as pd
import csv
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

        # component list
        compList = []

        csv.register_dialect('myDialect', delimiter=',',
                             skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        with open(dataPath, 'r') as file:
            reader = csv.reader(file)

            # ignore header
            next(reader, None)
            next(reader, None)

            for row in reader:
                compList.append((row[1], row[2]))

        if len(compList) > 0:
            return compList
        else:
            raise
    except Exception as e:
        raise


def loadGeneralData(compList):
    '''
    load general data of components
    args:
        compList: component list
    '''
    try:
        # data path
        dataMainDir = packageShortName + '\database'
        dataFile = DATABASE_INFO[0]['file']
        dataPath = os.path.join(dataMainDir, dataFile)

        csv.register_dialect('myDialect', delimiter=',',
                             skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        # component data
        compData = []

        file = open(dataPath, 'r')
        reader = csv.reader(file)

        header1 = next(reader, None)
        header2 = next(reader, None)

        # set
        # title
        compData.append(header1)
        # unit
        compData.append(header2)

        k = 0
        # init library
        for i in compList:
            for row in reader:
                if i == row[2]:
                    row[0] = k
                    compData.append(row)
                    k += 1
            # reset
            file.seek(0)

        return compData
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
        # data path
        dataMainDir = packageShortName + '\database'
        dataFile = [item['file']
                    for item in DATABASE_INFO if item['name'] == databaseName]
        # check
        if len(dataFile) == 0:
            raise Exception("Database is not found!")

        dataPath = os.path.join(dataMainDir, dataFile[0])

        with open(dataPath, 'r') as file:
            reader = csv.reader(file)

            # ignore header
            if databaseName == DATABASE_INFO[0]['name']:
                next(reader, None)
                next(reader, None)
            else:
                next(reader, None)

            for row in reader:
                compList.append((row[1], row[2]))

        print(0)
    except Exception as e:
        raise
