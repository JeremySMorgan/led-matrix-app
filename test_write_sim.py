import argparse
import os
import json
from time import sleep

from src.led_writer import LedWriter

NUM_PIXLES = 28*28

""" Example usage

python test_write.py --filename=rgb
python test_write.py --filename=led_matrix_data_empty
python test_write.py --filename=red_check
python test_write.py --filename=axes

"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", required=True, type=str)
    args = parser.parse_args()

    filepath = os.path.join("data/", args.filename + ".json")
    assert os.path.isfile(filepath), f"filepath '{filepath}' does not exist"

    led_writer = LedWriter(sim_mode=True)
    led_writer.clear()

    with open(filepath, "r") as f:
        data = json.load(f)
        led_writer.write_from_json(data)

        sleep(1.0)
        led_writer.clear()
            
        i = 15
        j = 5
        color = led_writer.strip.wheel(
                    (((i << 8) // NUM_PIXLES) + j * 4) & 255
                )
        #led_writer.strip.setPixelRGB(25, color)
        #led_writer.strip.show()
