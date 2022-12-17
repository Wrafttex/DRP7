from mqttdir import HubController 

testData = [{'id': '244b03d72780', 'idType': 55, 'rssi@1m': -71, 'rssi': -84, 'raw': 2.35, 'distance': 2.25, 'speed': 0.02, 'mac': '244b03d72780', 'interval': 615, 'roomId': 'test/topic'},
            {"id":"msft:cdp:0922","idType":40,"rssi@1m":-71,"rssi":-40,"raw":0.94,"distance":0.51,"speed":0.02,"mac":"3c690ee96a82","interval":312, 'roomId': 'test/topic/2'},
            {"id":"244b03d72780","idType":55,"rssi@1m":-71,"rssi":-23,"raw":2.35,"distance":2.25,"speed":0.02,"mac":"244b03d72780","interval":615, 'roomId': 'test/topic/2'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-54,"raw":0.33,"distance":0.35,"speed":-0.00,"mac":"55959568c9b6","interval":746, 'roomId': 'test/topic'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-82,"raw":2.06,"distance":2.17,"speed":-0.01,"mac":"7422e97424d0","interval":813, 'roomId': 'test/topic'},
            {"id":"md:0901:12","idType":20,"rssi@1m":-71,"rssi":-85,"raw":2.51,"distance":3.29,"speed":-0.05,"mac":"74812d6dada3","interval":2022, 'roomId': 'test/topic'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-90,"raw":3.49,"distance":3.19,"speed":0.04,"mac":"4949491706f1","interval":1305, 'roomId': 'test/topic'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-81,"raw":1.93,"distance":1.96,"speed":-0.00,"mac":"5434446b9108","interval":808, 'roomId': 'test/topic'},
            {"id":"bc7e8b2e9a71","idType":55,"rssi@1m":-71,"rssi":-93,"raw":4.25,"distance":5.07,"speed":-0.04,"mac":"bc7e8b2e9a71","interval":2741, 'roomId': 'test/topic'},
            {"id":"msft:cdp:0922","idType":40,"rssi@1m":-71,"rssi":-61,"raw":0.52,"distance":0.58,"speed":-0.01,"mac":"3c690ee96a82","interval":314, 'roomId': 'test/topic/2'},
            {"id":"244b03d72780","idType":55,"rssi@1m":-71,"rssi":-84,"raw":2.35,"distance":2.33,"speed":-0.00,"mac":"244b03d72780","interval":613, 'roomId': 'test/topic'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-53,"raw":0.31,"distance":0.34,"speed":-0.00,"mac":"55959568c9b6","interval":738, 'roomId': 'test/topic'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-82,"raw":2.06,"distance":2.11,"speed":-0.01,"mac":"7422e97424d0","interval":802, 'roomId': 'test/topic'},
            {"id":"md:0901:12","idType":20,"rssi@1m":-71,"rssi":-87,"raw":2.87,"distance":3.18,"speed":-0.03,"mac":"74812d6dada3","interval":2062, 'roomId': 'test/topic'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-84,"raw":2.35,"distance":3.43,"speed":-0.04,"mac":"4949491706f1","interval":1272, 'roomId': 'test/topic'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-79,"raw":1.69,"distance":1.95,"speed":-0.01,"mac":"5434446b9108","interval":821, 'roomId': 'test/topic'},
            {"id":"msft:cdp:0922","idType":40,"rssi@1m":-71,"rssi":-60,"raw":0.48,"distance":0.53,"speed":-0.00,"mac":"3c690ee96a82","interval":308, 'roomId': 'test/topic'},
            {"id":"244b03d72780","idType":55,"rssi@1m":-71,"rssi":-83,"raw":2.20,"distance":2.36,"speed":-0.01,"mac":"244b03d72780","interval":607, 'roomId': 'test/topic/2'},
            {"id":"sd:0xfe9f","idType":15,"rssi@1m":-71,"rssi":-56,"raw":0.37,"distance":0.33,"speed":0.00,"mac":"55959568c9b6","interval":747, 'roomId': 'test/topic'}]
f = open("data.txt", "w")
for row in testData:
    f.write(row)


HubController.processData()
f.close()
open("data.txt", "w").close()
print(HubController.roomOccupancy)