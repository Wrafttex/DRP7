#! /usr/bin/env node

var mqtt = require('mqtt')

var client = mqtt.connect({ port: 1883, host: '192.168.1.157', clean: true, encoding: 'binary', keepalive: 0 })
var counter = 0
//var interval = 5000
var last_message=0;
var start_flag=0;
var start_time=0;
function count (interval) {
  console.log('received/s', counter / interval * 1000)
  counter = 0
}

//setInterval(count, interval)

client.on('connect', function () {
  //count();
  this.subscribe('test')
  this.on('message', function (topic,message,packet) {
	  //console.log("message ="+message);
	  var count =parseInt(message);
	  var expected=last_message+1;
	  if (count==999999 || count==0){
		var end_time= new Date().getTime()
		if (start_time!=0 && count ==999999)
		{
		var interval=end_time-start_time
		console.log('received/s', expected / interval * 1000," count ",expected)
		counter = 0
		}
		if (count==0){
		console.log("starting message is ="+message);
		last_message=count;
		start_flag=1;
		start_time = new Date().getTime();
		}
	  }

	  else{
		  if (start_flag==1 && count!=0){
	
		  if (count!=expected && count!=999999){
			console.log("Error expected =",expected, "got ",count);
			//start_flag=0;			
		  }
		  last_message=count;
		  }
		
	  }
    counter++
  })
})
