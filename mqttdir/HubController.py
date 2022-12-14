import DataProcesser
import pandas as pd
import mqttTools.subscribe as Sub
import ast
import redis
import pytz
import time
from datetime import datetime
import os

roomDictionary = {}
roomOccupancy  = {}
roomEmpty = 0
roomEmptyTime = None
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

def getData():
    global roomOccupancy
    seedData = {
        "RoomOccupancy": []
    }
    try:
        data = redis_cache.json().get("room")
        assert (data != None), "Database Empty"
        return data
    except :
        while os.stat("data.txt").st_size == 0:
            time.sleep(1)

        processData()
        firstEntry = list(roomOccupancy.keys())[0]
        seedData["RoomOccupancy"].append({"ESPId": firstEntry, "Occupants": roomOccupancy[firstEntry], "TimeSinceLast": None})
        redis_cache.json().set("room", ".", seedData)
        return seedData

def redisDataHandler():
    roomEmpty == 0
    currentData = getData()
    currentKeys = list((row["ESPId"] for row in currentData["RoomOccupancy"]))
    for key in roomOccupancy.keys():
            if not key in currentKeys:
                currentData["RoomOccupancy"].append({"ESPId":key,"Occupants":0,"TimeSinceLast": datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})

    for row in currentData["RoomOccupancy"]:
        if row["ESPId"] in roomOccupancy:
            row.update({"Occupants": roomOccupancy[row["ESPId"]], "TimeSinceLast": None})
        else:
            row.update({"Occupants": 0, "TimeSinceLast" : datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})
    redis_cache.json().set("room", ".", currentData) 

def allRoomsEmpty():
    global roomEmpty
    global roomEmptyTime
    if roomEmpty == 0:
        roomEmptyTime = datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")
        roomEmpty = 1
    currentData = getData()
    for row in currentData["RoomOccupancy"]:
        row.update({"Occupants": 0, "TimeSinceLast" : roomEmptyTime})
    redis_cache.json().set("room", ".", currentData) 

def run() :
    global roomDictionary
    global roomOccupancy
    Sub.run()
    while True:
        if not os.stat("data.txt").st_size == 0:
            processData()
            redisDataHandler()
            open("data.txt", "w").close()
            roomDictionary = {}
            roomOccupancy  = {}
            time.sleep(5)
        else:
           allRoomsEmpty()
           time.sleep(5)

def test():
    while True:
        print("test")
        time.sleep(1)

if __name__ == '__main__':
    run()