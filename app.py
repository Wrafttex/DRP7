import redis
from flask import Flask, render_template, request, jsonify
#from flask_mqtt import Mqtt
from paho.mqtt import client as mqtt_client

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)
#app.config['MQTT_BROKER_URL'] = "localhost"
#app.config['MQTT_BROKER_PORT'] = 1883
#app.config['MQTT_USERNAME'] = "TestUser"
#app.config['MQTT_PASSWORD'] = "TestPassword"
#app.config['MQTT_KEEPALIVE'] = 5
#app.config['MQTT_TLS_ENABLED'] = False

#mqtt_client = Mqtt(app)

broker = "localhost"
port = 1883
topic = "test/topic"
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
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        publish_message(msg.payload.decode())

    client.subscribe(topic)
    client.on_message = on_message

def runConnect():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


@app.route("/updatePublications", methods=["POST"])
def publish_message(msg):
   return jsonify("", render_template("updatePublications.html", publications=msg))

@app.route("/imagetesting",methods=["GET","POST"])
def imagetest():
    return render_template("imagetesting.html")

@app.route("/imagedata",methods=["POST","GET"])
def data():
    print("test")
    f = open("test.txt","w")
    a =request.get_json()
    f.write(str(a["imgpixel"]["px"]))
    f.close()
    print(request.get_json())
    # df = pd.read_json()
    # df.to_json("test.csv")
    return str(a["imgpixel"]["px"]),200  

@app.route("/")
def home():
    return render_template("home.html", topic=topic, publications="")

if __name__ == "__main__":
    #runConnect()
    app.run(debug=True)