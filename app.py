from threading import Thread
from src.led_writer import LedWriter
from flask import Flask
from flask import request
import time
import datetime
import pickle

PORT = 5000
app = Flask(__name__)
BRIGHTNESS = 10

led_writer = LedWriter(BRIGHTNESS)
newest_request_t = 0

# App wide constants
CLEAR_TIME_SECS = 30.0*60.0

def _now_str() -> str:
    now = datetime.datetime.now()
    return now.strftime("%a %I:%M:%S %p")

@app.route("/")
def index():
    print("/ reached")
    return {"status": "OK"}


@app.route("/led", methods=["POST"])
def parse_request():
    """Parse a design and write to the led matrix"""
    print("/led reached")
    try:        
        led_writer.write_from_json(request.json)
        thread = Thread(target=clear_led_thread)
        thread.start()
    except Exception as e:
        print(f"Error parseing /LED request: {e}")
        return {"status": "error", "error": str(e)}
    return {"status": "OK", "error": ""}


@app.route("/shutdown", methods=["GET", "POST"])
def shutdown():
    """Kill the server and exit"""
    print("/shutdown reached")
    led_writer.clear()
    led_writer.cleanup()
    return {"status": "OK"}


def clear_led_thread():
    """Function that clears the led every `CLEAR_TIME_SECS` seconds. Function is blocking so
    should be called in its own thread
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



if __name__ == "__main__":
    print(f"Starting app.py, current time: {_now_str()}")
    app.run(debug=True, port=PORT, use_reloader=False)

