Introduction
============

.. image:: https://readthedocs.org/projects/adafruit-circuitpython-fxas21002c/badge/?version=latest
    :target: https://docs.circuitpython.org/projects/fxas21002c/en/latest/
    :alt: Documentation Status

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord

.. image:: https://github.com/adafruit/Adafruit_CircuitPython_FXAS21002C/workflows/Build%20CI/badge.svg
    :target: https://github.com/adafruit/Adafruit_CircuitPython_FXAS21002C/actions/
    :alt: Build Status

CircuitPython module for the NXP FXAS21002C gyroscope.

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_
* `Bus Device <https://github.com/adafruit/Adafruit_CircuitPython_BusDevice>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://github.com/adafruit/Adafruit_CircuitPython_Bundle>`_.

Installing from PyPI
=====================
On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/adafruit-circuitpython-fxas21002c/>`_. To install for current user:

.. code-block:: shell

    pip3 install adafruit-circuitpython-fxas21002c

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install adafruit-circuitpython-fxas21002c

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .env
    source .env/bin/activate
    pip3 install adafruit-circuitpython-fxas21002c

Usage Example
=============

.. code-block:: python3

    import time
    import board
    import adafruit_fxas21002c

    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = adafruit_fxas21002c.FXAS21002C(i2c)

    while True:
        gyro_x, gyro_y, gyro_z = sensor.gyroscope
        print('Gyroscope (radians/s): ({0:0.3f},  {1:0.3f},  {2:0.3f})'.format(gyro_x, gyro_y, gyro_z))
        time.sleep(1.0)


Documentation
=============

API documentation for this library can be found on `Read the Docs <https://docs.circuitpython.org/projects/fxas21002c/en/latest/>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/adafruit/Adafruit_CircuitPython_fxas21002c/blob/main/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.

Documentation
=============

For information on building library documentation, please check out `this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.
