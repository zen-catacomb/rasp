import urllib
import RPi.GPIO as GPIO
import time
import sys

url='http://zen-catacomb.herokuapp.com/touch'
nodata = "".encode("UTF-8")

GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.IN)

def log(msg):
    sys.stdout.write( time.strftime("%H:%M:%S") + " - " + msg + "\n")
    sys.stdout.flush()

prev = 0
while True:
    try:
        value = GPIO.input(17)
        if( value == 0 and prev == 1 ):
          log("touch event")
          urllib.urlopen(url, data=nodata)
        prev = value
    except Exception as e:
        log('x')
    time.sleep(0.1)
