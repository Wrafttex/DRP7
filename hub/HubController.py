import DataProcesser
import pandas as pd
import mqttTools.subscribe as Sub
from multiprocessing import Process
import ast
import redis
import json
import pytz
from datetime import datetime

roomDictionary = {}
roomOccupancy  = {}
redis_cache = redis.Redis(host="redis",port=6379,decode_responses=True)

def processData():
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

def redisDataHandler():
    currentData = redis_cache.json().get("room")
    for key in roomOccupancy.keys():
        if not key in currentData["RoomOccupancy"]:
            currentData["RoomOccupancy"].append({"ESPId":key,"Occupants":0,"TimeSinceLast": datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})

    for row in currentData["RoomOccupancy"]:
        if row["ESPId"] in roomOccupancy:
            row.update({"Occupants": roomOccupancy[row["ESPId"]], "TimeSinceLast": None})
        else:
            row.update({"Occupants": 0, "TimeSinceLast" : datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})
    print(json.dumps(currentData, indent=4))
    redis_cache.json().set("room", ".", currentData)    

def run() :
        processData()
        redisDataHandler()
run() 
#p0 = Process(target=Sub.run)
#p0.start()
#p1 = Process(target=run())
#p1.start()