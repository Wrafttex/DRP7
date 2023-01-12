import time
import pytz
import redis
import DataProcesser
from queue import Queue
from threading import Thread
from datetime import datetime
import mqttTools.puplish as Pub
import mqttTools.subscribe as Sub

def checkRooms(redis_cache):
    currentData = redis_cache.json().get("room")
    if currentData != None:
        currentTime = datetime.strptime(datetime.now(pytz.timezone('Europe/Copenhagen')).strftime("%H:%M:%S"), "%H:%M:%S")
        for row in currentData["RoomOccupancy"]:
            espId = row["ESPId"]
            dTime = currentTime - datetime.strptime(row["TimeSinceLast"], "%H:%M:%S")
            
            if dTime.total_seconds() >= 5:
                row.update({"Occupants": 0})
                Pub.publish("False", f"{espId}/occupancy")
            else:
                Pub.publish("True", f"{espId}/occupancy")

        redis_cache.json().set("room", ".", currentData)
    else:
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