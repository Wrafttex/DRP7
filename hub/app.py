import redis
from flask import Flask, render_template, request
from flask_cors import CORS
from mainspiffs import mainspiffs
from frontpagelayout import espdivLayout
app = Flask(__name__)
CORS(app)
redis_cache = redis.Redis(host="redis",port=6379,decode_responses=True)

def defaultsettings(dictonary):
    for key in list(dictonary.keys()):
        if dictonary[key] == "":
            tempvalue = redis_cache.get(key)
            if tempvalue == None:
                dictonary[key]=""
            else:
                dictonary[key]=tempvalue
    return dictonary

broker = "localhost"
port = 1883
topic = "test/topic"
username = "TestUser"
password = "TestPassword"
clientID = "HubSubcribe"

@app.route("/updatedb",methods=["POST"])
def updatedb():
    if request.method == "POST":
        room_name = request.form.to_dict()
        print(room_name)
        jsondata = redis_cache.json().get("room")
        print(jsondata)
        for index in range(len(jsondata["RoomOccupancy"])):
            print(jsondata["RoomOccupancy"][index]["ESPId"])
            if jsondata["RoomOccupancy"][index]["ESPId"] == room_name["room_name"]:
                jsondata["RoomOccupancy"].pop(index)
                print("poped",jsondata["RoomOccupancy"])
                redis_cache.json().set('room',".",jsondata)
                
                break
        
    return "succes",200

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
    espdata = defaultsettings(espdata)
    mainspiffs(espdata["room_name"],espdata["ssid"],espdata["wifi_pass"],espdata["mqtt_host"],espdata["mqtt_port"],espdata["mqtt_user"],espdata["mqtt_pass"])
    return espdata,200


@app.route("/")
def index():
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
    app.run(debug=True)
    
