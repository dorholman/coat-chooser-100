import random

# Parka = less then 25
# Heavy coat = less then 32
# Sweater = less then 40
# Jean jacket = less then 50
'''
if (weather < 26):
    print("Parka")

elif (weather < 40):
    print("Heavy coat")

elif (weather < 51):
    print("Sweater")

elif (weather < 61):
    print("Jean jacket")
'''

import requests, json
import RPi.GPIO as GPIO
import time

#jacket pins
HJ = 26
S = 5
TJ = 6
P = 13
NJ = 22

#set up GPIO pins:
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22,GPIO.OUT)
GPIO.setup(5,GPIO.OUT)
GPIO.setup(6,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

# Get city from IP info
ipinfo_base_url = "http://ipinfo.io"
response = requests.get(ipinfo_base_url)

area_info = response.json()
city = area_info['city']
loc = area_info['loc']
loc_split = loc.split(",")
#print(loc_split[0])
#print(loc_split[1])
lat = loc_split[0]
lon = loc_split[1]

while True:
    # Now get the weather
    weather_base_url = "http://api.openweathermap.org/data/2.5/weather?"

    api_key = "c8ff3b587ef1a84af6891810a00b9ca7"
    weather_url = weather_base_url + "appid=" + api_key + "&lat=" + lat + "&lon=" + lon + "&units=imperial"
   # print(weather_url)
    try:
        response = requests.get(weather_url)
    except ConnectionError:
        GPIO.output(S, GPIO.HIGH)
        GPIO.output(P, GPIO.HIGH)
        GPIO.output(TJ, GPIO.HIGH)
        GPIO.output(NJ, GPIO.HIGH)
        GPIO.output(HJ, GPIO.HIGH)
        time.sleep(300)
        GPIO.output(S, GPIO.LOW)
        GPIO.output(P, GPIO.LOW)
        GPIO.output(TJ, GPIO.LOW)
        GPIO.output(NJ, GPIO.LOW)
        GPIO.output(HJ, GPIO.LOW)
        continue

    weather_info = response.json()
    #print(weather_info)

    if weather_info['cod'] != "404":

        main_weather = weather_info["main"]

        current_temperature = main_weather["temp"]

       # print(main_weather["temp"])
    else:
	    print(" City Not Found ")
    temp = main_weather["temp"]
    print(temp)
    if (temp < 20):
        print("Parka")
        GPIO.output(P,GPIO.HIGH)

        GPIO.output(S,GPIO.LOW)
        GPIO.output(TJ,GPIO.LOW)
        GPIO.output(NJ,GPIO.LOW)
        GPIO.output(HJ,GPIO.LOW)

    elif (temp < 40):
        print("Heavy coat")
        GPIO.output(HJ,GPIO.HIGH)

        GPIO.output(NJ,GPIO.LOW)
        GPIO.output(TJ,GPIO.LOW)
        GPIO.output(P,GPIO.LOW)
        GPIO.output(S,GPIO.LOW)

    elif (temp < 50):
        print("thin jacket")
        GPIO.output(TJ,GPIO.HIGH)

        GPIO.output(S,GPIO.LOW)
        GPIO.output(NJ,GPIO.LOW)
        GPIO.output(P,GPIO.LOW)
        GPIO.output(HJ,GPIO.LOW)

    elif (temp < 65):
        print("Sweater")
        GPIO.output(S,GPIO.HIGH)

        GPIO.output(P,GPIO.LOW)
        GPIO.output(TJ,GPIO.LOW)
        GPIO.output(NJ,GPIO.LOW)
        GPIO.output(HJ,GPIO.LOW)

    else:
        print("No jacket")
        GPIO.output(NJ,GPIO.HIGH)

        GPIO.output(S,GPIO.LOW)
        GPIO.output(TJ,GPIO.LOW)
        GPIO.output(P,GPIO.LOW)
        GPIO.output(HJ,GPIO.LOW)
    time.sleep(60)
