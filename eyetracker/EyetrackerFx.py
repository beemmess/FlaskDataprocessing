import pandas as pd
import numpy as np
import json

def convertToDataFrame(message):
    # Get the data string from the JSON
    data = message["data"]
    # Get the features string and split it up into list
    features = message["features"].split(",")
    # Read the data as csv in buffer and put name of columns as features
    df = pd.read_csv(pd.compat.StringIO(data), names=features)

    return df, features

def averagePupilDiameter(message):
    # get the data as a dataframe
    df, features = convertToDataFrame(message)

    # calculate the mean of pupil diameters
    avgPupilL = df['pupilL'].mean()
    avgPupilR = df['pupilR'].mean()
    # change the type to "avgPupil"
    message["type"] = "avgPupil"
    # change features to avgPupilL and avgPupilR
    message["features"] = "avgPupilL,avgPupilR"
    # save the average data in the "data" value in the JSON
    message["data"] = "{},{}".format(avgPupilL,avgPupilR)
    return message
