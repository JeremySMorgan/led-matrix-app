import os
import sys
sys.path.append(os.getcwd())
from src import apa102

try:
    num_leds = 28*28
    strip = apa102.APA102(num_leds)
    head = -9  # Index of first 'on' pixel
    tail = -19  # Index of last 'off' pixel
    color = 0xFF0000  # 'On' color (starts red)

    while True:  # Loop forever
        
        strip.setPixelRGB(head, color)  # Turn on 'head' pixel
        strip.setPixelRGB(tail, 0)  # Turn off 'tail'
        strip.show()  # Refresh strip
        
        head += 1  # Advance head position
        if(head >= num_leds):  # Off end of strip?
            head = 0  # Reset to start
            color >>= 8  # Red->green->blue->black
            if(color == 0): color = 0xFF0000  # If black, reset to red

        tail += 1  # Advance tail position
        if(tail >= 432): 
            tail = 0  # Off end? Reset


except KeyboardInterrupt:  # Abbruch...
    print('Interrupted...')
    strip.clearStrip()
    print('Strip cleared')
    strip.cleanup()
    print('SPI closed')
