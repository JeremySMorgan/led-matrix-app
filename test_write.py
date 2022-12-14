import argparse
import os
import json

from src.led_writer import LedWriter


led_writer = LedWriter()

""" Example usage

python3 test_write.py --filename=rgb

"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", required=True, type=str)
    args = parser.parse_args()

    filepath = os.path.join("data/", args.filename + ".json")
    assert os.path.isfile(filepath), f"filepath '{filepath}' does not exist"

    with open(filepath, "r") as f:
        data = json.load(f)
        