#!/usr/bin/env python

import time
from led_matrix_writer import LedWriter
led_writer = LedWriter()

led_writer.clear_colors()

RED = led_writer.color_from_rgb([255, 0, 0])
colors = [RED]
    
while True:
    
    
    led_writer.set_colors(colors)
    
    colors.append(RED)
    #led_writer.clear_colors()
    time.sleep(.1)
    print(len(colors))
    
    
