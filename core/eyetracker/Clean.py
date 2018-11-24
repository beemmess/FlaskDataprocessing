import pandas as pd
import numpy as np
import scipy
import json

def convertToDataFrame(message):
    # Get the data string from the JSON
    data = message["data"]
    # Get the features string and split it up into list
    features = message["features"].split(",")
    # Read the data as csv in buffer and put name of columns as features
    df = pd.read_csv(pd.compat.StringIO(data), names=features)

    return df, features


def substitution(message):
    # get the data as a dataframe
    df, features = convertToDataFrame(message)
    # print(df.isnull().any(axis=1).index.values)
    null_rows = df[df.isnull().any(axis=1)].index.values

    # Generate list of lists of features, for substitution purpose
    features = [['leftX','rightX'],['rightX','leftX'],['leftY','rightY'],['rightY','leftY'],['pupilL','pupilR'],['pupilR','pupilL']]

    # Gazepoint/pupil substition link: https://arxiv.org/pdf/1703.09468.pdf
    # page 5 in the article
    for feature in features:
        df.loc[null_rows,feature[0]]=df.apply(lambda x : fx(x,feature),axis=1)

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
def fx(x,feature):
    if np.isnan(x[feature[0]]):
        return x[feature[1]]
    else:
        return x[feature[0]]



def interpolateMissingData(message):
    # get the data as a dataframe
    df, features = convertToDataFrame(message)

# https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.butter.html
# https://pandas.pydata.org/pandas-docs/stable/missing_data.html
    # delete rows after substition that still contains NaN
    # df = df.dropna()
    df = df.interpolate(method="linear")
    # convert the dataframe into csv string, with no row (index) numbers, and no header
    dataSub=df.to_csv(index=False,header=False)
    # save the type to preprocessed
    message["type"] = "interpolate"
    # save the preprocessed data into data value in JSON
    message["data"] = dataSub
    return message
