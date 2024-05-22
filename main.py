
from gpiozero import Buzzer
from time import time, sleep
from urllib.request import urlopen
import sys
import max30102
import hrcalc

m = max30102.MAX30102()

hr2 = 0
sp2 = 0


WRITE_API = "Your API Key" # Replace your ThingSpeak API key here
BASE_URL = "https://api.thingspeak.com/update?api_key={}".format(WRITE_API)

buzzer = Buzzer(26)

SENSOR_PIN = 17
humidity=90
temperature=46
SensorPrevSec = 0
SensorInterval = 2 # 2 seconds
ThingSpeakPrevSec = 0
ThingSpeakInterval = 20 # 20 seconds

try:
	while True:
		red, ir = m.read_sequential()
    
		hr,hrb,sp,spb = hrcalc.calc_hr_and_spo2(ir, red)

		print("hr detected:",hrb)
		print("sp detected:",spb)
		
		if(hrb == True and hr != -999):
			hr2 = int(hr)
			print("Heart Rate : ",hr2)
		if(spb == True and sp != -999):
			sp2 = int(sp)
			print("SPO2       : ",sp2)
		if time() - ThingSpeakPrevSec > ThingSpeakInterval:
				ThingSpeakPrevSec = time()
				
				thingspeakHttp = BASE_URL + "&field1={:.2f}&field2={:.2f}".format(hr2, sp2)
				print(thingspeakHttp)
            
				conn = urlopen(thingspeakHttp)
				print("Response: {}".format(conn.read()))
				conn.close()
            
				buzzer.beep(0.05, 0.05, 1)
				sleep(1)
            
except KeyboardInterrupt:
    conn.close()
