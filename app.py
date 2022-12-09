import redis
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
#from flask_mqtt import Mqtt
from paho.mqtt import client as mqtt_client
from mainspiffs import mainspiffs
import json
app = Flask(__name__)
CORS(app)
redis_cache = redis.Redis(host="redis",port=6379,decode_responses=True)

def defaultsettings(dictonary):
    for key in list(dictonary.keys()):
        if dictonary[key] == "":
            dictonary[key]=redis_cache.get(key)
    return dictonary

def espGridLayout():
    tableclass ="table table-hover"
    thscope = "<th scope=\"col\">"
    startlayout = f" <table class=\"{tableclass}\"> <thead> <tr> {thscope}ESP Name</th> {thscope}Occupancy detection</th></tr></thead><tbody>"
    roomjson = redis_cache.json().get("room")
    for index in range(len(roomjson["RoomOccupancy"])):
        buttonlayout = f"<tr><th scope=\"row\"><button type=\"button\" data-toggle=\"modal\" data-target=\"#Modal{roomjson['RoomOccupancy'][index]['ESPId']}\" class=\"btn btn-light\">{roomjson['RoomOccupancy'][index]['ESPId']}</button>"
        occuchecker = roomjson['RoomOccupancy'][index]["Occupants"]>0
        occulayout = f"</th><td>{occuchecker!s}</td></tr>"
        startlayout = f"{startlayout} {buttonlayout} {occulayout}"
    startlayout = f"{startlayout}  </tbody> </table>"
    for index in range(len(roomjson["RoomOccupancy"])):
        startmodallayout = f"<div class=\"modal fade\" id=\"Modal{roomjson['RoomOccupancy'][index]['ESPId']}\" tabindex=\"-1\" role=\"dialog\" aria-labelledby=\"Modal{roomjson['RoomOccupancy'][index]['ESPId']}Title\" aria-hidden=\"true\">"    
        headmodallayout = f"<div class=\"modal-dialog modal-dialog-centered\" role=\"document\"> <div class=\"modal-content\"> <div class=\"modal-header\"> <h5 class=\"modal-title\" id=\"Modal{roomjson['RoomOccupancy'][index]['ESPId']}Title\">{roomjson['RoomOccupancy'][index]['ESPId']}</h5> <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button></div>"
        bodymodalstarterlayout = f"<div class=\"modal-body\"><table class=\"table\"><thead><tr><th scope=\"col\">param</th><th scope=\"col\">Value</th></tr></thead><tbody>"
        
        for contentkey in roomjson["RoomOccupancy"][index].keys():
            bodymodalcontentlayout = f"<tr><th scope=\"row\">{contentkey}</th><td>{roomjson['RoomOccupancy'][index][contentkey]}</td></tr><tr>"
            bodymodalstarterlayout = f"{bodymodalstarterlayout} {bodymodalcontentlayout}"
        footermodallayout = f"</tbody></table></div><div class=\"modal-footer\"></div></div></div></div>"
        startlayout = f"{startlayout} {startmodallayout} {headmodallayout} {bodymodalstarterlayout} {footermodallayout}"
    
    return startlayout   

  
dicttesting =  {
    "RoomOccupancy": [
        {"ESPId":"testId0","Occupants":2,"TimeSinceLast": None},
        {"ESPId":"testId1","Occupants":3,"TimeSinceLast": None},
        {"ESPId":"testId2","Occupants":1,"TimeSinceLast": None},
        {"ESPId":"testId3","Occupants":5,"TimeSinceLast": None},
        {"ESPId":"testId4","Occupants":0,"TimeSinceLast": "13:50"},
        {"ESPId":"testId5","Occupants":0,"TimeSinceLast": "14:15"}
    ]
}

redis_cache.json().set('room',".",dicttesting)
print(redis_cache.json().get("room")) 
print(len(redis_cache.json().get("room")["RoomOccupancy"]),len(dicttesting["RoomOccupancy"][0].keys()))  
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

@app.route("/imagedata",methods=["GET","POST"])
def data():
    if request.method == "POST":
        a =request.get_json()
        return a,200
    if request.method == "GET":
        return {"test":"hello"}
    return "okay",200
@app.route("/esp_flash")
def esp_flash():
    return render_template("flash.html")

@app.route("/testingurl",methods=["POST"])
def testingurl():
    espdata = request.form.to_dict()
    print(espdata)
    espdata=defaultsettings(dictonary=espdata)
    print(espdata)
    mainspiffs(espdata["ssid"],espdata["wifi_pass"],espdata["mqtt_host"],espdata["mqtt_port"],espdata["mqtt_user"],espdata["mqtt_pass"])
    return espdata,200

@app.route("/esp_base")
def esp_base():
    return render_template("base_flash.html")

@app.route("/")
def home():
    return render_template("home.html", topic=topic, publications="")

@app.route("/index")
def index():
    return render_template("index.html",esp=espGridLayout())

@app.route("/setting",methods=["GET","POST"])
def settings():
    if request.method == "GET":
        return render_template("settings.html")
    
@app.route("/settingsSave",methods=["POST"])
def settingsSave():
    if request.method == "POST":
        MQTT_Data = request.form.to_dict()
        redis_cache.mset(MQTT_Data)
        return "Settings saved",200
    



#TODO Get SSL to work
if __name__ == "__main__":
    #runConnect()
    app.run(debug=True)
    