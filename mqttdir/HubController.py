import time
import sys
import redis
import DataProcesser
from queue import Queue
from threading import Thread
import mqttTools.puplish as Pub
import mqttTools.subscribe as Sub

def checkRooms(redis_cache):
    while True:
        currentData = redis_cache.json().get("room")
        if currentData != None:
            currentTime = time.time()
            for row in currentData["RoomOccupancy"]:
                espTopic = row["ESPId"]
                espId = espTopic.split('/')[2]

                dTime = currentTime - row["TimeSinceLast"]
                
                if dTime >= 5:
                    row.update({"Occupants": 0})
                    Pub.publish("False", f"{espTopic}/occupancy")
                    Pub.publish("off", f"cmnd/{espId}/POWER")
                else:
                    Pub.publish("True", f"{espTopic}/occupancy")
                    Pub.publish("on", f"cmnd/{espId}/POWER")

            redis_cache.json().set("room", ".", currentData)
        
        time.sleep(4)

def run():
    dataQueue = Queue()
    redis_cache = redis.Redis(host="redis",port=6379,decode_responses=True)

    Sub.run(dataQueue)
    Pub.run()

    t1 = Thread(target=DataProcesser.processData, args=(dataQueue,redis_cache,))
    t2 = Thread(target=checkRooms, args=(redis_cache,))
    t1.start()
    t2.start()

if __name__ == '__main__':
    run()