import argparse
import os
import json
from time import sleep

from src.led_writer import LedWriter



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

    led_writer = LedWriter()
    led_writer.clear()

    with open(filepath, "r") as f:
        data = json.load(f)
        led_writer.write_from_json(data)
                
        """
        led_writer.strip.setPixel(0, 255, 0, 0)
        led_writer.strip.setPixel(55, 0, 255, 0)
        led_writer.strip.setPixel(56, 255, 0, 0)
        led_writer.strip.setPixel(111, 0, 255, 0)
        
        led_writer.strip.setPixel(783, 0, 0, 255)
        led_writer.strip.setPixel(755, 0, 0, 255)
        led_writer.strip.setPixel(727, 0, 0, 255)
        led_writer.strip.show()
        """
        """
        led_writer.strip.setPixel(0, 255, 0, 0)
        led_writer.strip.setPixel(1, 0, 255, 0)
        led_writer.strip.setPixel(2, 0, 0, 255)
        led_writer.strip.setPixel(3, 255, 0, 0)
        led_writer.strip.setPixel(4, 0, 255, 0)
        led_writer.strip.setPixel(5, 0, 0, 255)
        led_writer.strip.setPixel(28+0, 255, 0, 0)
        led_writer.strip.setPixel(28+1, 0, 255, 0)
        led_writer.strip.setPixel(28+2, 0, 0, 255)
        led_writer.strip.setPixel(28+3, 255, 0, 0)
        led_writer.strip.setPixel(28+4, 0, 255, 0)
        led_writer.strip.setPixel(28+5, 0, 0, 255)
        led_writer.strip.setPixel(2*28+0, 255, 0, 0)
        led_writer.strip.setPixel(2*28+1, 0, 255, 0)
        led_writer.strip.setPixel(2*28+2, 0, 0, 255)
        led_writer.strip.setPixel(2*28+3, 255, 0, 0)
        led_writer.strip.setPixel(2*28+4, 0, 255, 0)
        led_writer.strip.setPixel(2*28+5, 0, 0, 255)
        led_writer.strip.show()
        """        
