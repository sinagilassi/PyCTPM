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
