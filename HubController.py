import DataProcesser
import pandas as pd
import mqttTools.subscribe as Sub
from multiprocessing import Process
import ast
import time

roomDictionary = {}
roomOccupancy  = {}
dataList = []

def processData():
    #while True:
    rawData = open("data.txt", "r").readlines()
    formatedData = []

    for row in rawData:
        formatedData.append(ast.literal_eval(row))

    inputData = pd.DataFrame(formatedData)
    DataProcesser.dataProcesser(inputData, roomDictionary)
    for key in roomDictionary:
        if not roomDictionary[key][1] in roomOccupancy:
            roomOccupancy.update({roomDictionary[key][1]: 1})
        else:
            roomOccupancy.update({roomDictionary[key][1]: roomOccupancy[roomDictionary[key][1]] + 1})
    print(roomOccupancy)

processData()
#p0 = Process(target=Sub.run)
#p0.start()
#p1 = Process(target=DataProcesser.dataProcesser(testData, "1", roomDictionary))
#p1.start()