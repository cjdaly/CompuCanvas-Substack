# The MIT License (MIT)
#
# Copyright (c) 2022 Chris J Daly (github user cjdaly)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

## configure sensors
import board, busio, digitalio, neopixel, time, random, traceback
import adafruit_shtc3, adafruit_sht4x
#
i2c = busio.I2C(board.SCL1, board.SDA1)
shtc3 = adafruit_shtc3.SHTC3(i2c)
sht4x = adafruit_sht4x.SHT4x(i2c)

# sensor averagers
import sensor_avg
shtc3_avg = sensor_avg.TempHumiAvg(shtc3, "shtc3")
sht4x_avg = sensor_avg.TempHumiAvg(sht4x, "sht40")

## NeoPixel
px = neopixel.NeoPixel(board.NEOPIXEL, 1)
px.fill((33,33,0))

# "boot" button
button = digitalio.DigitalInOut(board.BUTTON)
button.switch_to_input(pull=digitalio.Pull.UP)

# wait for button press...
while button.value:
  time.sleep(0.05)
#
px.fill((0,33,33))


## setup display
HAS_OLED=False
#
if HAS_OLED:  
  import displayio
  from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297
  displayio.release_displays()
  time.sleep(1)
  dsp_bus = displayio.I2CDisplay(i2c, device_address=0x3D)
  time.sleep(1)
  dsp = SH1107(dsp_bus, width=128, height=128, display_offset=DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297)
  print ("Initialized display!")

## setup WiFi
import secrets
import wifi, socketpool, ssl
import adafruit_requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError
#
print ("Connecting to WIFI: " + secrets.WIFI_SSID)
wifi.radio.connect(secrets.WIFI_SSID, secrets.WIFI_PASS)
#
pool = socketpool.SocketPool(wifi.radio)
requests = adafruit_requests.Session(pool, ssl.create_default_context())

## config AdaFruit IO
print ("Getting wifi test message...")
rsp = requests.get("http://wifitest.adafruit.com/testwifi/index.html")
print(rsp.text)
#
print ("Adafruit IO user: " + secrets.IO_USER)
io = IO_HTTP(secrets.IO_USER, secrets.IO_KEY, requests)

def process_sensor(sensor_avg, io):
  sensor_avg.measure()
  if sensor_avg.size() >= 6:
    t,h = sensor_avg.averages()
    io.send_data(sensor_avg.name+"-temp", t)
    io.send_data(sensor_avg.name+"-humi", h)

cycle = 0 ; errors = 0
print("\rcy:{}, er:{} ".format(cycle, errors), end='')
while True:
  try:
    px.fill((0,0,33))
    if (shtc3_avg.size() == 5):
      px.fill((0,22,33))
      if not wifi.radio.ipv4_address:
        # attempt to re-connect to WiFi
        wifi.radio.connect(secrets.WIFI_SSID, secrets.WIFI_PASS)
    #
    if random.randint(0,1) == 0:
      process_sensor(shtc3_avg, io)
      process_sensor(sht4x_avg, io)
    else: # switch the order
      process_sensor(sht4x_avg, io)
      process_sensor(shtc3_avg, io)
    #
    if (shtc3_avg.size() == 0):
      cycle += 1
      print("\rcy:{}, er:{} ".format(cycle, errors), end='')
      io.send_data("pla-dehumi.cycle", cycle)
    px.fill((0,33,0))
  except (OSError, RuntimeError) as ex:
    errors += 1
    px.fill((33,11,0))
    sht4x_avg.clear() ; shtc3_avg.clear()
    print()
    traceback.print_exception(ex, ex, ex.__traceback__)
  except BaseException as bex:
    print(" ... exiting ...")
    traceback.print_exception(bex, bex, bex.__traceback__)
    break
  #
  time.sleep(5)
