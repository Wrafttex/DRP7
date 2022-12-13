import DataProcesser
import pandas as pd
import mqttTools.subscribe as Sub
from multiprocessing import Process
import ast
import redis
import json
import time
from datetime import datetime

roomDictionary = {}
roomOccupancy  = {}
redis_cache = redis.Redis(host="redis",port=6379,decode_responses=True)

# currentData =  {
#     "RoomOccupancy": [
#         {"ESPId":"testId0","Occupants":2,"TimeSinceLast": None},
#         {"ESPId":"testId1","Occupants":3,"TimeSinceLast": None},
#         {"ESPId":"testId2","Occupants":1,"TimeSinceLast": None},
#         {"ESPId":"testId3","Occupants":5,"TimeSinceLast": None},
#         {"ESPId":"testId4","Occupants":0,"TimeSinceLast": "13:50"},
#         {"ESPId":"testId5","Occupants":0,"TimeSinceLast": "14:15"}
#     ]
# }

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
    #print(roomOccupancy)
    #print(currentData)

def redisDataHandler():
    currentData = redis_cache.json().get("room")
    #print(json.dumps(currentData, indent=4))
    for key in roomOccupancy.keys():
        if not key in currentData["RoomOccupancy"]:
            currentData["RoomOccupancy"].append({"ESPId":key,"Occupants":0,"TimeSinceLast": datetime.now().strftime("%H:%M")})

    for row in currentData["RoomOccupancy"]:
        if row["ESPId"] in roomOccupancy:
            row.update({"Occupants": roomOccupancy[row["ESPId"]], "TimeSinceLast": None})
        else:
            row.update({"Occupants": 0, "TimeSinceLast" : datetime.now().strftime("%H:%M")})
    print(json.dumps(currentData, indent=4))
    redis_cache.json().set("room", ".", currentData)    

processData()
redisDataHandler()
#p0 = Process(target=Sub.run)
#p0.start()
#p1 = Process(target=DataProcesser.dataProcesser(testData, "1", roomDictionary))
#p1.start()