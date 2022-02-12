#!/usr/bin/env python
import time
import os
import sys
from math import sin, cos, pi

sys.path.append(os.getcwd())
from src.led_writer import LedWriter, Cell


def main(led_writer: LedWriter):

    led_writer.clear_colors()
    colors = []
    n_leds = led_writer.num_leds
    counter = 0

    while True:

        i = counter % n_leds
        r = 0  # 128 +128 * sin(i * 2*pi/n_leds)
        g = 256 * (cos(i * 2 * pi / n_leds + 2 * pi / 3) ** 2)
        b = 0
        color = Cell(r=int(r), g=int(g), b=int(b), x=0, y=0)
        print(color)
        colors.append(color)

        led_writer.write_colors(colors)
        colors.append(color)

        counter += 1
        time.sleep(0.001)


if __name__ == "__main__":

    led_writer = LedWriter()

    try:
        main(led_writer)
    except KeyboardInterrupt:
        led_writer.clear_colors()
