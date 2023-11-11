from dataclasses import dataclass
from typing import List, Tuple, Dict
from src import apa102
from time import time

BOARD_WIDTH = 28
BOARD_HEIGHT = 28


@dataclass
class Cell:
    r: int
    g: int
    b: int
    led_idx: int

    @property
    def color(self) -> int:
        return (self.r << 16) + (self.g << 8) + self.b

    def set_blank(self):
        self.r = 0
        self.g = 0
        self.b = 0

    #def __post_init__(self):
    #    assert isinstance(self.led_idx, int)
    #    assert isinstance(self.r, int)
    #    assert isinstance(self.g, int)
    #    assert isinstance(self.b, int)
    #    assert 0 <= self.r <= 255
    #    assert 0 <= self.g <= 255
    #    assert 0 <= self.b <= 255


def xy_to_led_idx(x: int, y: int) -> int:
    """Converts the xy position of a led to the led_number which is
    used to index the buffer
    
    Led matrix numbering format:
    
        0  1  2  ... 26 27
        55 54 53 ... 29 28
        56 57 58 ... 59 60
        88 87 86 ... 62 61
        ...
        783 782  ...   756
    
    Coordinate system:
    
        +y
        ^
        |
        |
        |
        .-----> +x
      
    """
    y_inv = BOARD_HEIGHT - y - 1
    x_mod = x % BOARD_WIDTH
    n0 = y_inv * BOARD_HEIGHT
    if y_inv == 0 or y_inv % 2 == 0:
        n = n0 + x_mod
    else:
        n = n0 + (BOARD_WIDTH - x_mod - 1)
    return n



class LedWriter:
    def __init__(self, brightness: int = 10):
        assert 0 < brightness <= 31
        self.num_leds = BOARD_WIDTH * BOARD_HEIGHT
        self.strip = apa102.APA102(self.num_leds, brightness)

    def clear(self):
        """Clear the led matrix"""
        self.strip.clearStrip()

    # TODO(@jstmn): Speed up write time by setting pixel buffer in a 
    # single call, using numpy or something
    def write(self, cells: List[Cell], debug_timing: bool = False):
        """Write to the led matrix.
        """
        self.strip.reset_buffer()
        
        t0 = time()
        for cell in cells:
            assert isinstance(cell, Cell)
            self.strip.setPixel(cell.led_idx, cell.r, cell.g, cell.b)
            # self.strip.setPixelRGB(cell.led_idx, cell.color)

        if debug_timing:
            print("strip.setPixel():", time() - t0)

        t0 = time()
        self.strip.show()
        if debug_timing:
            print("strip.show():    ", time() - t0)

    def update_buffer(self, cells):
        for cell in cells:
            assert isinstance(cell, Cell)
            self.strip.setPixel(cell.led_idx, cell.r, cell.b, cell.g)

    def write_from_json(self, json_data: Dict):
        """Parse a json of rgb values and write to the led matrix. json format:
            { "data": [
                {"r":0,"g":0,"b":0,"a":0,"x":0,"y":0},
                ...
                {"r":0,"g":0,"b":0,"a":0,"x":27,"y":27}
                ]
            }
        """
        self.clear()
        colors = []
        for idx, data in enumerate(json_data["data"]):
            r = int(data["r"])
            g = int(data["g"])
            b = int(data["b"])
            if r > 0 or g > 0 or b > 0:
                led_idx = xy_to_led_idx(int(data["x"]), int(data["y"]))
                assert 0 <= led_idx < BOARD_HEIGHT * BOARD_WIDTH, f"invalid led_idx={led_idx} (max allowed = {BOARD_HEIGHT}*{BOARD_WIDTH} = {BOARD_HEIGHT * BOARD_WIDTH})"
                cell = Cell(r=r, g=g, b=b, led_idx=led_idx)
                colors.append(cell)
        self.write(colors)

if __name__ == "__main__":
    writer = LedWriter()
    

