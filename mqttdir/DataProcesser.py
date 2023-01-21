import ast
import time
import pandas as pd
import queue

def dataProcesser(data):
    roomDictionary = {}
    roomBleList = pd.DataFrame(data).drop(columns=["speed", "interval", "idType", "rssi@1m", "raw", "distance"])
    
    for row in roomBleList.index:
        if not roomBleList["mac"][row] in roomDictionary.keys():
            roomDictionary.update({roomBleList["mac"][row]: [roomBleList["rssi"][row], roomBleList["roomId"][row]]})
        elif roomDictionary[str(roomBleList["mac"][row])][1] == roomBleList["roomId"][row]:
            continue
        else:
            if roomBleList["rssi"][row] >= roomDictionary[str(roomBleList["mac"][row])][0]:
                roomDictionary.update({roomBleList["mac"][row]: [roomBleList["rssi"][row], roomBleList["roomId"][row]]})
            else:
                continue

    roomOccupancy = {}
    for key in roomDictionary:
        if not roomDictionary[key][1] in roomOccupancy:
            roomOccupancy.update({roomDictionary[key][1]: 1})
        else:
            roomOccupancy.update({roomDictionary[key][1]: roomOccupancy[roomDictionary[key][1]] + 1})

    return roomOccupancy


def redisDataHandler(roomOccupancy: dict, redis_cache):
    currentData = redis_cache.json().get("room")
    currentTime = time.time()
    
    if currentData == None: # if database Empty
        currentData = {"RoomOccupancy": []}
        currentKeys = []
    else:
        currentKeys = list((row["ESPId"] for row in currentData["RoomOccupancy"]))
    
    for key in roomOccupancy.keys():
        if key not in currentKeys:
            currentData["RoomOccupancy"].append({"ESPId":key,"Occupants":0,"TimeSinceLast": currentTime})

    for row in currentData["RoomOccupancy"]:
        EspId = row["ESPId"]
        if EspId in roomOccupancy:
            row.update({"Occupants": roomOccupancy[EspId], "TimeSinceLast": currentTime})
            
    redis_cache.json().set("room", ".", currentData) 

def processData(dataQueue: queue.Queue, redis_cache):
    while True:
        if not dataQueue.empty():
            numItems = 0
            formatedData = []
            while numItems <= 50:
                numItems += 1
                try:
                    data = dataQueue.get_nowait()
                    formatedData.append(ast.literal_eval(data))
                    dataQueue.task_done()
                except queue.Empty:
                    break

            inputData = pd.DataFrame(formatedData)
            roomOccupancy = dataProcesser(inputData)
        
            redisDataHandler(roomOccupancy, redis_cache)
        else:
            time.sleep(.5)