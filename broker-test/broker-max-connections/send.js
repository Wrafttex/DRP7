#! /usr/bin/env node

var mqtt = require('mqtt')
var client = mqtt.connect({ port: 1883, host: '192.168.1.157', clean: true, keepalive: 0 })
var loops=2;
var loop_count=0;
var sent = 0;
var interval = 5000;
var delay=100;
var pub_flag=1;
var start_time=0;

function sleep(milliSeconds) {
//console .log("sleeping ",sent);
 var startTime = new Date().getTime();
 while (new Date().getTime() < startTime + milliSeconds)
	 ;
 }


function count () {
  console.log('sent/s', sent / interval * 1000)
  console.log("sent =",sent);
  sent = 0
  loop_count++;
  if (loop_count>loops){
	  console.log("quitting");
	  clearInterval(timer_id);
	  client.end();
	  process.exit(0);
	  pubflag=0;
	  
  }
}



function immediatePublish () {
  setImmediate(publish)
}

function publish () {
//if (sent==45){ //inject error
//	sent=46;
//}
var end_flag=0;
if (sent==0){
	start_time=new Date().getTime();
}
//console.log("in publish",end_flag);
if (new Date().getTime()-start_time>=interval){
	end_flag=1;

}
s=sent.toString();

l=s.length;
l_out=6;
for(i=0;i<l_out-l;i++){
s="0"+s;
}

payload=s;
//console.log(s);

if (pub_flag==1){
	if (end_flag==1){
		client.publish('test', "999999", immediatePublish)
		console.log('sent/s', sent / interval * 1000)
		console.log("sent =",sent);
		sent=0;
		pub_flag=1;
		end_flag=0; //reset
		
	}
	else{ 
		client.publish('test', payload, immediatePublish)
		sent++
	}
sleep(delay);
}

}



client.on('connect', publish);

client.on('offline', function () {
  console.log('offline');
})

client.on('error', function () {
  console.log('reconnect!');
  client.stream.end();
})
//var timer_id=setInterval(count, interval);
