from typing import List, Tuple
import apa102

BOARD_WIDTH = 28
BOARD_HEIGHT = 28

class LedWriter(object):
    
    def __init__(self):
        self.num_leds = BOARD_WIDTH*BOARD_HEIGHT
        self.strip = apa102.APA102(self.num_leds)

    def parse_request(self, req_json) -> List[int]:
        """ Parse a json of rgb values, returns a list of colors
        """
        colors = []
        for cell in req_json["data"]:
            rgb = [cell["r"], cell["g"], cell["b"]]
            color = self.color_from_rgb(rgb)
            colors.append(color)
        return colors
    
    def clear_colors(self):
        """ Clear the led matrix
        """
        self.strip.clearStrip()
    
    def color_from_rgb(self, rgb: Tuple[int, int, int]) -> int:
        return self.strip.combineColor(rgb[0], rgb[1], rgb[2])
            
    def write_colors(self, colors: List[int]):
        """ Write the colors to the led matrix. 
        """
        # TODO(@jeremysm): Write colors by each led's x/y position
        i = 0
        for color in colors:
            self.strip.setPixelRGB(i, color)
            i += 1
        self.strip.show()

