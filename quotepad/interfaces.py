import os
import sqlite3
import time
from multiprocessing import Process

import wiringpi

from quotepad.serializers import BinaryTextEncoder

DATA_REQUEST_PIN = 4
CHANNEL = 0
SPEED = 250000

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(DATA_REQUEST_PIN, wiringpi.GPIO.INPUT)
connection_string = "sqlite:///{}/quotepad.db".format(os.getcwd())
conn = sqlite3.connect(connection_string)
query = """select *
           from text
           where active = 1
           order by id asc"""
cursor = conn.cursor()
query_result = cursor.execute(query)


def send_data():
    global query_result

    try:
        data = next(query_result)
    except StopIteration:
        query_result = cursor.execute(query)
        data = next(query_result)

    bytes_to_send = BinaryTextEncoder.serialize(data[1])
    wiringpi.wiringPiSPIDataRW(0, bytes_to_send)


def reset():
    global query_result
    query_result = cursor.execute(query)


def _run_process():
    wiringpi.wiringPiSPISetup(CHANNEL, SPEED)
    wiringpi.pinMode(DATA_REQUEST_PIN, wiringpi.GPIO.INPUT)
    wiringpi.wiringPiISR(DATA_REQUEST_PIN, wiringpi.GPIO.INT_EDGE_RISING, send_data)

    while True:
        time.sleep(0.1)


def run():
    Process(target=_run_process).start()