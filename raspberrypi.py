import serial
import RPi.GPIO
import urllib2
import json

hostname = 'http://139.199.168.197:5000/dachuang/api/v1/'
yellowLED = {'hardwarename' : 'redLED'}

ser = serial.Serial('/dev/ttyACM0', 9600, timeout = 1)

while 1:
    try:
	r = urllib2.Request(hostname + 'hardware?hardwarename=redLED')
        r = urllib2.urlopen(r)
        res = r.read()
        result = json.loads(res)
        print result
    except urllib2.HTTPError, e:
        print e.code
    except urllib2.URLError, e:
        print str(e)

    hardwarename = result['name']
    if hardwarename == 'redLED':
        if result['status'] == 1:
	    ser.write('y')
    	else:
    	    ser.write('N')
    	response = ser.readall()
    	print response
