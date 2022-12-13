import DataProcesser
import pandas as pd
import mqttTools.subscribe as Sub
import ast
import redis
import json
import pytz
import time
from datetime import datetime
import os

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
    currentKeys = list((row["ESPId"] for row in currentData["RoomOccupancy"]))
    for key in roomOccupancy.keys():
            if not key in currentKeys:
                currentData["RoomOccupancy"].append({"ESPId":key,"Occupants":0,"TimeSinceLast": datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})

    for row in currentData["RoomOccupancy"]:
        if row["ESPId"] in roomOccupancy:
            row.update({"Occupants": roomOccupancy[row["ESPId"]], "TimeSinceLast": None})
        else:
            row.update({"Occupants": 0, "TimeSinceLast" : datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})
    #print(json.dumps(currentData, indent=4))
    redis_cache.json().set("room", ".", currentData)    

def run() :
    global roomDictionary
    global roomOccupancy
    while True:
        if not os.stat("data.txt").st_size == 0:
            processData()
            redisDataHandler()
            open("data.txt", "w").close()
            roomDictionary = {}
            roomOccupancy  = {}
            time.sleep(10)

if __name__ == '__main__':
    Sub.run()
    run()