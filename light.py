import urllib
import RPi.GPIO as GPIO
import time
import sys

url='http://zen-catacomb.herokuapp.com/light/'
nodata = "".encode("UTF-8")

GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN)

def log(msg):
    sys.stdout.write( time.strftime("%H:%M:%S") + " - " + msg + "\n")
    sys.stdout.flush()

while True:
    try:
        value=str(1-GPIO.input(4))
        log(value)
        urllib.urlopen(url + value, data=nodata)
    except Exception as e:
        log('x')
    time.sleep(1)
