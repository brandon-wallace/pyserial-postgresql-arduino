#!/usr/bin/env python3
"""
This program will request data from an Arduino device's DS18S20 temperature
sensors at a specified interval. The data is saved in a Postgresql database.
"""

import logging
from datetime import datetime
import time
import serial
from database import insert_data


logging.basicConfig(filename='error.log', level=logging.DEBUG, filemode='w',
                    format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()
logger.disabled = False


# Initiate the serial connection to the Arduino device.
try:
    logger.debug('Attempting to make serial connection to Arduino board.')
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    # Brief pause to establish connection to port.
    time.sleep(3)
except Exception as e:
    logger.exception(e)
    exit(1)


def read_sensors():
    '''Read the sensors connected to Arduino device.'''
    global sensor1, sensor2, sensor3
    logger.debug('Sending signal to request sensor data.')
    # When the Arduino receives the character 'z' it will read the sensor data.
    ser.write(b'z')
    try:
        data = ser.readline().decode('utf-8')
        data = data.split()
        sensor1 = data[0]
        sensor2 = data[1]
        sensor3 = data[2]
        return (sensor1, sensor2, sensor3)
    except Exception as e:
        logger.exception(e)
        return


while True:
    # Get the current date and time from the datetime module.
    date_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    read_sensors()
    # Save data in a Postgresql database.
    insert_data(date_time, sensor1, sensor2, sensor3)
    # Set an interval by seconds.
    time.sleep(300)

ser.close()
