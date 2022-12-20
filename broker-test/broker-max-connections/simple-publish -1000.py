import paho.mqtt.client as mqtt
import time
import json
broker="192.168.1.157"
broker="raspberrypi.home"
#broker="216.10.243.185"
#broker="broker.hivemq.com"
#broker="iot.eclipse.org"
#broker="test.mosquitto.org"
#broker="mqtt.thingspeak.com"
#port =1883
port=8883 #ssl
keepalive=1800
def on_log(client, userdata, level, buf):
   print(buf)
def on_message(client, userdata, message):
   time.sleep(1)
   print("message received",str(message.payload.decode("utf-8")))
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        #print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
        client.loop_stop()  
def on_disconnect(client, userdata, rc):
   pass
   #print("client disconnected ok")
def on_publish(client, userdata, mid):
   time.sleep(1)
   print("In on_pub callback mid= "  ,mid)

mqtt.Client.connected_flag=False#create flag in class
clients=[]
nclients=1000
print("Stating to connect ",nclients," clients")
for i in range(nclients):
   cname ="python-"+str(i)
   client = mqtt.Client(cname)             #create new instance
   client.tls_set('c:/python34/steve/MQTT-demos/certs/ca-pi.crt')
   client.connect(broker,port,keepalive)           #establish connection
   #client.on_log=on_log #this gives getailed logging
   client.on_connect = on_connect
   client.on_disconnect = on_disconnect
   #client.on_publish = on_publish
   client.on_message = on_message
   clients.append(client)
   while not client.connected_flag:
      client.loop()
      time.sleep(0.05)


topic="house/sensor1"
#topic="channels/358781/publish/BJKZEY6TEB4GTHZG"
print("All clients connected ")

#
count =0
print("Publishing ")
for client in clients:
   client.loop()
   msg="message "+str(count)
   client.publish(topic,msg)
   time.sleep(0.01)

time.sleep(3600)
#client.loop_stop() #stop loop
for client in clients:
   client.disconnect()


