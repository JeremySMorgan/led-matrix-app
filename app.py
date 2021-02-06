from threading import Thread
from led_matrix_writer import LedWriter
from flask import Flask
from flask import request
import time
import psutil
import datetime


app = Flask(__name__)
led_writer = LedWriter()
newest_request_t = 0

# App wide constants
CLEAR_TIME_SECS = 30.0*60.0

@app.route("/")
def index():
    print(request.data)
    return "RPi online"

@app.route('/LED', methods=['POST'])
def parse_request():
    
    print("\n parsing request to \\LED")
    
    try:
        colors = led_writer.parse_request(request.json)
        led_writer.save_colors(colors)
        led_writer.set_colors (colors)
        thread = Thread(target=clear_led_thread)
        thread.start()
        #thread.join()
        
    except Exception as e:
        print("error: ", e.message)
        return 'Error parsing request'
        
    return 'OK'

@app.route('/shutdown', methods=['GET', 'POST'])
def shutdown():
    print("shutdown called")
    led_writer.clear_colors()
    #PROCNAME = "ngrok" 
    #for proc in psutil.process_iter():
    #    if proc.name() == PROCNAME:
    #        proc.kill()
    return 'shutdown'

def clear_led_thread():
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
        #app.run(debug=True)
        
        while True:
            time.sleep(.25)
            print(f"in app.py (started at: {now_str})")
    except Exception:
        print("Socket already in use, exiting()")
 
