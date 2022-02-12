from threading import Thread
from src.led_writer import LedWriter
from flask import Flask
from flask import request
import time
import datetime

app = Flask(__name__)
led_writer = LedWriter()
newest_request_t = 0

# App wide constants
#CLEAR_TIME_SECS = 30.0*60.0
CLEAR_TIME_SECS = 10

@app.route("/")
def index():
    """ / Endpoint 
    """
    print("/ reached")
    return {"status": "OK"}

@app.route('/LED', methods=['POST'])
def parse_request():
    """ Parse a design and write to the led matrix
    """
    print("/LED reached")
    try:
        colors = led_writer.parse_request(request.json)
        led_writer.write_colors(colors)
        thread = Thread(target=clear_led_thread)
        thread.start()
    except Exception as e:
        print("Error parseing /LED request: {e}")
        return {"status": "error"}
    return {"status": "OK"}

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    """ Kill the server and exit
    """
    print("/shutdown reached")
    led_writer.clear_colors()
    # TODO(@jeremysm): exit app when reached
    return {"status": "OK"}
    
def clear_led_thread():
    """ Function that clears the led every `CLEAR_TIME_SECS` seconds. Function is blocking so
    should be called in its own thread
    """
    global newest_request_t
    request_t = time.time()
    newest_request_t = request_t
    time.sleep(CLEAR_TIME_SECS)
    if newest_request_t == request_t:
        print("clearing colors")
        led_writer.clear_colors()
    else:
        print("new request recieved during sleeping period")
    
def _now_str() -> str:
    now = datetime.datetime.now()
    return now.strftime('%a %I:%M:%S %p')
    
    
if __name__ == "__main__":

    print(f"Starting app.py, current time: {_now_str()}")
    app.run(debug=True, use_reloader=False)
    #try:
    #    
    #except Exception as e:
    #    print(f"Error running app: {e}")
