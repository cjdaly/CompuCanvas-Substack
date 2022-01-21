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
import board, busio, digitalio, neopixel, time, random
import adafruit_shtc3, adafruit_sht4x
#
i2c = busio.I2C(board.SCL1, board.SDA1)
shtc3 = adafruit_shtc3.SHTC3(i2c)
sht4x = adafruit_sht4x.SHT4x(i2c)

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
import displayio
from adafruit_displayio_sh1107 import SH1107, DISPLAY_OFFSET_ADAFRUIT_128x128_OLED_5297
#
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

def read_sensor(name, sensor, io):
  m = sensor.measurements
  # print ("IO update: " + name)
  io.send_data(name+"-temp", m[0])
  io.send_data(name+"-humi", m[1])
  # print("[{}]-> temp:{}, humi:{}".format(name, m[0], m[1]))

cycle = 0
while True:
  px.fill((0,0,33))
  cycle += 1
  print("\rcycle: " + str(cycle) + " ... ", end='')
  try:
    if random.randint(0,1) == 0:
      read_sensor("shtc3", shtc3, io)
      read_sensor("sht40", sht4x, io)
    else: # switch the order
      read_sensor("sht40", sht4x, io)
      read_sensor("shtc3", shtc3, io)
    #
    io.send_data("pla-dehumi.cycle", cycle)
    px.fill((0,33,0))
    time.sleep(30)
  except BaseException as bex:
    print(bex)
    break

print("Exiting...")
