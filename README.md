# SmartCityLights 

##[Visit our website!] (http://fengyicitylight.parseapp.com/)

###Our goal is to monitor and control a light bulb from the Internet.
####Introduction
The light bulb can be treated as a street lamp / light that can be controlled by any third party through the cloud. Additionally, we also detect the number of people near the light bulb through Broadcom's WICED Sense sensor. The WICED Sense communicates through Bluetooth Low Energy and informs the cloud about details such as temperature, pressure, etc.


We can dynamically vary the intensity of the light bulb and read information from it into the cloud.
####About
In this project, the light bulb is being emulated on the Raspberry Pi / Linux machine. There are three programs to implement city light project:

The bulb's logic is programmed in C (~/Bulb/bulbemulate.py)
The bulb's GUI is programmed in Python (~/Bulb/bulbemulate.py)
The weather information to adjust bulb is pulled from http://openweathermap.org/, programmed in python (~/Bulb/weather.py)
These three programs are tied together through Inter Process Communication using sockets. Each program communicated with the other on a specific socket port as the system architecture figure shown above. Run the bulbemulate.py, and it calls for other two program weather.py and lightbulb.c.

####Run Program
cd Bulb
python bulbemulate.py
