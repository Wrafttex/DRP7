from paho.mqtt import client as mqtt_client

broker = "mosquitto"
port = 1883
username = "TestUser"
password = "TestPassword"
clientID = "BleTestDevice"
client = mqtt_client.Client(clientID)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("pub connected to MQTT Broker!")
    else:
        print("Failed to connect, return code %d\n", rc)

def publish(msg, topic):
        result = client.publish(topic, msg)
        status = result[0]
        if status != 0:
            print(f"Failed to send message: {msg} to topic {topic}")

def run():
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    
    client.connect(broker, port)
    client.loop_start()

if __name__ == '__main__':
    run()