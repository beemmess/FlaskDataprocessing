import pandas as pd
import numpy as np
import json

def convertToDataFrame(message):
    # Get the data string from the JSON
    data = message["data"]
    # Get the attributes string and split it up into list
    attributes = message["attributes"].split(",")
    # Read the data as csv in buffer and put name of columns as attributes
    df = pd.read_csv(pd.compat.StringIO(data), names=attributes)

    return df, attributes


def avgPupilDiameter(message):
    # get the data as a dataframe
    df, attributes = convertToDataFrame(message)

    # calculate the mean of pupil diameters
    avgPupilL = df['pupilL'].mean()
    avgPupilR = df['pupilR'].mean()
    # change the type to "avgPupil"
    message["type"] = "avgPupil"
    # change attributes to avgPupilL and avgPupilR
    message["attributes"] = "avgPupilL,avgPupilR"
    # save the average data in the "data" value in the JSON
    message["data"] = "{},{}".format(avgPupilL,avgPupilR)
    return message


def avgPupilDiameterForEachTask(message):
    # get the data as a dataframe
    df, attributes = convertToDataFrame(message)
    # Get the neccesary fetures
    df = df[['pupilL','pupilR','task']]
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
    # Create an empty list for pupil for each task
    dfAvgList = []
    # calculate the mean of pupil diameters for each task
    for dataframe in dfList:
        task = (dataframe["task"].unique()).tolist()
        task = ''.join(task)
        avgPupilL = dataframe["pupilL"].mean()
        avgPupilR = dataframe["pupilR"].mean()
        dfAvgList.append([avgPupilL,avgPupilR,task])
    df = pd.DataFrame(dfAvgList)

    # change the type to "avgPupilTasks"
    message["type"] = "avgPupilTasks"
    # change attributes to avgPupilL and avgPupilR
    message["attributes"] = "avgPupilL,avgPupilR,task"
    dataSub=df.dropna().to_csv(index=False,header=False)
    # save the average data in the "data" value in the JSON
    message["data"] = dataSub
    return message
