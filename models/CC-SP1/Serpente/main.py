# The MIT License (MIT)
#
# Copyright (c) 2021 Chris J Daly (github user cjdaly)
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

import time, board, pulseio, digitalio

def initDIn(dPin):
  dIn = digitalio.DigitalInOut(dPin)
  dIn.direction=digitalio.Direction.INPUT
  dIn.pull=digitalio.Pull.DOWN
  return dIn

# digital inputs
dIn0 = initDIn(board.D0)
dIn1 = initDIn(board.D1)
dIn3 = initDIn(board.D3)
dIn4 = initDIn(board.D4)
dIn5 = initDIn(board.D5)
#
dIns = [dIn0, dIn1, None, dIn3, dIn4, dIn5]

# RGB outputs
ledR = pulseio.PWMOut(board.LED_R)
ledG = pulseio.PWMOut(board.LED_G)
ledB = pulseio.PWMOut(board.LED_B)
#
leds = [ledR, ledG, ledB]

# last values read for mode, red, green, blue
mrgbVals = [0,0,0,0]

# 8 light intensity levels
pwmLvlsR = [0, 8000, 16000, 24000, 32000, 40000, 48000, 54000]
pwmLvlsG = [0, 6000, 12000, 18000, 24000, 30000, 36000, 42000]
pwmLvlsB = [0, 15000, 22000, 32000, 42000, 50000, 58000, 65000]

def readState(dS0, dS1):
  v0=dS0.value ; v1 = dS1.value
  time.sleep(0.1)
  while (v0 != dS0.value) or (v1 != dS1.value) :
    v0=dS0.value ; v1 = dS1.value
    time.sleep(0.1)
  return v0,v1
  
def readValue(dV0, dV1, dV2):
  v = 0
  if dV0.value:
    v += 1
  if dV1.value:
    v += 2
  if dV2.value:
    v += 4
  return v

def updateVals(dIns, mrgbVals):
  s0, s1 = readState(dIns[0], dIns[1])
  val = readValue(dIns[5], dIns[4], dIns[3])
  if not s0 and not s1: # mode select
    mrgbVals[0] = val
  elif not s0 and s1: # red
    mrgbVals[1] = val
  elif s0 and not s1: # green
    mrgbVals[2] = val
  elif s0 and s1: # blue
    mrgbVals[3] = val
  # print("s0: " + str(s0) + ", s1: " + str(s1) + ", val: " + str(val))

def updateLEDs(leds, mrgbVals):
  leds[0].duty_cycle = 65535 - pwmLvlsR[mrgbVals[1]]
  leds[1].duty_cycle = 65535 - pwmLvlsG[mrgbVals[2]]
  leds[2].duty_cycle = 65535 - pwmLvlsB[mrgbVals[3]]

count = 0; max = 20; mode = 0

while True:
  updateVals(dIns, mrgbVals)
  if (mrgbVals[0] != mode):
    mode = mrgbVals[0]
  if mode == 0:
    updateLEDs(leds, mrgbVals)
  else:
    updateLEDs(leds, mrgbVals)
  #
  count += 1
  if count >= max:
    count = 0

