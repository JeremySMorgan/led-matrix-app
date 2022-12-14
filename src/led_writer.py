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

    def __post_init__(self):
        assert isinstance(self.led_idx, int)
        assert isinstance(self.r, int)
        assert isinstance(self.g, int)
        assert isinstance(self.b, int)
        assert 0 <= self.r <= 255
        assert 0 <= self.g <= 255
        assert 0 <= self.b <= 255


# TODO(@jstmn): Validate this mapping
def xy_to_led_idx(x: int, y: int) -> int:
    """Converts the xy position of a led to the led_number which is
    used to index the buffer
    """
    return BOARD_WIDTH * x + y




class LedWriter:
    def __init__(self, brightness: int = 10):
        self.num_leds = BOARD_WIDTH * BOARD_HEIGHT
        assert brightness >= 0 and brightness <= 31
        self.strip = apa102.APA102(self.num_leds, brightness)

    def clear(self):
        """Clear the led matrix"""
        self.strip.clearStrip()

    def cleanup(self):
        """Clear the led matrix"""
        self.strip.cleanup()

    def write(
        self,
        cells: List[Cell],
        debug_timing: bool = False,
        save_buffer: bool = True,
    ):
        """Write to the led matrix."""
        # TODO(@jstmn): Write colors by each led's x/y position
        # TODO(@jstmn): Speed up write time by setting pixel buffer
        # in a single call, using numpy or something
        # TODO(@jstmn): Write list of cells that don't start at index 0
        t0 = time()
        for cell in cells:
            assert isinstance(cell, Cell)
            self.strip.setPixel(cell.led_idx, cell.r, cell.b, cell.g)
            # self.strip.setPixelRGB(cell.led_idx, cell.color)

        if debug_timing:
            print("strip.setPixel():", time() - t0)

        t0 = time()
        self.strip.show(save_buffer=save_buffer)
        if debug_timing:
            print("strip.show():    ", time() - t0)


    def write_from_json(self, json_data: Dict):
        """Parse a json of rgb values and write to the led matrix. json format:

            {
                {}
            }

        """
        colors = []
        for idx, data in enumerate(json_data["data"]):
            # TODO(@jstmn): Get led_idx from x, y
            #led_idx = xy_to_led_idx(int(data["x"]), int(data["y"]))
            led_idx = idx
            cell = Cell(
                r=int(data["r"]),
                g=int(data["g"]),
                b=int(data["b"]),
                led_idx=led_idx,
            )
            colors.append(cell)
        return colors