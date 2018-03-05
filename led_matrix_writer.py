import apa102

class LedWriter(object):
    
    def __init__(self):
        self.num_leds = 28*28
        self.strip = apa102.APA102(self.num_leds)
        self.colors = None
    
    def parse_request(self, value_str):
        print "\n"
        value_str = str(value_str)
        value_str = value_str.replace("\n","")
        value_str = value_str.replace("\"","")
        value_str = value_str.replace("\'","")
        value_str = value_str.replace(", u'')])])","")
        value_str = value_str.replace("]}, u)])])","")
        value_str = value_str.replace("CombinedMultiDict([ImmutableMultiDict([]), ImmutableMultiDict([({paramName:[","")
        value_list = value_str.split(",")
        colors = []
        for item in value_list:
            color = self.color_from_str(item)
            colors.append(color)
        return colors
        
    def save_colors(self,colors):
        self.colors = colors
        
    def write_saved_colors(self):
        if self.colors:
            self.set_colors(self.colors)
    
    
    def color_from_str(self,str_):
    
        if "tr" in str_:
            return self.strip.combineColor(0,0,0)
    
        elif "rgb" in str_:
            s = str_.replace("(","")
            s = s.replace(")","")
            s = s.replace("{","")
            s = s.replace("}","")
            s = s.replace("'","")
            s = s.replace("r","")
            s = s.replace("'","")
            s = s.replace("\'","")
            s = s.replace("g","")
            s = s.replace("b","")
            s_list = s.split(".")
            r = int(s_list[0])
            g = int(s_list[1])
            b = int(s_list[2])
            return self.strip.combineColor(r,g,b)
        else:
            print "error: str_:",str_," not recognized"
            
    def set_colors(self,colors):
        
        i = 0;
        for color in colors:
            self.strip.setPixelRGB(i, color)
            i += 1
        
        self.strip.show()

    
    
    
    
