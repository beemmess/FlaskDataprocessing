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

def normalizedGSR(message):
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

    # Create an empty list of average GSR list
    avgGSRList = []
    # iterate through the dataframe list, and store each mean in a list
    for dataframe in dfList:
        avgGSRList.append(dataframe["GSR"].mean())
    # sum up the average list
    sumAvgGSR = sum(avgGSRList)
    # calculate the average GSR of all tasks
    avgGSR = sumAvgGSR/nrOfTasks
    # iterate through all the data and normalize the dataset
    # the result is equation 5.1 page 90 in:
    # Robost Multimodel Cognitive Load Measurement
    print(df)
    df["GSR"]=df.apply(lambda x : x["GSR"]/avgGSR,axis=1)

    print("done")
    print(df)

    # change the type to "normalized"
    message["type"] = "normalized"
    message["features"] = "timestamp,normGSR,PPG,task"

    # return message

    # print(df)
