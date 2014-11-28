import urllib
import RPi.GPIO as GPIO
import time
import urllib
import sys

urlHum ='http://zen-catacomb.herokuapp.com/humidity/'
urlTemp='http://zen-catacomb.herokuapp.com/temperature/'
nodata = "".encode("UTF-8")

def bin2dec(string_num):
    return str(int(string_num, 2))

data = []

GPIO.setmode(GPIO.BCM)

def log(msg):
    sys.stdout.write(time.strftime("%H:%M:%S") + " - " + msg + "\n")
    sys.stdout.flush()

def bin2dec(string_num):
    return int(string_num, 2)

while True:
  time.sleep(0.5)
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(4,GPIO.OUT)
  GPIO.output(4,GPIO.HIGH)
  time.sleep(0.025)
  GPIO.output(4,GPIO.LOW)
  time.sleep(0.02)

  GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_UP)

  data = []

  for i in range(0,500):
      data.append(GPIO.input(4))

  bit_count = 0
  tmp = 0
  count = 0
  HumidityBit = ""
  TemperatureBit = ""
  crc = ""

  try:
    while data[count] == 1:
      tmp = 1
      count = count + 1

    for i in range(0, 32):
      bit_count = 0

      while data[count] == 0:
        tmp = 1
        count = count + 1

      while data[count] == 1:
        bit_count = bit_count + 1
        count = count + 1

      if bit_count > 3:
        if i>=0 and i<8:
          HumidityBit = HumidityBit + "1"
        if i>=16 and i<24:
          TemperatureBit = TemperatureBit + "1"
      else:
        if i>=0 and i<8:
          HumidityBit = HumidityBit + "0"
        if i>=16 and i<24:
          TemperatureBit = TemperatureBit + "0"
  except:
    log("ERR_RANGE")
    continue

  try:
    for i in range(0, 8):
      bit_count = 0

      while data[count] == 0:
        tmp = 1
        count = count + 1

      while data[count] == 1:
        bit_count = bit_count + 1
        count = count + 1

      if bit_count > 3:
        crc = crc + "1"
      else:
        crc = crc + "0"
  except:
    log("ERR_RANGE")
    continue

  humidity = bin2dec(HumidityBit)
  temperature = bin2dec(TemperatureBit)

  if humidity + temperature - bin2dec(crc) == 0:
    log("Humidity:"+ str(humidity) +"%")
    urllib.urlopen(urlHum + str(humidity), data=nodata)
    log("Temperature:"+ str(temperature) +"C")
    urllib.urlopen(urlTemp + str(temperature), data=nodata)
  else:
    log("ERR_CRC")
