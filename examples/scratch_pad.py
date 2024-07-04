#!/usr/bin/env python
from time import time, sleep

import os
import sys
from math import sin, cos, pi

sys.path.append(os.getcwd())
from src.led_writer import LedWriter, Cell

BRIGHTNESS = 15
# 128 +128 * sin(led_idx * 0.1*pi/n_leds)


def main(led_writer: LedWriter):

    led_writer.clear()
    n_leds = led_writer.num_leds
    n = 10
    cells = [Cell(x=0, y=0, r=0, g=0, b=0, led_idx=i) for i in range(n_leds)]

    # Write color
    for led_idx in range(255):
        cells[led_idx].r = 255 if (led_idx % 3) == 0 else 0
        cells[led_idx].g = 255 if ((led_idx + 1) % 3) == 0 else 0
        # cells[led_idx].b = 255 if ((led_idx +2) % 3) == 0 else 0

    write_idx_0 = 15
    write_idx_f = 25
    write_cells = cells[write_idx_0:write_idx_f]

    print("Going to write cells:")
    for cell in write_cells:
        print("  ", cell)

    print()
    print("Buffer before write")
    led_writer.strip.print_buffer(n=n)

    led_writer.write(write_cells, debug_timing=False)

    #
    print()
    print("Buffer after write")
    led_writer.strip.print_buffer(n=n)


if __name__ == "__main__":

    led_writer = LedWriter(brightness=BRIGHTNESS)

    main(led_writer)

    sleep(10)
    print("Done - Clearing leds")
    led_writer.clear()
    led_writer.cleanup()
