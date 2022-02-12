from threading import Thread
from src.led_writer import LedWriter, parse_http_data
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
# CLEAR_TIME_SECS = 30.0*60.0
CLEAR_TIME_SECS = 10

def _now_str() -> str:
    now = datetime.datetime.now()
    return now.strftime("%a %I:%M:%S %p")

@app.route("/")
def index():
    """/ Endpoint"""
    print("/ reached")
    return {"status": "OK"}


@app.route("/LED", methods=["POST"])
def parse_request():
    """Parse a design and write to the led matrix"""
    print("/LED reached")
    try:
        # Save requests
        with open("example_requests/request_" + _now_str() + ".pickle", "wb") as f:
            import pickle
            pickle.dump(request.json, f)
        
        cells = parse_http_data(request.json)
        led_writer.write(cells)
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
        print("clearing colors")
        led_writer.clear()
    else:
        print("new request recieved during sleeping period")



if __name__ == "__main__":

    print(f"Starting app.py, current time: {_now_str()}")
    app.run(debug=True, port=PORT, use_reloader=False)

