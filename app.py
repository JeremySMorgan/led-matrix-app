from threading import Thread
import time

from src.utils import wait_for_internet, send_json_post
from src.ngrok_manager import NgrokManager
from src.led_writer import LedWriter

from flask import Flask
from flask import request

app = Flask(__name__)

# Constants
PORT = 5001
HEROKU_HOSTNAME = "http://jeremysmorgan.herokuapp.com"

NGROK_CYCLE_TIME_SEC = 15*60  # Change url every 30 minutes
UPDATE_HEROKU_HOSTNAME_URL = f"{HEROKU_HOSTNAME}/update_rpi_hypervisor_address"
UPDATE_HEROKU_HOSTNAME_INTERVAL = 5

BRIGHTNESS = 10
CLEAR_TIME_SECS = 15.0*60.0 # Clear led matrix 15 minutes after a new design is received

ngrok_manager = NgrokManager(PORT)
ngrok_manager.start_tunnel()

led_writer = LedWriter(BRIGHTNESS)
newest_request_t = 0
exit_update_hostname_thread = False
exit_update_ngrok_url_thread = False


def update_ngrok_url_thread():
    """ Update the exposed ngrok url
    """
    global exit_update_ngrok_url_thread, ngrok_manager
    while True:
        time.sleep(NGROK_CYCLE_TIME_SEC)
        print("Updating ngrok url")
        print("current hostname:", ngrok_manager.get_public_hostname())
        ngrok_manager.stop_tunnel()
        ngrok_manager.start_tunnel()
        print("new hostname:    ", ngrok_manager.get_public_hostname())
        if exit_update_ngrok_url_thread:
            break


def update_heroku_known_hostnames_thread():
    """ Update the heroku server with the known app & hypervisor public 
    ngrok addresses
    """
    global exit_update_hostname_thread
    while True:
        if ngrok_manager.get_public_hostname() is None:
            time.sleep(0.1)
            continue
        data = {"HOSTNAME": ngrok_manager.get_public_hostname()}
        res = send_json_post(UPDATE_HEROKU_HOSTNAME_URL, data, verbose=False)
        time.sleep(UPDATE_HEROKU_HOSTNAME_INTERVAL)
        if exit_update_hostname_thread:
            break


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


@app.route('/led', methods=['POST'])
def parse_request():
    try:
        led_writer.write_from_json(request.json)
        thread = Thread(target=clear_led_thread)
        thread.start()
    except Exception as e:
        print(f"Error parseing /LED request: {e}")
        return {"status": "ERROR", "error": str(e)}
    return {"status": "OK", "error": ""}


"""" Example usage

python3.6 /home/pi/Desktop/led-matrix-app/app.py
"""


if __name__ == "__main__":
    wait_for_internet()
    
    thread = Thread(target=update_heroku_known_hostnames_thread)
    thread.start()
    
    ngrok_thread = Thread(target=update_ngrok_url_thread)
    ngrok_thread.start()
    
    led_writer.clear()
    try:
        app.run(debug=True, port=PORT, use_reloader=False)
    except KeyboardInterrupt:
        print("Keyboard interrupt caught, shutting down")
        exit_update_hostname_thread = True
        exit_update_ngrok_url_thread = True

        print("Shutting down ngrok_manager")
        ngrok_manager.stop_tunnel()

