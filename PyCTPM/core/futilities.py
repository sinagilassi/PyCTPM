# FILE UTILITY
# -------------

# package/module list
import os
import json
import fnmatch
import re
import csv
import random
import numpy as np
from datetime import date


class FileUtilityClass:
    '''
    file utility class
    '''

    def __init__(self):
        pass

    @staticmethod
    def CheckFileFormat(filePath):
        '''
        check file format

        args:
            filePath: file name dir

        return:
            file directory, file name, file format
        '''
        # check file exist
        if os.path.isfile(filePath):
            # file analysis
            fileDir = os.path.dirname(filePath)
            fileName = os.path.basename(filePath)
            fileFormat = os.path.splitext(filePath)[1]
            fileFormat = str(fileFormat.split(".")[-1]).lower()
            # res
            return fileDir, fileName, fileFormat
        else:
            raise Exception('file path is not valid.')
