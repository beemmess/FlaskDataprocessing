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

def avgGSRandPPG(message):
    # get the data as a dataframe
    df, features = convertToDataFrame(message)

    # calculate the mean of pupil diameters
    avgGSR = df['GSR'].mean()
    avgPPG = df['PPG'].mean()
    # change the type to "avgPupil"
    message["type"] = "avgGSRandPPG"
    # change features to avgPupilL and avgPupilR
    message["features"] = "avgGSR,avgPPG"
    # save the average data in the "data" value in the JSON
    message["data"] = "{},{}".format(avgGSR,avgPPG)
    return message

def normalize(message):
    df, features = convertToDataFrame(message)
    # Get list of tasks example [1, 2, 3, 4......]
    listOfTasks = df["task"].unique()
    # Count how many taskst there are example: 4
    nrOfTasks = listOfTasks.shape[0]
    # create an empty list
    dfList=[]
    # iterate through the data with task number (for example: 1) and store each
    # datafame in a list
    for task in listOfTasks:
        dfList.append(df.loc[df["task"]==task])

    # Create an empty list for average of GSR and PPG for each task
    avgGSRList = []
    avgPPGList = []
    # iterate through the dataframe list, and store each mean in a list
    for dataframe in dfList:
        avgGSRList.append(dataframe["GSR"].mean())
        avgPPGList.append(dataframe["PPG"].mean())

    # sum up the average list
    sumAvgGSR = sum(avgGSRList)
    sumAvgPPG = sum(avgPPGList)
    # calculate the average GSR/PPG of all tasks
    avgGSR = sumAvgGSR/nrOfTasks
    avgPPG = sumAvgPPG/nrOfTasks

    # iterate through all the data and normalize the dataset
    # the result is equation 5.1 page 90 in:
    # Robost Multimodel Cognitive Load Measurement
    # print(df)
    df["GSR"]=df.apply(lambda x : x["GSR"]/avgGSR, axis=1)
    df["PPG"]=df.apply(lambda y : y["PPG"]/avgPPG, axis=1)
    dataSub=df.to_csv(index=False,header=False)
    # change the type to "normalized"
    message["type"] = "normalize"
    message["data"] = dataSub

    return message

    # print(df)
