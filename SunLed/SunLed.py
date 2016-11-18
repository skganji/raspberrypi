#!/usr/bin/env python
"""
#==============================================================================
#title           :SunLed.py
#description     :This program will Calculate SunSet and SunRise times
                  and turn on LED connected to a relay on GPIO 7 (PIN 26)
                  30 Minutes before SunSet and turn it off 30 Minutes
                  after SunRise
#author          :Sampath Ganji
#date            :11/18/2016
#version         :0.1
#usage           :python pyscript.py
#notes           :
#python_version  :2.7.10 
#==============================================================================
"""

# Import the modules needed to run the script.
import RPi.GPIO as GPIO
import time
import ConfigParser
from Sun import Sun
from datetime import datetime, timedelta

def isSunSet(coords):
    """
    Check if Sun has set for the specified Coordinates
    """
    sun = Sun()
    SunSetTime = sun.getSunsetTime( coords )
    
    now = datetime.now()
    SunSetTimeDT = datetime(now.year, now.month, now.day, SunSetTime['hr'], int(SunSetTime['min']), 00)
    
    if now > SunSetTimeDT - timedelta(minutes=30):
        print "Sun is set"
        print "Now", now, "SunSet", SunSetTimeDT
        return True
    else:
        return False

def isSunRise(coords):
    """
    Check if Sun has risen for the specified Coordinates
    """
    sun = Sun()
    SunRiseTime = sun.getSunriseTime( coords )

    now = datetime.now()
    SunRiseTimeDT = datetime(now.year, now.month, now.day, SunRiseTime['hr'], int(SunRiseTime['min']), 00)
    
    if now > SunRiseTimeDT + timedelta(minutes=30):
        print "Sun is risen"
        print "Now", now, "SunRise", SunRiseTimeDT
        return True
    else:
        return False

if __name__ == "__main__":
    Config = ConfigParser.ConfigParser()
    Config.read("./config.ini")
    latitude = Config.get('coordinates', 'latitude')
    longitude = Config.get('coordinates', 'longitude')
    # Pin Definitons:
    ledPin = 26 # Broadcom pin 23 (Pi pin 16)

    # Pin Setup:
    GPIO.setmode(GPIO.BOARD) # Board pin-numbering scheme
    GPIO.setup(ledPin, GPIO.OUT) # LED pin set as output

    # Initial state for LEDs:
    GPIO.output(ledPin, GPIO.HIGH)

    # Longitude and Latitude from configuration file
    coords = {'longitude' : longitude, 'latitude' : latitude }
    try:
        while 1:
            if isSunSet(coords) or not isSunRise(coords):
                if GPIO.input(ledPin):
                    print "Turning on LED"
                    GPIO.output(ledPin, GPIO.LOW)
            else:
                if not GPIO.input(ledPin):
                    print "Turning off LED"
                    GPIO.output(ledPin, GPIO.HIGH)
            time.sleep(60)
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPIO
