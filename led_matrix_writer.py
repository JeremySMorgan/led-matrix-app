import apa102

BOARD_WIDTH = 28
BOARD_HEIGHT = 28

class LedWriter(object):
    
    def __init__(self):
        self.num_leds = BOARD_WIDTH*BOARD_HEIGHT
        self.strip = apa102.APA102(self.num_leds)
        self.colors = None
    
    def parse_request(self, req_json):
        
        colors = []
        for cell in req_json["data"]:
            rgb = [cell["r"], cell["g"], cell["b"]]
            color = self.color_from_rgb(rgb)
            colors.append(color)
        return colors
    
    def clear_colors(self):
        self.strip.clearStrip()
    
    def save_colors(self,colors):
        self.colors = colors
        
    def write_saved_colors(self):
        if self.colors:
            self.set_colors(self.colors)
    
    def color_from_rgb(self, rgb):
        return self.strip.combineColor(rgb[0], rgb[1], rgb[2])
            
    def set_colors(self,colors):
        i = 0;
        for color in colors:
            self.strip.setPixelRGB(i, color)
            i += 1
        
        self.strip.show()

