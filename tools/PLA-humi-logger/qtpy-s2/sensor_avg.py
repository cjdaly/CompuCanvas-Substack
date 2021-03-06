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

class TempHumiAvg:
    def __init__(self, sensor, name=""):
        self.sensor = sensor
        self.name = name
        self.temps = []
        self.humis = []
    
    def measure(self):
        temp, humi = self.sensor.measurements
        self.temps.append(temp)
        self.humis.append(humi)

    def size(self):
        return len(self.temps)

    def clear(self):
        self.temps.clear()
        self.humis.clear()

    def averages(self):
        if self.size() < 3:
            return None, None
        t = sorted(self.temps)[1:-1]
        h = sorted(self.humis)[1:-1]
        self.clear()
        return sum(t)/len(t), sum(h)/len(h)
    