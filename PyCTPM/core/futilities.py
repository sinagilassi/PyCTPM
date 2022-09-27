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

    @staticmethod
    def SaveNpArray(arr, file_name='', location=''):
        '''
        save numpy array
        '''
        try:
            # full file name
            if not file_name:
                file_name = "np_array"
            fullFileName = f"{file_name}.npy"
            # location
            fileLoc = os.path.join(location, fullFileName)

            # open
            with open(fileLoc, 'wb') as f:
                np.save(f, arr)

            print(f"save operation is done.")
        except Exception as e:
            raise
