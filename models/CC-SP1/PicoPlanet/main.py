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

import time, board, touchio
from digitalio import DigitalInOut, Direction, Pull

touch1 = touchio.TouchIn(board.A0)
touch2 = touchio.TouchIn(board.A1)
touch3 = touchio.TouchIn(board.A2)

minMax1 = [touch1.raw_value, touch1.raw_value]
minMax2 = [touch2.raw_value, touch2.raw_value]
minMax3 = [touch3.raw_value, touch3.raw_value]

ledG = DigitalInOut(board.D5) ; ledG.direction = Direction.OUTPUT
ledR = DigitalInOut(board.D6) ; ledR.direction = Direction.OUTPUT
ledB = DigitalInOut(board.D7) ; ledB.direction = Direction.OUTPUT

dOut1 = DigitalInOut(board.D1) ; dOut1.direction = Direction.OUTPUT
dOut2 = DigitalInOut(board.D2) ; dOut2.direction = Direction.OUTPUT
dOut3 = DigitalInOut(board.D3) ; dOut3.direction = Direction.OUTPUT

def processTouch(touch, minMax, led, dOut):
  v = touch.raw_value
  if v < minMax[0]:
    minMax[0] = v
  if v > minMax[1]:
    minMax[1] = v
  #
  m = (minMax[1]-minMax[0]) / 2
  if v > minMax[0]+m:
    led.value = False ; dOut.value = True ; return True
  else:
    led.value = True ; dOut.value = False ; return False

def tchTxt(t, m):
  return str(t.raw_value) + "(" + str(m[0]) + "," + str(m[1]) + ")"

def printTouches(t1, m1, t2, m2, t3, m3):
  print(
    "t1:" + tchTxt(t1, m1) +
    ", t2:" + tchTxt(t2, m2) +
    ", t3:" + tchTxt(t3, m3)
  )

while True:
  # printTouches(touch1, minMax1, touch2, minMax2, touch3, minMax3)
  rgbTxt = "["
  if processTouch(touch1, minMax1, ledR, dOut1):
    rgbTxt += 'R'
  else:
    rgbTxt += 'r'
  #
  if processTouch(touch2, minMax2, ledG, dOut2):
    rgbTxt += 'G'
  else:
    rgbTxt += 'g'
  #
  if processTouch(touch3, minMax3, ledB, dOut3):
    rgbTxt += 'B'
  else:
    rgbTxt += 'b'
  rgbTxt += ']'
  print(rgbTxt)
  time.sleep(0.33)


