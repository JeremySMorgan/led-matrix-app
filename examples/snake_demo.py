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

    snake_length = 150
    tail = -snake_length

    cells = [
        Cell(x=0, y=0, r=0, g=0, b=0, led_idx=i) for i in range(n_leds)
    ]

    while True:

        if tail - 1 >= 0:
            cells[tail - 1].set_blank()

        for i in range(snake_length):
            led_idx = (tail + i) % n_leds
            if led_idx < 0:
                continue
            r = 0
            g = 0
            b = 128 + 128 * sin(led_idx / n_leds * 5 * 2 * pi)
            cells[led_idx].r = int(r)
            cells[led_idx].g = int(g)
            cells[led_idx].b = int(b)

        write_idx_0 = max(0, tail - 1)
        write_idx_f = tail + snake_length
        write_cells = cells[write_idx_0:write_idx_f]
        led_writer.write(write_cells, debug_timing=False)
        if len(write_cells) > 0:
            print(write_cells[-1])

        tail += 1
        if tail == n_leds:
            tail = 0


if __name__ == "__main__":

    led_writer = LedWriter(brightness=BRIGHTNESS)

    try:
        main(led_writer)
    except KeyboardInterrupt:
        led_writer.clear()
        led_writer.cleanup()
