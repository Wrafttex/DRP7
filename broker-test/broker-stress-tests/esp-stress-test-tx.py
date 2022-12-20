#! c:\python34\python3
#!/usr/bin/env python
import signal
import time
import json
import random
import paho.mqtt.client as paho
# edit these settings
broker = "192.168.1.64"
port = 1883
blocks = 25  # edit for number of blocks
messages = 200  # edit for stress messages per block (total msg = messages+(messages*esps))
message_size = 1  # edit for size of message
M_delay = 0.00001  # delay between messages
Loop_delay = 2
pub_topic = "v3/test"

esps = 200
bles = 500
esp_topic = "espresense/rooms"
total_msg = messages+(messages*esps)
username = "TestUser"
password = "TestPassword"
# end edit


def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.connected_flag = True  # set flag
        print("connected OK")
        client.subscribe("tests/results")
    else:
        print("Bad connection Returned code=", rc)


def stress_msg():
    c = str(count).rjust(6, "0")
    l = str(loop_count).rjust(6, "0")
    mro = str(int(message_rate)).rjust(6, "0")
    header = c+DL+l+DL+MS+DL+mro+DL
    header = header.ljust(40, "P")
    message = header + msg
    client.publish(pub_topic, message)  # publish
    message = ""


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
    esp_macs.append(rand_mac())

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

BC=str(blocks).rjust(6, "0")
MS=str(messages).rjust(6, "0")
BS=str(message_size).rjust(6, "0")
ST="STARTXXX"
ET="ENDXXXXX"
SB="X"*8
EB="Z"*8
DL="YY"
header=""


msg="!"*message_size
header=ST+BC+MS+BS
client.publish(pub_topic, header)  # publish
while loop_count < blocks:
    # print("pub loop")
    stime=time.time()
    client.publish(pub_topic, SB)  # publish
    for count in range(1, messages+1):
        #client.loop(.001)
        stress_msg()
        #time.sleep(M_delay)
        for esp_name in esp_macs:
            esp_msg(esp_name)
            #time.sleep(M_delay)

    client.publish(pub_topic, EB)  # publish
    time_taken=time.time()-stime
    print(f"Time taken = {time_taken:.3f} ")
    message_rate=total_msg/time_taken
    print(f"message rate {message_rate:.3f} messages per second")
    message_rate=((messages*message_size)+(messages*esp_message_size))/time_taken
    print(f"message rate {message_rate:.3f} Bytes per second")

    time.sleep(Loop_delay)
    count=0
    loop_count += 1

client.publish(pub_topic, ET)  # publish
time.sleep(20)
client.disconnect()  # disconnect
client.loop_stop()  # stop loop
