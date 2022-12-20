#! c:\python34\python3
#!/usr/bin/env python
##demo code provided by Steve Cope at www.steves-internet-guide.com
##email steve@steves-internet-guide.com
##Free to use for any purpose
##If you like and use this code you can
##buy me a drink here https://www.paypal.me/StepenCope
import signal

import time,random
import paho.mqtt.client as paho

broker="192.168.1.64"
port=1883
username = "TestUser"
password = "TestPassword"
#broker="test.mosquitto.org"
#define callback
def on_message(client, userdata, message):
   m=str(message.payload.decode("utf-8"))
   #print("received message =",m)
   message_handler(message.topic,m)
def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("subscribing")
        client.subscribe("v3/#")#subscriclient.blocks_expected
        client.connecting=False
        print("connected OK")
    else:
        print("Bad connection Returned code=",rc)
def on_disconnect(client, userdata, flags, rc=0):
    #print("DisConnected with flags",str(flags),"result code "+str(rc)+"client id  "+str(client))
    client.connected_flag==False
def update_status():
   client.start_flag=False
   interval=time.time()-client.start_time
   print(f"messages Received {client.rx_count}")
   print(f"time taken {interval:.3f}")
   b_rate=(int(client.rx_message_size)*client.rx_count)/interval
   
   print(f"{b_rate:.3f} Bytes/second")
   try:
      print(f"messages received/s {(client.rx_count/interval):.3f}")
   except:
      pass
   if client.block_count!=client.send_block_count:
      client.error_flag=True
      print(f"Block expected {client.block_count} Got {client.send_block_count}")
   client.block_count+=1

   if  client.error_flag:
      print(f"errors in block {client.block_count}")
      client.error_blocks+=1
   print(f"received {client.block_count} blocks with {client.error_blocks} block errors")
   #print(client.rx_message_size,"message size")
   client.error_flag=False #reset
   client.last_rx_message=0
   client.rx_count = 0 #reset
   print("----------------")
def show_results(msg):
   print(msg)
   client.publish("test/results",msg)


def test_summary():
   show_results("Ending test")
   if client.error_blocks!=0:
      show_results(str(client.error_blocks) +" errors detected")
   if client.blocks_expected==client.block_count and client.error_blocks==0:
   
      show_results("test successful blocks sent "+str(client.blocks_expected)+\
                   " blocks received "+\
            str(client.block_count))
   else:
      show_results("test failed sent "+str(client.blocks_expected)+" blocks received "+\
            str(client.block_count)+" blocks in error "+str(client.error_blocks))
         
   print("+++++++++++++++++++++")
            

def message_handler(topic,msg):
   
   m=msg[:40]
   if msg[:8]==ST:
      client.blocks_expected=int(msg[8:14])
      client.messages_expected=int(msg[15:20])
      client.rx_message_size=int(msg[21:26])
      print("==================")
      print("Starting New Test")
      print("Expecting ",client.messages_expected, " messages in blocks")
      print("Message size= ",int(client.rx_message_size),"bytes")
      print("==================")

      return
   if msg[:8]==ET:
      test_summary()
      init_counters() #reset for new start
      return
   if msg==SB:
      client.start_flag=True
      client.start_time = time.time()
      client.block_flag=False
      return
   if msg[:8]==EB:
      update_status()
      client.start_flag=False
      return
   if client.start_flag:
      if len(m)<40:
         print("Message garbled ",m)
         client.error_flag=True
         return
      s= m.split(DL)
      mcount=int(s[0])
      client.send_block_count=int(s[1])
      if client.send_block_count==0:
         client.block_count=0 #reset block count
      client.rx_block_size=s[2]
      client.send_rate=s[3]
         
      client.rx_count+=1
      client.rx_message_expected=client.last_rx_message+1
      if mcount!=client.rx_message_expected:
         print("Error expected =",client.rx_message_expected, "got ",mcount)
         client.error_flag=True
      client.last_rx_message=mcount
      client.time_last_message=time.time()
             
      
def init_counters():

   client.rx_count=0
   client.rx_rate=0
   client.send_rate=0
   client.rx_loop_count=0
   client.rx_block_size=0
   client.start_flag=False
   client.error_flag=False
   client.error_blocks=0
   client.start_time=0
   client.last_rx_message=0
   client.rx_message_expected=0
   client.block_count=0
   client.block_flag=False
   client.blocks_expected=0
   client.time_last_message=time.time()

cname="rx-client-"+str(int(time.time()))
client= paho.Client(cname)  #create client object client1.on_publish = on_publish                          #assign function to callback client1.connect(broker,port)                                 #establish connection client1.publish("house/bulb1","on")  
######
if username != "":
   client.username_pw_set(username, password)
client.connected_flag=False
client.on_message=on_message
client.on_connect=on_connect
client.on_disconnect=on_disconnect
#####

client.connecting=False
init_counters()
###############
print("Starting Press CTRL+C to Stop")
print("connecting to broker ",broker)
client.connect(broker,port)#connect
client.run_flag=True
ST="STARTXXX"
ET="ENDXXXXX"
SB="X"*8
EB="Z"*8
DL="YY"
header=""
client.loop_start()
try:
   while client.run_flag:
      time.sleep(.1)
      if not client.connected_flag:
         print("Receive failed quitting")
         client.run_flag=False
         client.loop_stop()
except KeyboardInterrupt:
   print("Stopping")
   client.run_flag=False
   client.loop_stop()
         
time.sleep(4)
client.disconnect() #disconnect


