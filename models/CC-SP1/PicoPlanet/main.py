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

import time, board, touchio, pulseio, random, gc
from digitalio import DigitalInOut, Direction

touch1 = touchio.TouchIn(board.A0)
touch2 = touchio.TouchIn(board.A1)
touch3 = touchio.TouchIn(board.A2)

minMax1 = [touch1.raw_value, touch1.raw_value]
minMax2 = [touch2.raw_value, touch2.raw_value]
minMax3 = [touch3.raw_value, touch3.raw_value]

ledG = pulseio.PWMOut(board.D5)
ledR = pulseio.PWMOut(board.D6)
ledB = pulseio.PWMOut(board.D7)
ledI = 0.2

dOut1 = DigitalInOut(board.D1) ; dOut1.direction = Direction.OUTPUT
dOut2 = DigitalInOut(board.D2) ; dOut2.direction = Direction.OUTPUT
dOut3 = DigitalInOut(board.D3) ; dOut3.direction = Direction.OUTPUT

def rnd():
  return random.random()

def genColor():
  r = random.randint(0,6)
  if r==0:
    return [rnd(), 0, 0]
  elif r==1:
    return [0, rnd(), 0]
  elif r==2:
    return [0, 0, rnd()]
  elif r==3:
    return [rnd(), rnd(), 0]
  elif r==4:
    return [rnd(), 0, rnd()]
  elif r==5:
    return [0, rnd(), rnd()]
  elif r==6:
    return [rnd(), rnd(), rnd()]

def modeSolid(st):
  col = st['color']
  cyc = st['cycle']

def modePulse(st):
  col = st['color']
  cyc = st['cycle']
  max = st['max']
  if st['inc'] > 0:
    if cyc >= max:
      st['inc'] = -1
    else:
      st['cycle'] += 1
  else:
    if cyc <= 0:
      st['inc'] = 1
      st['rep'] += 1
    else:
      st['cycle'] -= 1
  lvl = cyc / max
  return [col[0]*lvl,col[1]*lvl,col[2]*lvl]

def modeBlink(st):
  cyc = st['cycle']
  if cyc == st['max']:
    st['cycle'] = 0
    st['rep'] += 1
  else:
    st['cycle'] += 1
  #
  if (cyc <= st['mid']):
    return st['color']
  else:
    return st['color2']

def modeSequence(st):
  mi = st['modeIdx']
  m = st['modes'][mi] ; s = st['states'][mi]
  if s['rep'] >= s['reps']:
    s['rep'] = 0
    mi += 1
    if mi >= len(st['modes']):
      mi = 0
    st['modeIdx'] = mi
    m = st['modes'][mi] ; s = st['states'][mi]
  return m(s)

def genState():
  color2 = [0,0,0]
  if random.randint(0,1) == 0:
    color2 = genColor()
  return {
    'color':genColor(),
    'color2': color2,
    'rep':0,
    'reps':random.randint(3,7),
    'cycle':0,
    'max': random.randint(24,64),
    'mid': random.randint(8,32),
    'inc':1,
  }

def genMode():
  m=modeSequence
  modes = [] ; states = []
  s = {
    'modes':modes,
    'states':states,
    'modeIdx':0
  }
  #
  for i in range(random.randint(3,7)):
    mt = random.randint(0,1)
    if mt == 0:
      modes.append(modeBlink)
      states.append(genState())
    elif mt == 1:
      modes.append(modePulse)
      states.append(genState())
  #
  return m,s

mode,state=genMode()

def processTouch(touch, minMax, dOut):
  v = touch.raw_value
  if v < minMax[0]:
    minMax[0] = v
  if v > minMax[1]:
    minMax[1] = v
  #
  m = (minMax[1]-minMax[0]) / 2
  if (m>200) and (v>minMax[0]+m):
    dOut.value = True ; return True
  else:
    dOut.value = False ; return False

def tchTxt(t, m):
  return str(t.raw_value) + "(" + str(m[0]) + "," + str(m[1]) + ")"

def printTouches(t1, m1, t2, m2, t3, m3):
  print(
    "t1:" + tchTxt(t1, m1) +
    ", t2:" + tchTxt(t2, m2) +
    ", t3:" + tchTxt(t3, m3)
  )

def updateRGB(lR, lG, lB, lI, md, st):
  rgb=md(st)
  lR.duty_cycle = 65535 - int(lI * rgb[0] * 65535)
  lG.duty_cycle = 65535 - int(lI * rgb[1] * 65535)
  lB.duty_cycle = 65535 - int(lI * rgb[2] * 65535)

while True:
  # printTouches(touch1, minMax1, touch2, minMax2, touch3, minMax3)
  if processTouch(touch1, minMax1, dOut1) and (ledI>0):
    ledI -= 0.05
    time.sleep(0.33)
  #
  if processTouch(touch2, minMax2, dOut2) and (ledI<=1):
    ledI += 0.05
    time.sleep(0.33)
  #
  if processTouch(touch3, minMax3, dOut3):
    mode,state=genMode()
    gc.collect() ; print("Mem: " + str(gc.mem_free()))
    time.sleep(1.33)
  #
  updateRGB(ledR, ledG, ledB, ledI, mode, state)
  time.sleep(0.05)

