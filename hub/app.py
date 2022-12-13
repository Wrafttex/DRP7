import redis
from flask import Flask, render_template, request
from flask_cors import CORS
from mainspiffs import mainspiffs
from frontpagelayout import espdivLayout
app = Flask(__name__)
from threading import Thread
CORS(app)
redis_cache = redis.Redis(host="redis",port=6379,decode_responses=True)

def defaultsettings(dictonary):
    for key in list(dictonary.keys()):
        if dictonary[key] == "":
            dictonary[key]=redis_cache.get(key)
    return dictonary

  
dicttesting =  {
    "RoomOccupancy": [
        {"ESPId":"testId0","Occupants":2,"TimeSinceLast": None},
        {"ESPId":"testId1","Occupants":3,"TimeSinceLast": None},
        {"ESPId":"testId2","Occupants":1,"TimeSinceLast": None},
        {"ESPId":"testId3","Occupants":5,"TimeSinceLast": None},
        {"ESPId":"testId4","Occupants":0,"TimeSinceLast": "13:50"},
        {"ESPId":"testId5","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId6","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId7","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId8","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId9","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId10","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId11","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId12","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId13","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId14","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId15","Occupants":0,"TimeSinceLast": "14:15"},
        {"ESPId":"testId16","Occupants":0,"TimeSinceLast": "14:15"},
    ]
}

redis_cache.json().set('room',".",dicttesting)
##Thread(target=HubController.test).start
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

def nonetoempty(obj):
    emptylist = []
    for local in obj:
        if local == None:
            emptylist.append("")
        else:
            emptylist.append(local)
    return emptylist


@app.route("/esp_flash")
def esp_flash():
    return render_template("flash.html",espdata=nonetoempty(redis_cache.mget("ssid","wifi_pass","mqtt_host","mqtt_port","mqtt_user","mqtt_pass")))


@app.route("/customdata",methods=["POST","GET"])
def customdata():
    espdata = request.form.to_dict()
    # espdata=defaultsettings(dictonary=espdata)
    mainspiffs(espdata["room_name"],espdata["ssid"],espdata["wifi_pass"],espdata["mqtt_host"],espdata["mqtt_port"],espdata["mqtt_user"],espdata["mqtt_pass"])
    return espdata,200


@app.route("/")
def index():
    print("testing")
    roomjson = redis_cache.json().get("room")
    return render_template("index.html",esp=espdivLayout(roomjson))


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


if __name__ == "__main__":
    #runConnect()
    app.run(debug=True)
    
