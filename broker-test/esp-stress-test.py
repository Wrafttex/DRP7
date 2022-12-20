#! c:\python34\python3
#!/usr/bin/env python
import time
import json
import random
import paho.mqtt.client as paho
# edit these settings
broker = "localhost"
port = 1883
blocks = 5  # edit for number of blocks
messages = 1  # edit for stress messages per block (total msg = messages+(messages*esps))
message_size = 1  # edit for size of message
M_delay = 0.00001  # delay between messages
Loop_delay = 10

esps = 200
bles = 500
esp_topic = "espresense/rooms"
ocupy_topic = "espresense/rooms/+/occupancy"
total_msg = messages*esps
username = "TestUser"
password = "TestPassword"
# end edit
message_log = {}
message_delay = []

def on_message(client, userdata, message):
    if message.topic == "tests/results":
        print(str(message.payload.decode("utf-8")))
    else:
        recive_time = time.time()
        device_id = message.topic.split("/")[2]
        if device_id in esp_macs and str(message.payload.decode("utf-8")) == "True":
            delay = recive_time - message_log[device_id]["sendt"]
            time_taken=int(delay*1000) # in ms
            message_log[device_id]["delay"] = time_taken
            message_delay.append(time_taken)


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
        client.subscribe("tests/results")
        client.subscribe(ocupy_topic)
    else:
        print("Bad connection Returned code=", rc)


def rand_mac():
    mac = [0x00, 0x24, 0x81,
           random.randint(0x00, 0x7f),
           random.randint(0x00, 0xff),
           random.randint(0x00, 0xff)]

    return ':'.join(map(lambda x: "%02x" % x, mac))


def esp_msg(esp_name):
    # {"id":"bc7e8b2e9a71","idType":55,"rssi@1m":-71,"rssi":-95,"raw":4.85,"distance":5.18,"speed":-0.02,"mac":"bc7e8b2e9a71","interval":2800}
    mac = random.choice(ble_macs)
    message = json.dumps({
                    "id": mac,
                    "idType": random.choice([15, 20, 40, 55]),
                    "rssi@1m": -71,
                    "rssi": random.randint(-95, -53),
                    "raw": random.randint(0, 4)+random.random(),
                    "distance": random.randint(0, 5)+random.random(),
                    "speed": -0.02,
                    "mac": mac,
                    "interval": random.randint(300, 3000)})
    client.publish(esp_topic+"/"+esp_name, message)  # publish

esp_macs = []
for i in range(esps):
    name = rand_mac().replace(":","")
    esp_macs.append(name)
    message_log[name] = {"sendt": 0, "delay": 0}

ble_macs = []
for i in range(bles):
    ble_macs.append(rand_mac())

esp_message_size = len('{"id":"bc7e8b2e9a71","idType":55,"rssi@1m":-71,"rssi":-95,"raw":4.85,"distance":5.18,"speed":-0.02,"mac":"bc7e8b2e9a71","interval":2800}'.encode('utf-8'))

cname="tx-client-"+str(int(time.time()))
client=paho.Client(cname)
# assign function to callback                                 #establish connection client1.publish("house/bulb1","on")
######
if username != "":
   client.username_pw_set(username, password)
client.connected_flag=False
client.on_message=on_message
client.on_connect=on_connect
#####
print("connecting to broker ", broker)
client.connect(broker, port)  # connect
client.loop_start()
while not client.connected_flag:
    time.sleep(.1)
print("subscribing ")
client.subscribe("test/results")  # subscribe
print("publishing ")
count=1
message_rate=0
loop_count=0

while loop_count < blocks:
    stime=time.time()
    for count in range(0, messages):
        for esp_name in esp_macs:
            if count == 0:
                message_log[esp_name]["sendt"] = time.time()
            esp_msg(esp_name)

    time_taken=(time.time()-stime)+0.00000000001

    wait = 0
    while len(message_delay) < esps and wait < 20:
        wait += 1
        time.sleep(1)
    
    print(f"Time taken = {time_taken:.3f} ")
    message_rate=total_msg/time_taken
    print(f"message rate {message_rate:.3f} messages per second")
    message_rate=((messages*message_size)+(messages*esp_message_size))/time_taken
    print(f"message rate {message_rate:.3f} Bytes per second")
    try:
        print(f"messages recived: {len(message_delay)}")
        print(f"Max Time: {max(message_delay)} ms")
        print(f"Mix Time: {min(message_delay)} ms")
        print(f"Avg Time: {sum(message_delay)/len(message_delay)} ms")
    except:
        pass

    message_delay = []
    for esp_name in esp_macs: 
        message_log[esp_name] = {"sendt": 0, "delay": 0}

    time.sleep(Loop_delay)
    count=0
    loop_count += 1

time.sleep(20)
client.disconnect()  # disconnect
client.loop_stop()  # stop loop
