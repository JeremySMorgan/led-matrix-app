#!/usr/bin/env python
import threading
from led_matrix_writer import LedWriter
from flask import Flask
from flask import request
import time
app = Flask(__name__)
led_writer = LedWriter()

@app.route("/")
def hello():
    print request.data
    return "Hello World!"

@app.route('/LED', methods=['GET', 'POST'])
def parse_request():
    colors = led_writer.parse_request(request.values)
    led_writer.save_colors(colors)
    led_writer.set_colors(colors)
    return 'OK'

def loop_thread():
    delay = .08
    sum_t = 0
    t=0
    while t < sum_t:
        led_writer.write_saved_colors()
        time.sleep(delay)
        t += delay
        if (t - int(t)) <.1:
            print int(t)
 
if __name__ == "__main__":
    thread_ = threading.Thread(group=None, target=loop_thread,name="XASDF")
    thread_.start()
    app.run(debug=True)
 
