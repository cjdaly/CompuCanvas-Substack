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

import unittest
import sensor_avg

class MockSensor:
    def __init__(self, t=0, h=0):
        self.measurements = [t,h]

    def set(self, t, h):
        self.measurements[0] = t
        self.measurements[1] = h

class TestTempHumiAvg(unittest.TestCase):
    def test_MockSensor(self):
        ms = MockSensor(1, 2)
        self.assertEqual(1, ms.measurements[0])
        self.assertEqual(2, ms.measurements[1])
        #
        ms = MockSensor(3)
        self.assertEqual(3, ms.measurements[0])
        self.assertEqual(0, ms.measurements[1])
        #
        ms = MockSensor()
        self.assertEqual(0, ms.measurements[0])
        self.assertEqual(0, ms.measurements[1])

    def test_MockSensor_set(self):
        ms = MockSensor()
        self.assertEqual(0, ms.measurements[0])
        self.assertEqual(0, ms.measurements[1])
        #
        ms.set(3, 5)
        self.assertEqual(3, ms.measurements[0])
        self.assertEqual(5, ms.measurements[1])

    def test_TempHumiAvg(self):
        ms = MockSensor()
        tha = sensor_avg.TempHumiAvg(ms)
        for i in range(6):
            ms.set(i, i)
            tha.measure()
        self.assertEqual(6, tha.size())
        #
        t, h = tha.averages()
        self.assertEqual(2.5, t)
        self.assertEqual(2.5, h)
        self.assertEqual(0, tha.size())

    def test_TempHumiAvg_unsorted(self):
        ms = MockSensor()
        tha = sensor_avg.TempHumiAvg(ms)
        #
        ms.set(2, 5) ; tha.measure()
        ms.set(1, 2) ; tha.measure()
        ms.set(0, 1) ; tha.measure()
        ms.set(5, 3) ; tha.measure()
        ms.set(4, 0) ; tha.measure()
        ms.set(3, 4) ; tha.measure()
        self.assertEqual(6, tha.size())
        #
        t, h = tha.averages()
        self.assertEqual(2.5, t)
        self.assertEqual(2.5, h)
        self.assertEqual(0, tha.size())

    def test_TempHumiAvg_None(self):
        ms = MockSensor()
        tha = sensor_avg.TempHumiAvg(ms)
        self.assertEqual(0, tha.size())
        #
        t, h = tha.averages()
        self.assertIsNone(t)
        self.assertIsNone(h)
        #
        ms.set(3, 3)
        tha.measure()
        self.assertEqual(1, tha.size())
        #
        t, h = tha.averages()
        self.assertIsNone(t)
        self.assertIsNone(h)

