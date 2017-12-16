import serial
import RPi.GPIO
import urllib2
import json

hostname = 'http://139.199.168.197:5000/dachuang/api/v1/allHardware'

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 4)

while 1:
    r = urllib2.Request(hostname)
    r = urllib2.urlopen(r)
    res = r.read()
    result = json.loads(res)
    print result
    send = ''
    if result[0]['status'] == 1:
    	send += 'a'
    else:
     	send += 'A'
    if result[1]['status'] == 1:
	send += 'b'
    else:
   	send += 'B'
    ser.write(send)
    response = ser.readall()
    if '' != response: 
        response = response[0:2]
        ret = urllib2.Request("http://139.199.168.197:5000/dachuang/api/v1/updateHardware?hardwarename=tempUnit&status=3" + '&num=' + response)
        ret = urllib2.urlopen(ret)
