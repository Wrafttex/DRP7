import redis
from flask import Flask, render_template, request
from flask_cors import CORS
from mainspiffs import mainspiffs
from frontpagelayout import espgridLayout
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
        # print(room_name)
        json_data = redis_cache.json().get("room")
        # print(json_data)
        for index in range(len(json_data["RoomOccupancy"])):
            # print(json_data["RoomOccupancy"][index]["ESPId"])
            if json_data["RoomOccupancy"][index]["ESPId"] == room_name["room_name"]:
                json_data["RoomOccupancy"].pop(index)
                # print("poped",json_data["RoomOccupancy"])
                redis_cache.json().set('room',".",json_data)
                
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
    empty_list = []
    for local in obj:
        if local == None:
            empty_list.append("")
        else:
            empty_list.append(local)
    return empty_list


@app.route("/esp_flash")
def esp_flash():
    return render_template("flash.html",espdata=nonetoempty(redis_cache.mget("ssid","wifi_pass","mqtt_host","mqtt_port","mqtt_user","mqtt_pass")))


@app.route("/customdata",methods=["POST","GET"])
def customdata():
    esp_data = request.form.to_dict()
    esp_data = defaultsettings(esp_data)
    mainspiffs(esp_data["room_name"],esp_data["ssid"],esp_data["wifi_pass"],esp_data["mqtt_host"],esp_data["mqtt_port"],esp_data["mqtt_user"],esp_data["mqtt_pass"])
    return esp_data,200


@app.route("/")
def index():
    roomjson = redis_cache.json().get("room")
    return render_template("index.html",esp=espgridLayout(roomjson))


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
    
