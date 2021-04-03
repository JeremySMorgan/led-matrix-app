from threading import Thread
from led_matrix_writer import LedWriter
from flask import Flask
from flask import request
import time
import datetime

app = Flask(__name__)
led_writer = LedWriter()
newest_request_t = 0

# App wide constants
CLEAR_TIME_SECS = 30.0*60.0

@app.route("/")
def index():
    print(request.data)
    return "OK"

@app.route('/LED', methods=['POST'])
def parse_request():
    
    print("\n parsing request to \\LED")
    
    try:
        colors = led_writer.parse_request(request.json)
        led_writer.write_colors(colors)
        thread = Thread(target=clear_led_thread)
        thread.start()
        
    except Exception as e:
        print("error: ", e.message)
        return 'Error parsing request'
        
    return "OK"

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    print("shutdown called")
    led_writer.clear_colors()
    return 'shutdown'

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
    
if __name__ == "__main__":

    now = datetime.datetime.now()
    now_str = now.strftime('%a %I:%M:%S %p')
    print(f"starting app.py at: {now_str}")
        
    try:
        app.run(debug=True)
    except Exception:
        print("Socket already in use, exiting()")
 
