import time
import os
import sys

sys.path.append(os.getcwd())
from src import apa102

try:
    num_leds = 28 * 28
    strip = apa102.APA102(num_leds)
    head = 1
    color = strip.combineColor(255, 0, 0)

    while True:  # Loop forever
        strip.setPixelRGB(head, color)  # Turn on 'head' pixel
        strip.show()  # Refresh strip
        time.sleep(1)

except KeyboardInterrupt:  # Abbruch...
    print("Interrupted...")
    strip.clearStrip()
    print("Strip cleared")
    strip.cleanup()
    print("SPI closed")
