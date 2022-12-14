import pandas as pd

def dataProcesser(data, roomDictionary):
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