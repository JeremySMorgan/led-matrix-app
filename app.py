from threading import Thread
import time

import socketio
from time import sleep
import json

from src.utils import wait_for_internet
from src.led_writer import LedWriter, LedWriterSim

sio = socketio.Client()

SIM_MODE = True

# Constants
HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"

BRIGHTNESS = 10
CLEAR_TIME_SECS = 15.0*60.0 # Clear led matrix 15 minutes after a new design is received

if not SIM_MODE:
    led_writer = LedWriter(BRIGHTNESS)
else:
    led_writer = LedWriterSim()

newest_request_t = 0


def clear_led_thread():
    """Function that clears the led every `CLEAR_TIME_SECS` seconds. 
    Function is blocking so should be called in its own thread
    """
    global newest_request_t
    request_t = time.time()
    newest_request_t = request_t
    time.sleep(CLEAR_TIME_SECS)
    if newest_request_t == request_t:
        print("clearing board")
        led_writer.clear()
    else:
        print("new request recieved during sleeping period")

@sio.event
def connect():
    print("connected")

@sio.event
def connect_error():
    print('[INFO] Failed to connect to server.')

@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')


@sio.on("led-design")
def message_received(message):
    print("got 'led-design' message")
    request_json = json.loads(message)
    led_writer.write_from_json(request_json)
    thread = Thread(target=clear_led_thread)
    thread.start()
    return {"status": "OK", "error": ""}


@sio.on('*')
def unhandled_event(event, sid, data):
    print("caught an unhandled event")


""" Example usage

source /home/jm/Desktop/led-matrix-app/venv/bin/activate && python3 /home/jm/Desktop/led-matrix-app/app.py
"""

if __name__ == "__main__":

    if not SIM_MODE:
        wait_for_internet()
        led_writer.clear()
        sio.connect(HEROKU_HOSTNAME)
        while True:
            sleep(1.0)

    else:
        sio.connect("http://localhost:5001/")
        led_writer.run()