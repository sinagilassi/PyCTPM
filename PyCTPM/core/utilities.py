# UTILITY FUNCTIONS
# ------------------

# import packages/modules
import os
import numpy as np
import pandas as pd
import csv
# internal
from PyCTPM.core.config import ROUND_FUN_ACCURACY
from PyCTPM.database import DATABASE_INFO, DATABASE_FOLDER_NAME
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
        # data file
        dataFile = DATABASE_INFO[0]['file']
        # abs path
        pathAbs = os.path.abspath(os.path.dirname(__file__))
        # relative path to database file
        dataPathDirRel = '../' + DATABASE_FOLDER_NAME
        # database file
        dataPath = os.path.join(pathAbs, dataPathDirRel, dataFile)

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
                compList.append([row[1], row[2]])

        if len(compList) > 0:
            return compList
        else:
            raise
    except Exception as e:
        raise


def loadGeneralDataV1(compList):
    '''
    load general data of components
    args:
        compList: component list
    '''
    try:
        # data path
        # dataMainDir = packageShortName + '\database'
        # dataFile = DATABASE_INFO[0]['file']
        # dataPath = os.path.join(dataMainDir, dataFile)

        # data file
        dataFile = DATABASE_INFO[0]['file']
        # abs path
        pathAbs = os.path.abspath(os.path.dirname(__file__))
        # relative path to database file
        dataPathDirRel = '../' + DATABASE_FOLDER_NAME
        # database file
        dataPath = os.path.join(pathAbs, dataPathDirRel, dataFile)

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


def loadGeneralDataV2(compList):
    '''
    load general data of components
    args:
        compList: component list
    '''
    try:
        # data path
        # dataMainDir = packageShortName + '\database'
        # dataFile = DATABASE_INFO[0]['file']
        # dataPath = os.path.join(dataMainDir, dataFile)

        # data file
        dataFile = DATABASE_INFO[0]['file']
        # abs path
        pathAbs = os.path.abspath(os.path.dirname(__file__))
        # relative path to database file
        dataPathDirRel = '../' + DATABASE_FOLDER_NAME
        # database file
        dataPath = os.path.join(pathAbs, dataPathDirRel, dataFile)

        csv.register_dialect('myDialect', delimiter=',',
                             skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        # component data
        compData = []
        compDataIndex = []
        compDataSelected = []

        file = open(dataPath, 'r')
        reader = csv.DictReader(file)

        # skip unit row
        next(reader, None)

        # convert to dict
        for row in reader:
            compData.append(row)

        # find compo index in data comp
        for i in compList:
            _loop1 = [j for j, item in enumerate(
                compData) if i in item.values()]
            compDataIndex.append(_loop1[0])

        # select
        for j in compDataIndex:
            compDataSelected.append(compData[j])

        return compDataSelected
    except Exception as e:
        raise


def loadGeneralDataV3(compList, state):
    '''
    load general data of components

    args:
        compList: component list
        state: component state (g,l,aq)

    output:
        dict of list of thermodynamic data 
    '''
    try:
        # data path
        # dataMainDir = packageShortName + '\database'
        # dataFile = DATABASE_INFO[0]['file']
        # dataPath = os.path.join(dataMainDir, dataFile)

        # data file
        dataFile = DATABASE_INFO[0]['file']
        # abs path
        pathAbs = os.path.abspath(os.path.dirname(__file__))
        # relative path to database file
        dataPathDirRel = '../' + DATABASE_FOLDER_NAME
        # database file
        dataPath = os.path.join(pathAbs, dataPathDirRel, dataFile)

        csv.register_dialect('myDialect', delimiter=',',
                             skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        # component data
        compData = []
        compDataIndex = []
        compDataSelected = []
        compDataSelectedDict = {}

        file = open(dataPath, 'r')
        reader = csv.DictReader(file)

        # skip unit row
        next(reader, None)

        # convert to dict
        for row in reader:
            compData.append(row)

        # find compo index in data comp
        for i in enumerate(zip(compList, state)):
            _loop1 = [j for j, item in enumerate(
                compData) if i[0] in item.values()]
            compDataIndex.append(_loop1[0])

        # select
        for j in compDataIndex:
            compDataSelected.append(compData[j])

        #! check
        if len(compDataSelected) == 1:
            return compDataSelected[0]
        else:
            raise Exception("component not found!")

    except Exception as e:
        raise


def loadGeneralDataInfo():
    '''
    load info of the general data of components
    '''
    try:
        # data path
        # dataMainDir = packageShortName + '\database'
        # dataFile = DATABASE_INFO[0]['file']
        # dataPath = os.path.join(dataMainDir, dataFile)

        # data file
        dataFile = DATABASE_INFO[0]['file']
        # abs path
        pathAbs = os.path.abspath(os.path.dirname(__file__))
        # relative path to database file
        dataPathDirRel = '../' + DATABASE_FOLDER_NAME
        # database file
        dataPath = os.path.join(pathAbs, dataPathDirRel, dataFile)

        csv.register_dialect('myDialect', delimiter=',',
                             skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        # component data
        infoData = []

        file = open(dataPath, 'r')
        reader = csv.DictReader(file)

        k = 0
        # save title/unit
        for row in reader:
            if k < 1:
                infoData.append(row)
                k += 1
            else:
                break

        return infoData
    except Exception as e:
        raise Exception("loading database failed!", e)


def checkUnitGeneralData(headerInfo, propName):
    '''
    display info of the general data of components 
        header 1: symbol
        header 2: unit
    args:
        headerInfo: the first two rows
        propName: the symbol of property
    '''
    try:
        if propName == 'ALL':
            # delete
            headerInfo.pop("no")
            headerInfo.pop("component-name")
            headerInfo.pop("component-symbol")
            return headerInfo
        else:
            # find
            propUnit = ''
            for key in headerInfo.keys():
                if key == propName:
                    propUnit = headerInfo[key]

            if not propUnit:
                raise Exception("property unit not found!")
            else:
                return propUnit

    except Exception as e:
        raise Exception("try error!", e)


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
        # dataMainDir = packageShortName + '\database'
        dataFile = [item['file']
                    for item in DATABASE_INFO if item['name'] == databaseName]
        # check
        if len(dataFile) == 0:
            raise Exception("Database is not found!")

        # abs path
        pathAbs = os.path.abspath(os.path.dirname(__file__))
        # relative path to database file
        dataPathDirRel = '../' + DATABASE_FOLDER_NAME
        # database file
        dataPath = os.path.join(pathAbs, dataPathDirRel, dataFile[0])

        # dataPath = os.path.join(dataMainDir, dataFile[0])

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


def csvLoaderV2(compList, databaseName, rowsSkip=0):
    '''
    load csv data of components
    args:
        compList: component list
    output:
        dict
    '''
    try:
        # data path
        # dataMainDir = packageShortName + '\database'
        # dataFile = databaseName
        # dataPath = os.path.join(dataMainDir, dataFile)

        # data file
        dataFile = databaseName
        # abs path
        pathAbs = os.path.abspath(os.path.dirname(__file__))
        # relative path to database file
        dataPathDirRel = '../' + DATABASE_FOLDER_NAME
        # database file
        dataPath = os.path.join(pathAbs, dataPathDirRel, dataFile)

        csv.register_dialect('myDialect', delimiter=',',
                             skipinitialspace=True, quoting=csv.QUOTE_MINIMAL)

        # component data
        compData = []
        compDataIndex = []
        compDataSelected = []

        file = open(dataPath, 'r')
        reader = csv.DictReader(file)

        # skip unit row
        if rowsSkip > 0:
            for r in range(rowsSkip):
                next(reader, None)

        # convert to dict
        for row in reader:
            compData.append(row)

        # find compo index in data comp
        for i in compList:
            _loop1 = [j for j, item in enumerate(
                compData) if i in item.values()]
            compDataIndex.append(_loop1[0])

        # select
        for j in compDataIndex:
            compDataSelected.append(compData[j])

        return compDataSelected
    except Exception as e:
        raise


def loadAllData(compList):
    '''
    load all data (csv)
    args:
        compList: component list
    output:
        dict 
    '''
    try:
        # database name

        # load general data
        _d1 = loadGeneralDataV2(compList)
        # load heat capacity at constant pressure
        _d2 = csvLoaderV2(compList, DATABASE_INFO[1]['file'])
        # load thermal conductivity
        _d3 = csvLoaderV2(compList, DATABASE_INFO[2]['file'], 1)
        # load viscosity
        _d4 = csvLoaderV2(compList, DATABASE_INFO[3]['file'], 1)

        # data
        databaseSet = {
            DATABASE_INFO[0]['name']: _d1,
            DATABASE_INFO[1]['name']: _d2,
            DATABASE_INFO[2]['name']: _d3,
            DATABASE_INFO[3]['name']: _d4
        }
        # return
        return databaseSet

    except Exception as e:
        raise Exception("loading failed! ", e)


def loadDataEOS(compList):
    '''
    load eos (general) data
    args:
        compList: component name list
    output:
        dict
    '''
    try:
        # load general data
        _d1 = loadGeneralDataV2(compList)
        # return
        return _d1
    except Exception as e:
        raise Exception("loading failed! ", e)
