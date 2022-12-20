import DataProcesser
import pandas as pd
import mqttTools.subscribe as Sub
import mqttTools.puplish as Pub
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
pubClient = 0
redis_cache = redis.Redis(host="redis",port=6379,decode_responses=True)

def processData():
    rawData = open("data.txt", "r").readlines()
    open("data.txt", "w").close()

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
    global pubClient
    roomEmpty == 0
    count = 0
    currentData = getData()
    currentKeys = list((row["ESPId"] for row in currentData["RoomOccupancy"]))
    for key in roomOccupancy.keys():
            if not key in currentKeys:
                currentData["RoomOccupancy"].append({"ESPId":key,"Occupants":0,"TimeSinceLast": datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})

    for row in currentData["RoomOccupancy"]:
        EspId = row["ESPId"]
        if  EspId in roomOccupancy:
            row.update({"Occupants": roomOccupancy[EspId], "TimeSinceLast": None})
            Pub.publish(pubClient, "True", f"{EspId}/occupancy")
        else:
            row.update({"Occupants": 0, "TimeSinceLast" : datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")})
            Pub.publish(pubClient, "False", f"{EspId}/occupancy")
        count += 1

    print(f"Publish count: {count}")
            
    redis_cache.json().set("room", ".", currentData) 

def allRoomsEmpty():
    global roomEmpty
    global roomEmptyTime
    if roomEmpty == 0:
        roomEmptyTime = datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M")
        roomEmpty = 1
    currentData = getData()
    for row in currentData["RoomOccupancy"]:
        espId = row["ESPId"]
        row.update({"Occupants": 0, "TimeSinceLast" : roomEmptyTime})
        Pub.publish(pubClient, "False", f"{espId}/occupancy")
    redis_cache.json().set("room", ".", currentData) 

def run():
    global roomDictionary
    global roomOccupancy
    global pubClient
    Sub.run()
    pubClient = Pub.run()
    while True:
        rawData = open("data.txt", "r")
        if not os.stat("data.txt").st_size == 0:
            processData()
            redisDataHandler()
            roomDictionary = {}
            roomOccupancy  = {}
            time.sleep(1)
        else:
            allRoomsEmpty()
            rawData.close()
            time.sleep(1)

def test():
    while True:
        print("test")
        time.sleep(1)

if __name__ == '__main__':
    run()