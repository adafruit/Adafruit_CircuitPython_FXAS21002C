# The MIT License (MIT)
#
# Copyright (c) 2017 Tony DiCola for Adafruit Industries
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
"""
`adafruit_fxas21002c`
====================================================

CircuitPython module for the NXP FXAS21002C gyroscope.  Based on the driver
from:
  https://github.com/adafruit/Adafruit_FXAS21002C

See examples/simpletest.py for a demo of the usage.

* Author(s): Tony DiCola
"""
import time

import adafruit_bus_device.i2c_device as i2c_device


# Internal constants and register values:
_FXAS21002C_ADDRESS       = const(0x21)  # 0100001
_FXAS21002C_ID            = const(0xD7)  # 1101 0111
_GYRO_REGISTER_STATUS     = const(0x00)
_GYRO_REGISTER_OUT_X_MSB  = const(0x01)
_GYRO_REGISTER_OUT_X_LSB  = const(0x02)
_GYRO_REGISTER_OUT_Y_MSB  = const(0x03)
_GYRO_REGISTER_OUT_Y_LSB  = const(0x04)
_GYRO_REGISTER_OUT_Z_MSB  = const(0x05)
_GYRO_REGISTER_OUT_Z_LSB  = const(0x06)
_GYRO_REGISTER_WHO_AM_I   = const(0x0C)  # 11010111   r
_GYRO_REGISTER_CTRL_REG0  = const(0x0D)  # 00000000   r/w
_GYRO_REGISTER_CTRL_REG1  = const(0x13)  # 00000000   r/w
_GYRO_REGISTER_CTRL_REG2  = const(0x14)  # 00000000   r/w
_GYRO_SENSITIVITY_250DPS  = 0.0078125    # Table 35 of datasheet
_GYRO_SENSITIVITY_500DPS  = 0.015625     # ..
_GYRO_SENSITIVITY_1000DPS = 0.03125      # ..
_GYRO_SENSITIVITY_2000DPS = 0.0625       # ..

# User facing constants/module globals:
GYRO_RANGE_250DPS  = 250
GYRO_RANGE_500DPS  = 500
GYRO_RANGE_1000DPS = 1000
GYRO_RANGE_2000DPS = 2000

class FXAS21002C:

    # Class-level buffer for reading and writing data with the sensor.
    # This reduces memory allocations but means the code is not re-entrant or
    # thread safe!
    _BUFFER = bytearray(7)

    def __init__(self, i2c, address=_FXAS21002C_ADDRESS,
                 gyro_range=GYRO_RANGE_250DPS):
        assert gyro_range in (GYRO_RANGE_250DPS, GYRO_RANGE_500DPS,
                              GYRO_RANGE_1000DPS, GYRO_RANGE_2000DPS)
        self._gyro_range = gyro_range
        self._device = i2c_device.I2CDevice(i2c, address)
        # Check for chip ID value.
        if self._read_u8(_GYRO_REGISTER_WHO_AM_I) != _FXAS21002C_ID:
            raise RuntimeError('Failed to find FXAS21002C, check wiring!')
        ctrlReg0 = 0x00
        if gyro_range == GYRO_RANGE_250DPS:
            ctrlReg0 = 0x03
        elif gyro_range == GYRO_RANGE_500DPS:
            ctrlReg0 = 0x02
        elif gyro_range == GYRO_RANGE_1000DPS:
            ctrlReg0 = 0x01
        elif gyro_range == GYRO_RANGE_2000DPS:
            ctrlReg0 = 0x00
        # Reset then switch to active mode with 100Hz output
        # Putting into standy doesn't work as the chip becomes instantly
        # unresponsive.  Perhaps CircuitPython is too slow to go into standby
        # and send reset?  Keep these two commented for now:
        #self._write_u8(_GYRO_REGISTER_CTRL_REG1, 0x00)     # Standby)
        #self._write_u8(_GYRO_REGISTER_CTRL_REG1, (1<<6))   # Reset
        self._write_u8(_GYRO_REGISTER_CTRL_REG0, ctrlReg0) # Set sensitivity
        self._write_u8(_GYRO_REGISTER_CTRL_REG1, 0x0E)     # Active
        time.sleep(0.1) # 60 ms + 1/ODR

    def _read_u8(self, address):
        # Read an 8-bit unsigned value from the specified 8-bit address.
        with self._device:
            self._BUFFER[0] = address & 0xFF
            self._device.write(self._BUFFER, end=1, stop=False)
            self._device.readinto(self._BUFFER, end=1)
        return self._BUFFER[0]

    def _write_u8(self, address, val):
        # Write an 8-bit unsigned value to the specified 8-bit address.
        with self._device:
            self._BUFFER[0] = address & 0xFF
            self._BUFFER[1] = val & 0xFF
            self._device.write(self._BUFFER, end=2)

    def read_raw(self):
        """Read the raw gyroscope readings.  Returns a 3-tuple of X, Y, Z axis
        16-bit unsigned values.  If you want the gyroscope values in friendly
        units consider using the gyroscope property!
        """
        # Read 7 bytes from the sensor.
        with self._device:
            self._BUFFER[0] = _GYRO_REGISTER_STATUS | 0x80
            self._device.write(self._BUFFER, end=1, stop=False)
            self._device.readinto(self._BUFFER)
        # Parse out the gyroscope data.
        status = self._BUFFER[0]
        xhi    = self._BUFFER[1]
        xlo    = self._BUFFER[2]
        yhi    = self._BUFFER[3]
        ylo    = self._BUFFER[4]
        zhi    = self._BUFFER[5]
        zlo    = self._BUFFER[6]
        # Shift values to create properly formed integers
        raw_x = ((xhi << 8) | xlo) & 0xFFFF
        raw_y = ((yhi << 8) | ylo) & 0xFFFF
        raw_z = ((zhi << 8) | zlo) & 0xFFFF
        return (raw_x, raw_y, raw_z)

    @property
    def gyroscope(self):
        """Read the gyroscope value and return its X, Y, Z axis values as a
        3-tuple in radians/second.
        """
        raw = self.read_raw()
        # Compensate values depending on the resolution
        if self._gyro_range == GYRO_RANGE_250DPS:
            return map(lambda x: x * _GYRO_SENSITIVITY_250DPS, raw)
        elif self._gyro_range == GYRO_RANGE_500DPS:
            return map(lambda x: x * _GYRO_SENSITIVITY_500DPS, raw)
        elif self._gyro_range == GYRO_RANGE_1000DPS:
            return map(lambda x: x * _GYRO_SENSITIVITY_1000DPS, raw)
        elif self._gyro_range == GYRO_RANGE_2000DPS:
            return map(lambda x: x * _GYRO_SENSITIVITY_2000DPS, raw)
