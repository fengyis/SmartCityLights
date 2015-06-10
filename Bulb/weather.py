############################################################
# IOT Poject
# Pulls the Weather forecast, Sunrise & Sunset Times
# Website for forecast: www.openweathermap.org
# Communication with lghtbulb.c happens over IPC communication port 50008
############################################################

import json
import httplib2
import time
import socket

# Constants
HOST = '127.0.0.1'        # Local host
PORT_WEATHER = 50008      # Weather Port
PORT_LOCALINFO = 50012    # Local Info Port

# Enter city, country to track local weather information. By editing country and city, we can monitor weather for any location.
city = "New York"
country = "USA"
baseUrl = "http://api.openweathermap.org/data/2.5/weather?q="

# Client Side Socket Code. We establish socket connectivity with an endpoint and send weather and local information
# Exceptions need to be caught, else we will terminate abruptly and create havoc.
def clientSendSocket(port, data):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)
	try:
		s.connect((HOST, port))
		s.send(data)
	except socket.error:
		#s.close()
		print "weather::clientSendSocket(): Socket Exception :" + str(port)
	except error:
		#s.close()
		print "weather::clientSenseSocket(): Exception"
		pass
	s.settimeout(None)
	s.close()

# main()
if __name__=="__main__":
	# Initial time delay of 5 seconds required to counter race condition of establishing socket connectivity
	time.sleep(5)
	h = httplib2.Http(".cache")
	h.add_credentials('', '')
	while(True):
		resp, content = h.request(baseUrl  + city + "," + country, "GET")
		try:
			contentJson = json.loads(content)
		except ValueError:
			print "weather::main(): JSON Exception"
			continue

		# Obtain sunset and sunrise times
		sunsetTime = time.ctime(contentJson["sys"]["sunset"]).split(" ")[3]
		sunriseTime = time.ctime(contentJson["sys"]["sunrise"]).split(" ")[3]
		localInfoText = contentJson["name"] + "\n" + contentJson["sys"]["country"] + "\n" + contentJson["weather"][0]["main"] + "\n" + contentJson["weather"][0]["description"] + "\n"
		weatherText = contentJson["weather"][0]["main"] + "\n" + sunriseTime + "\n" + sunsetTime + "\n"
		#print("weather:: Weather from weather.py is "+weatherText);
		# Write data and send via port PORT_WEATHER
		clientSendSocket(PORT_WEATHER, weatherText)
		clientSendSocket(PORT_LOCALINFO, localInfoText)
		time.sleep(5)





