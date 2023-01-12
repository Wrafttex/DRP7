from paho.mqtt import client as mqtt_client
from queue import Queue

broker = "mosquitto"
port = 1883
topic = "espresense/rooms/+"
username = "TestUser"
password = "TestPassword"
clientID = "HubSubcribe"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def on_message_old(client, userdata, msg):
    f = open("./data.txt", "a")
    f.write(str(msg.payload.decode())[:-1] + ", 'roomId': '" + str(msg.topic) + "'}" + "\n")
    f.close()
    return msg.payload.decode() 

def on_message(client, userdata, msg):
    userdata["dataQueue"].put(str(msg.payload.decode())[:-1] + ", 'roomId': '" + str(msg.topic) + "'}" + "\n")
    return msg.payload.decode() 

def run(dataQueue: Queue):
    client = mqtt_client.Client(clientID, userdata={"dataQueue": dataQueue})
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.connect(broker, port)
    client.subscribe(topic)
    
    client.loop_start()
    

if __name__ == '__main__':
    run()