# LOADDATA CLASS
# ---------------

# packages/modules
import os
import numpy as np
import pandas as pd
from PyCTPM.core.futilities import FileUtilityClass


class LoaddataClass:
    def __init__(self):
        pass

    @staticmethod
    def load_csv_to_df(csv_file):
        '''
        remove duplicated rows according to column_name value

        args:
            csv_file: csv file path

        return:
            df_new: dataframe
            rowNo: row number
            colNo: column number
            colsName: column name
        '''
        try:
            # file path (complete)
            filePath = csv_file.strip()

            fileDir, fileName, fileFormat = FileUtilityClass.CheckFileFormat(
                filePath)

            # dataframe
            df = pd.read_csv(filePath)
            # remove duplicated records
            df_new = df.drop_duplicates()

            # column names
            colsName = list(df_new.columns)

            # unit
            unitName = list(df_new.iloc[0])

            # data
            df_data = df_new.iloc[1:]

            # numpy array
            np_data = df_data.to_numpy()

            # data no
            rowNo, colNo = df_data.shape

            return np_data, df_data, rowNo, colNo, colsName

        except Exception as e:
            raise

    @staticmethod
    def Pxy_BinarySystemInterpretData(pool, np_data, rowNo, vapor_pressure_method):
        '''
        sort Pxy data
        '''
        # calculate activity coefficient using modified-raoult's law
        AcCo = np.zeros((rowNo, 2))
        xi = np.zeros((rowNo, 2))

        for i in range(rowNo):
            # check for x1=0, activity coefficient is not defined
            if i > 0 and i < rowNo-1:
                # set
                _T = float(np_data[i, 1])
                _P = float(np_data[i, 2])
                # component 1
                _x1 = float(np_data[i, 3])
                _y1 = float(np_data[i, 4])
                # component 2
                _x2 = 1 - _x1
                _y2 = 1 - _y1
                # mix
                xi[i, 0] = _x1
                xi[i, 1] = _x2

                # for component 1
                # vapor-pressure at T
                _VaPr1 = pool[0].vapor_pressure(
                    _T, vapor_pressure_method)

                # activity coefficient
                _AcCo1 = (_y1*_P)/(_x1*_VaPr1)
                AcCo[i, 0] = _AcCo1

                # for component 2
                # vapor-pressure at T
                _VaPr2 = pool[1].vapor_pressure(
                    _T, vapor_pressure_method)

                # activity coefficient
                _AcCo2 = (_y2*_P)/(_x2*_VaPr2)
                AcCo[i, 1] = _AcCo2

        # res
        return AcCo, xi, _T
