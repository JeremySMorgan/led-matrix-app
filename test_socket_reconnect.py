from time import sleep

import socketio

from src.utils import wait_for_internet, logprint

# Constants
HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"


if __name__ == "__main__":
    wait_for_internet()

    for i in range(5):
        print("trying connection", i)

        sio = socketio.Client()

        @sio.event
        def connect():
            # global am_connected
            # am_connected = True
            logprint("[socket] connected")

        @sio.event
        def connect_error():
            logprint("[socket] failed to connect to server.")

        @sio.event
        def disconnect():
            # global am_connected
            # am_connected = False
            logprint("[socket] Disconnected from server.")


        @sio.on("*")
        def unhandled_event(event, sid, data):
            logprint(f"[socket] caught an unhandled event: '{event}'")

        sio.connect(HEROKU_HOSTNAME)

        sleep(5.0)
        sio.disconnect()
        print("disconnected")