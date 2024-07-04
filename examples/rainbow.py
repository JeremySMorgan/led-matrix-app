import sys
import os

sys.path.append(os.getcwd())
from src import apa102


# numPixels = 432-73 # 1/2 Strip plus one LED is broken
NUM_PIXLES = 28 * 28

"""
Now for the actual rainbow cycle algorithm
"""
try:

    strip = apa102.APA102(NUM_PIXLES, 0)  # Low brightness (2 out of max. 31)
    while True:  # Loop forever
        for j in range(NUM_PIXLES << 8):  # Shift the start of the rainbow across the strip
            for i in range(NUM_PIXLES):  # spread (or compress) one rainbow onto the strip
                # For a faster shift, add more than 1 * j per loop (e.g. + 2 * j)
                index = strip.wheel((((i << 8) // NUM_PIXLES) + j * 4) & 255)
                strip.setPixelRGB(i, index)
            strip.show()

except KeyboardInterrupt:  # Abbruch...
    print("Interrupted...")
    strip.clearStrip()
    print("Strip cleared")
    strip.cleanup()
    print("SPI closed")
