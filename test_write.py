import argparse
import os
import json
from time import sleep
from math import floor

from src.led_writer import LedWriter, Cell, N_LEDS_PER_DIM

NUM_PIXLES = 28*28



def snake():

    for i in range(28*28):
        x = i
        y = N_LEDS_PER_DIM - 2 - floor(i / N_LEDS_PER_DIM)
        cells = [Cell(
            r=0,
            g=255,
            b=255,
            x=x,
            y=y
        )]
        led_writer.write(cells)
    exit()


""" Example usage

python test_write.py --filename=cgl
python test_write.py --filename=rgb
python test_write.py --filename=led_matrix_data_empty
python test_write.py --filename=red_check
python test_write.py --filename=axes
python test_write.py --filename=snake

"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", required=True, type=str)
    args = parser.parse_args()

    led_writer = LedWriter()
    led_writer.clear()

    if args.filename == "snake":
        snake()

    filepath = os.path.join("data/", args.filename + ".json")
    assert os.path.isfile(filepath), f"filepath '{filepath}' does not exist"

    with open(filepath, "r") as f:
        data = json.load(f)
        led_writer.write_from_json(data)

        sleep(10.0)
        led_writer.clear()

        # i = 15
        # j = 5
        # color = led_writer.strip.wheel(
        #             (((i << 8) // NUM_PIXLES) + j * 4) & 255
        #         )
        #led_writer.strip.setPixelRGB(25, color)
        #led_writer.strip.show()
