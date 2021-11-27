# DOCS UTILITY
# -------------

# import packages/modules
import os
import numpy as np
import pandas as pd
import csv
from typing import List
# internals
from PyCTPM.core import removeDuplicatesList, comp
from PyCTPM.database import DATABASE_INFO
from PyCTPM.core.info import packageShortName
from PyCTPM.docs.prop import propList


class dUtilityClass:
    def __init__(self):
        pass

    @staticmethod
    def extractCompData(compData, compProperty):
        """
        build a list of desired component data
        args:
            compData: component database dict list
            compProperty: property name
        """
        # try/except
        try:
            # prop list
            propList = [item[compProperty] for item in compData]
            return propList
        except Exception as e:
            raise

    @staticmethod
    def extractGenProp(compData, compProperty, headerIndex=[0, 1]):
        """
        build a list of desired component data
        args:
            compData: component database 2D-array
            compProperty: property name
        """
        try:
            # res
            res = []
            # header length
            headerLength = len(headerIndex)
            # find index
            propIndex = compData[0].index(compProperty)
            # loop
            for i in range(len(compData)):
                if i > headerLength - 1:
                    res.append(float(compData[i][propIndex]))

            if len(res) == 0:
                print("Database is empty!")
                raise Exception("Database is empty!")
            # res
            return res
        except Exception as e:
            raise

    @staticmethod
    def buildComponentList(compList):
        """ 
        build component list participated in 
        this list is used for component availability in the app database
        """
        # try/except
        try:
            # check availability of selected components
            compListApp = comp()
            compSymbolListApp = [item[1] for item in compListApp]

            # check
            for i in compList:
                if i not in compSymbolListApp:
                    raise Exception(
                        f"component {i} is not in the app database!")

            # unique names
            compListUnique = removeDuplicatesList(compList)
            return compListUnique

        except Exception as e:
            raise

    @staticmethod
    def checkAppPropList(propName):
        '''
        check property is available in the app prop list
        '''
        try:
            if propName in propList:
                return propName
            else:
                raise Exception(
                    f"property is not in the app property list!")
        except Exception as e:
            raise

    @staticmethod
    def mixtureMolecularWeight(MoFri, MWi, unit="g/mol"):
        """
        calculate mixture molecular weight [g/mol]
        args:
            MoFri: component mole fraction
            MWi: molecular weight [g/mol]
        """
        # try/exception
        try:
            # check
            if not isinstance(MoFri, np.ndarray):
                if isinstance(MoFri, List):
                    MoFri0 = np.array(MoFri)
            else:
                MoFri0 = np.copy(MoFri)

            if not isinstance(MWi, np.ndarray):
                if isinstance(MWi, List):
                    MWi0 = np.array(MWi)
            else:
                MWi0 = np.copy(MWi)

            # check
            if MoFri0.size != MWi0.size:
                raise Exception("elements are not equal")
            #
            MixMoWe = np.dot(MoFri0, MWi0)

            # check unit
            if unit == 'g/mol':
                MixMoWe
            elif unit == 'kg/mol':
                MixMoWe = MixMoWe*1e-3
            elif unit == 'kg/kmol':
                MixMoWe = MixMoWe

            return MixMoWe
        except Exception as e:
            print(e)
