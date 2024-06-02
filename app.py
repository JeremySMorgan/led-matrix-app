from threading import Thread
from time import time, sleep
import json
from datetime import datetime
import os

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
# CLEAR_TIME_SECS = 10

# TODO: there is an issue where the server doesn't reconnect when the internet goes down, or something like that. should 
# always check to see if a connection is maintained, and try to reconnect if not. 
# TODO also: - show a green square when connected, red square when disconnected
# TODO: quit if another app.py process is running

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


def indicate_alive_thread():
    dir_path = '/home/jm/Desktop/led-matrix-app/is_alive'
    prefix = 'iaa' # 'is alive at'
    print(f"[INFO] starting indicate_alive_thread() to indicate liveliness")

    while True:
        # delete all directories with prefix
        dirs = [f for f in os.listdir(dir_path) if os.path.isdir(os.path.join(dir_path, f))]
        for subdir in dirs:
            if subdir[0:len(prefix)] == prefix:
                # rmdir is safe in that it won't delete a non empty directory - an error if dir contains files 
                # 'OSError: [Errno 39] Directory not empty'
                os.rmdir(os.path.join(dir_path, subdir))
        now_str = datetime.now().strftime('%d:%m:%Y__%H:%M:%S')
        new_dir = os.path.join(dir_path, f'{prefix}__{now_str}/')
        os.mkdir(new_dir)
        sleep(1)


@sio.event
def connect():
    print("[INFO] connected")

@sio.event
def connect_error():
    print('[INFO] Failed to connect to server.')

@sio.event
def disconnect():
    print('[INFO] Disconnected from server.')


@sio.on("led-design")
def message_received(message):
    print("[INFO] received message")
    request_json = json.loads(message)
    # with open("data/cgl.json", "w") as json_file:
    #     json.dump(request_json, json_file)
    led_writer.write_from_json(request_json)
    thread = Thread(target=clear_led_thread, args=(CLEAR_TIME_SECS, ))
    thread.start()
    return {"status": "OK", "error": ""}


@sio.on('*')
def unhandled_event(event, sid, data):
    print("[INFO] caught an unhandled event")


""" Example usage

source /home/jm/Desktop/led-matrix-app/venv/bin/activate && python3 /home/jm/Desktop/led-matrix-app/app.py
"""

if __name__ == "__main__":

    print(f"\n[INFO] started server at {datetime.now()}")
    show_is_alive_thread = Thread(target=indicate_alive_thread)
    show_is_alive_thread.start()

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