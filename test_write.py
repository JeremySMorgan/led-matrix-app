import argparse
import os
import json

from src.led_writer import LedWriter



""" Example usage

python test_write.py --filename=rgb
python test_write.py --filename=led_matrix_data_empty
python test_write.py --filename=red_check

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
