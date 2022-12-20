#! c:\python34\python3
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
import signal
import time
import paho.mqtt.client as paho
##edit these settings
broker="192.168.1.82"
port=1883
blocks=50 #edit for number of blocks
messages=200 #edit for messages per block
message_size=1000 #edit for size of message
M_delay=0.00001 #delay between messages
Loop_delay=2
inject_error=False
error_block=3 #put error in this block
pub_topic="v3/test"
#inject_error=True
### end edit
#broker="test.mosquitto.org"
#define callback
def on_message(client, userdata, message):
   print(str(message.payload.decode("utf-8")))
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK")
        client.subscribe("tests/results")
    else:
        print("Bad connection Returned code=",rc)


cname="tx-client-"+str(int(time.time()))
client= paho.Client(cname)
#assign function to callback                                 #establish connection client1.publish("house/bulb1","on")  
######
client.connected_flag=False
client.on_message=on_message
client.on_connect=on_connect
#####
print("connecting to broker ",broker)
client.connect(broker,port)#connect
client.loop_start()
while not client.connected_flag:
   time.sleep(.1)
print("subscribing ")
client.subscribe("test/results")#subscribe
print("publishing ")
count=1
message_rate=0
loop_count=0

BC=str(blocks).rjust(6,"0")
MS=str(messages).rjust(6,"0")
BS=str(message_size).rjust(6,"0")
ST="STARTXXX"
ET="ENDXXXXX"
SB="X"*8
EB="Z"*8
DL="YY"
header=""


msg="!"*message_size
header=ST+BC+MS+BS
client.publish(pub_topic,header)#publish
while loop_count<blocks:
   #print("pub loop")
   stime=time.time()
   client.publish(pub_topic,SB)#publish
   for count in range(1,messages+1):
      client.loop(.0001)
      c=str(count).rjust(6,"0")
      l=str(loop_count).rjust(6,"0")
      mro=str(int(message_rate)).rjust(6,"0")
      header= c+DL+l+DL+MS+DL+mro+DL
      header=header.ljust(40,"P")
      message=header+ msg
      if loop_count==4 and inject_error:
         if count==error_block:
            print ("publishing error ")
            continue
      client.publish(pub_topic,message)#publish
      time.sleep(M_delay)
      message=""
   client.publish(pub_topic,EB)#publish
   time_taken=time.time()-stime
   print("Time taken = %.3f " %time_taken)
   message_rate=messages/time_taken
   print("message rate %.3f " %message_rate," messages per second")
   message_rate=messages*message_size/time_taken
   print("message rate %.3f" %message_rate," Bytes per second")

   time.sleep(Loop_delay)
   count=0
   loop_count+=1
   
client.publish(pub_topic,ET)#publish
time.sleep(20)
client.disconnect() #disconnect
client.loop_stop() #stop loop
