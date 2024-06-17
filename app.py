from threading import Thread
from time import time, sleep
import json
from datetime import datetime
import os

import socketio

from src.utils import wait_for_internet, logprint
from src.led_writer import LedWriter, LedWriterSim


# SIM_MODE = True
SIM_MODE = False

# Constants
HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"

BRIGHTNESS = 10
CLEAR_TIME_SECS = 15.0*60.0 # Clear led matrix 15 minutes after a new design is received
# CLEAR_TIME_SECS = 10

# TODO: there is an issue where the server doesn't reconnect when the internet goes down, or something like that. should 
# always check to see if a connection is maintained, and try to reconnect if not. 
# TODO also: - show a green square when connected, red square when disconnected
# TODO: quit if another app.py process is running

if not SIM_MODE:
    led_writer = LedWriter(BRIGHTNESS)
else:
    led_writer = LedWriterSim()

sio = socketio.Client()

newest_request_t = 0
board_is_active = False
was_disconnected = False

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
        logprint("clear_led_thread(): clearing board")
        led_writer.clear()
        led_writer.stop_cgl()
        board_is_active = False
    else:
        logprint("clear_led_thread(): new request recieved during sleeping period, exiting with noops performed")


def indicate_alive_thread():
    dir_path = '/home/jm/Desktop/led-matrix-app/is_alive'
    prefix = 'iaa' # 'is alive at'
    logprint(f"[INFO] starting indicate_alive_thread() to indicate liveliness")

    while True:
        # delete all directories with prefix
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        for file in files:
            if file[0:len(prefix)] == prefix:
                os.remove(os.path.join(dir_path, file))
        now_str = datetime.now().strftime('%d:%m:%Y__%H:%M:%S')
        new_file = os.path.join(dir_path, f'{prefix}__{now_str}')
        open(new_file, "w").close()
        sleep(1)


@sio.event
def connect():
    logprint("[socket] connected")

@sio.event
def connect_error():
    logprint('[socket] failed to connect to server.')

@sio.event
def disconnect():
    global was_disconnected
    was_disconnected = True
    logprint('[socket] Disconnected from server.')


@sio.on("led-design")
def message_received(message):
    logprint("[socket] received message")
    request_json = json.loads(message)
    # with open("data/cgl.json", "w") as json_file:
    #     json.dump(request_json, json_file)
    led_writer.write_from_json(request_json)
    thread = Thread(target=clear_led_thread, args=(CLEAR_TIME_SECS, ))
    thread.start()
    return {"status": "OK", "error": ""}


@sio.on('*')
def unhandled_event(event, sid, data):
    logprint(f"[socket] caught an unhandled event: '{event}'")


""" Example usage

source /home/jm/Desktop/led-matrix-app/venv/bin/activate && python3 /home/jm/Desktop/led-matrix-app/app.py
"""

if __name__ == "__main__":

    print("\n=====", flush=True)
    logprint(f"[socket] started server")
    show_is_alive_thread = Thread(target=indicate_alive_thread)
    show_is_alive_thread.start()

    clk_thread = Thread(target=clock_thread)
    clk_thread.start()

    logprint(f"SIM_MODE: {SIM_MODE}")
    if not SIM_MODE:

        while True:
            wait_for_internet()
            was_disconnected = False
            led_writer.clear()
            sio.connect(HEROKU_HOSTNAME)
            while True:
                sleep(1.0)
                if was_disconnected:
                    logprint("[socket] detected that socket was disconnected. Attempting to reconnect")
    else:
        sio.connect("http://localhost:5001/")
        led_writer.run()