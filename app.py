from threading import Thread
from time import time, sleep
import json

import socketio

from src.utils import wait_for_internet
from src.led_writer import LedWriter, LedWriterSim

sio = socketio.Client()

# SIM_MODE = True
SIM_MODE = False

# Constants
HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"

BRIGHTNESS = 10
CLEAR_TIME_SECS = 15.0*60.0 # Clear led matrix 15 minutes after a new design is received
CLEAR_TIME_SECS = 10


if not SIM_MODE:
    led_writer = LedWriter(BRIGHTNESS)
else:
    led_writer = LedWriterSim()

newest_request_t = 0
board_is_active = False


def clock_thread():
    # shows the time when the board is inactive
    global board_is_active
    while True:
        if board_is_active:
            continue
        led_writer.draw_time()
        sleep(0.1)


def clear_led_thread(delay: float):
    """Function that clears the led every `CLEAR_TIME_SECS` seconds. 
    Function is blocking so should be called in its own thread
    """
    global newest_request_t, board_is_active
    board_is_active = True
    request_t = time()
    newest_request_t = request_t
    sleep(delay)
    if newest_request_t == request_t:
        print("clear_led_thread(): clearing board")
        led_writer.clear()
        led_writer.stop_cgl()
        board_is_active = False
    else:
        print("clear_led_thread(): new request recieved during sleeping period, exiting with noops performed")

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
    print("message_received(message): received message")
    request_json = json.loads(message)
    # with open("data/cgl.json", "w") as json_file:
    #     json.dump(request_json, json_file)
    led_writer.write_from_json(request_json)
    thread = Thread(target=clear_led_thread, args=(CLEAR_TIME_SECS, ))
    thread.start()
    return {"status": "OK", "error": ""}


@sio.on('*')
def unhandled_event(event, sid, data):
    print("caught an unhandled event")


""" Example usage

source /home/jm/Desktop/led-matrix-app/venv/bin/activate && python3 /home/jm/Desktop/led-matrix-app/app.py
"""

if __name__ == "__main__":
    clk_thread = Thread(target=clock_thread)
    clk_thread.start()

    print("SIM_MODE:", SIM_MODE)
    if not SIM_MODE:
        wait_for_internet()
        led_writer.clear()
        sio.connect(HEROKU_HOSTNAME)
        while True:
            sleep(1.0)
    else:
        sio.connect("http://localhost:5001/")
        led_writer.run()