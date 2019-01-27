import pandas as pd
import numpy as np
import scipy
import json

def convertToDataFrame(message):
    # Get the data string from the JSON
    data = message["data"]
    # Get the attributes string and split it up into list
    attributes = message["attributes"].split(",")
    # Read the data as csv in buffer and put name of columns as attributes
    df = pd.read_csv(pd.compat.StringIO(data), names=attributes)

    return df, attributes


def substitution(message):
    # get the data as a dataframe
    df, attributes = convertToDataFrame(message)
    # print(df.isnull().any(axis=1).index.values)
    null_rows = df[df.isnull().any(axis=1)].index.values

    # Generate list of lists of attributes, for substitution purpose
    attributesList = [['leftX','rightX'],['rightX','leftX'],['leftY','rightY'],['rightY','leftY'],['pupilL','pupilR'],['pupilR','pupilL']]

    # Gazepoint/pupil substition link: https://arxiv.org/pdf/1703.09468.pdf
    # page 5 in the article
    for attribute in attributesList:
        df.loc[null_rows,attribute[0]]=df.loc[null_rows].apply(lambda x : fx(x,attribute),axis=1)
    # fillna is used as to fill empty with string "NaN" so that when string is
    # parsed to double in e.g. Java, it will be regocnised as NaN
    # Then convert the dataframe into csv, with no row (index) numbers, and no header
    dataSub=df.fillna("NaN").to_csv(index=False,header=False)
    # save the type to preprocessed
    message["type"] = "substitution"
    # save the preprocessed data into data value in JSON
    message["data"] = dataSub

    return message

# This function checks for NaN values and replaces NaN with corresponding values
# from the other eye value
def fx(x,attribute):
    if np.isnan(x[attribute[0]]):
        return x[attribute[1]]
    else:
        return x[attribute[0]]



def interpolateMissingData(message):
    # get the data as a dataframe
    df, attributes = convertToDataFrame(message)

# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.butter.html
# https://pandas.pydata.org/pandas-docs/stable/missing_data.html
    df = df.interpolate(method="linear")
    # convert the dataframe into csv string, with no row (index) numbers, and no header
    dataSub=df.fillna("NaN").to_csv(index=False,header=False)
    # save the type to preprocessed
    message["type"] = "interpolate"
    # save the preprocessed data into data value in JSON
    message["data"] = dataSub
    return message


# def interpolateMissingDataAfterSubstitution(message):
#
#
# def removeNanRowsAfterSubstitution(message):
#
#     msgSub = substitution(message)
#
#     df, attributes = convertToDataFrame(msgSub)
#
#     data = df.dropna().to_csv(index=False, header=False)
#
#     message["type"] = ""
