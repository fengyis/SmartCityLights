############################################################
# IOT Poject
# GUI for Light Bulb
# This program is the core that loads other dependent
# programs.
############################################################

import subprocess
import os
import signal
import Tkinter as tk
import ImageTk
import Image
import socket
import select
import httplib
import json
from threading import Thread

# Constants
PORT_LOCALINFO = 50012
PORT_TIME = 50011
PORT_INTENSITY = 50013
HOST = "127.0.0.1"
baseUrl = "api.parse.com"

# Initializing variables and basic set up for Bulb GUI. All images for bulb are pulled from ./Images/ folder
bulbRoot = tk.Tk()
img = ImageTk.PhotoImage(Image.open("../Images/Intensity_0.png").resize((640,500), Image.ANTIALIAS))
bulbRoot.geometry("640x800")
panel = tk.Label(bulbRoot, text="hello", image = img)
headingPanel = tk.Label(bulbRoot, padx=10, text="LightBulb Emulator", fg="green", bg="black", font="Verdana 10 bold", width=640)
weatherPanel = tk.Label(bulbRoot, padx=10, text="Weather,City, and Local Time information to be displayed here", fg="red", bg="yellow", font="Verdana 10 bold", width=640, height=200)
panel.pack(side="bottom")
headingPanel.pack(side="top")
weatherPanel.pack(side="top")
intensity, currentTime = None, None
city, country = None, None
briefWeather, weatherDesc = None, None
socketBulb = 0
socketLocalInfo = 0
socketTime = 0
socketDict = {socketBulb:True, socketTime:True, socketLocalInfo:True}

# Function to create a socket for server and listen on respective port. We invoke this from main()
def createServerSocket(port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((HOST, port))
	s.listen(2)
	s.setblocking(0)
	return s

# We listen on sockets on PORTs defined above
def acceptSocketConnection(listOfSockets):
	global intensity, currentTime, briefWeather, weatherDesc, city, country
	while(True):
		inputs = listOfSockets
		print listOfSockets
		outputs = []
		while inputs:
			readable, writeable, exceptional = select.select(inputs, outputs, inputs, 2)
			for s in readable:
				if s is socketTime:
					conn, addr = socketTime.accept()
					currentTime = conn.recv(10)
					conn.close()
				if s is socketBulb:
					conn, addr = socketBulb.accept()
					intensity = conn.recv(10)
					conn.close()
				if s is socketLocalInfo:
					conn, addr = socketLocalInfo.accept()
					data = conn.recv(1024)
					city = data.split("\n")[0] + "\n"
					country = data.split("\n")[1] + "\n"
					briefWeather = data.split("\n")[2] + "\n"
					weatherDesc = data.split("\n")[3] + "\n"
					conn.close()

# This function is a callback after periodic interval. Called by bulbRoot.after()
# We also update the GUI of bulb here
def checkCondition():

	print "Intensity is", intensity , type(intensity)
	if intensity == "0":
		new_path = "Intensity_0.png"
	if intensity == "1":
		new_path = "Intensity_1.png"
	if intensity == "2":
		new_path = "Intensity_2.png"
	if intensity == "3":
		new_path = "Intensity_3.png"
	if intensity == "4":
		new_path = "Intensity_4.png"
	if intensity == "5":
		new_path = "Intensity_5.png"
	if intensity == "6":
		new_path = "Intensity_6.png"
	if intensity == "7":
		new_path = "Intensity_7.png"
	if intensity == "8":
		new_path = "Intensity_8.png"
	if intensity == "9":
		new_path = "Intensity_9.png"
	if intensity == "10":
		new_path = "Intensity_10.png"

	if intensity != None:
		# Update the new image and text when needed in GUI
		newImg = ImageTk.PhotoImage(Image.open("../Images/" + new_path).resize((640,500), Image.ANTIALIAS))
		panel.configure(image = newImg)
		panel.image = newImg
	
	if city != None and country != None and briefWeather != None and weatherDesc != None:
		weatherPanel.configure(text = city + country + briefWeather + weatherDesc + currentTime, fg="red", bg="yellow", font="Verdana 10 bold", width=640, height=200)
		connection = httplib.HTTPSConnection(baseUrl, 443)
		connection.connect()
		connection.request('PUT', '/1/classes/TestObject/R9rJyA1Jx0', json.dumps({
       "City": city,
       "Weather": briefWeather
     }), {
       "X-Parse-Application-Id": "tDqgJgXy6F4s7imyPGuPEFyLFkeEkm3B1kEUMg8D",
       "X-Parse-REST-API-Key": "oB1DseqDiajKRJsOsQ56cDCBYuMgYkFi5hPm9VEd",
       "Content-Type": "application/json"
     })
		
	bulbRoot.after(5000, checkCondition)

# main()
if __name__=="__main__":

	# Create three 3 server sockets
	socketBulb = createServerSocket(PORT_INTENSITY)
	socketTime = createServerSocket(PORT_TIME)
	socketLocalInfo = createServerSocket(PORT_LOCALINFO)
	socketList = [socketBulb, socketTime, socketLocalInfo]
	thread1 = Thread(target = acceptSocketConnection, args = (socketList, ))
	thread1.daemon = True
	thread1.start()

	# Spawn two other processes for application ( Parse + Weather )
	p1 = subprocess.Popen(['./lightbulb'])
	p2 = subprocess.Popen('python ./weather.py', shell=True, preexec_fn=os.setsid)
	bulbRoot.after(5000, checkCondition)
	bulbRoot.mainloop()

	# Once we close the GUI, we need to clean up and close the processes p1 and p2
	p1.terminate()
	os.killpg(p2.pid, signal.SIGTERM)