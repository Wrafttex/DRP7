from paho.mqtt import client as mqtt_client
import socket
# ipaddd = socket.gethostbyname("mosquitto")
broker = "mosquitto"
port = 1883
topic = "espresense/rooms/+"
username = "TestUser"
password = "TestPassword"
clientID = "HubSubcribe"

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(clientID)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        f = open("./data.txt", "a")
        #print([msg.payload.decode(), msg.topic])
        f.write(str(msg.payload.decode())[:-1] + ", 'roomId': '" + str(msg.topic) + "'}" + "\n")
        f.close()
        return msg.payload.decode()

    client.subscribe(topic)
    client.on_message = on_message
    

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_start()

if __name__ == '__main__':
    run()