from paho.mqtt import client as mqtt_client
import time

broker = "localhost"
port = 1883
topic = "espresense/rooms/BleTestDevice2"
username = "TestUser"
password = "TestPassword"
clientID = "BleTestDevice"

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

def publish(client, msg):
    while True:
        time.sleep(0.5)
        result = client.publish(topic, msg)
        status = result[0]
        if status == 0:
            print(f"Send `{msg}` to topic `{topic}`")
        else:
            print(f"Failed to send message: {msg} to topic {topic}")

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client, str({"id":"244b03d72780","idType":55,"rssi@1m":-71,"rssi":-84,"raw":2.35,"distance":2.25,"speed":0.02,"mac":"244b03d72780","interval":615}))

if __name__ == '__main__':
    run()