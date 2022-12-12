import redis
from flask import Flask, render_template, request, jsonify
from flask_mqtt import Mqtt
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


@app.route("/updatePublications", methods=["POST"])
def publish_message(msg):
   return jsonify("", render_template("updatePublications.html", publications=msg))

@app.route("/")
def home():
    return render_template("home.html", topic=topic, publications="")

if __name__ == "__main__":
    app.run(debug=True)