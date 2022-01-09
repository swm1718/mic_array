# Adapted from alexa_led_pattern.py at https://github.com/respeaker/4mics_hat/blob/master/interfaces/alexa_led_pattern.py

import time

class DOALEDPattern(object):
    def __init__(self, show=None, number=12):
        self.pixels_number = number
        self.pixels = [0] * 4 * number

        if not show or not callable(show):
            def dummy(data):
                pass
            show = dummy

        self.show = show
        self.stop = False

    def wakeup(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number

        pixels = [0, 24, 0, 24, 0, 0, 24, 0] * (self.pixels_number/2)
        #pixels[position * 4 + 2] = 48

        self.show(pixels)

    def listen(self, direction=0):
        position = int((direction + 15) / (360 / self.pixels_number)) % self.pixels_number
        
        pixels = [0, 0, 0, 0] * self.pixels_number
        pixels[position * 4 + 2] = 48
        pixels[(position-1)%self.pixels_number * 4 + 2] = 12
        pixels[(position+1)%self.pixels_number * 4 + 2] = 12
        
        self.show(pixels)

#     def think(self):
#         pixels  = [0, 0, 12, 12, 0, 0, 0, 24] * self.pixels_number

#         while not self.stop:
#             self.show(pixels)
#             time.sleep(0.2)
#             pixels = pixels[-4:] + pixels[:-4]

#     def speak(self):
#         step = 1
#         position = 12
#         while not self.stop:
#             pixels  = [0, 0, position, 24 - position] * self.pixels_number
#             self.show(pixels)
#             time.sleep(0.01)
#             if position <= 0:
#                 step = 1
#                 time.sleep(0.4)
#             elif position >= 12:
#                 step = -1
#                 time.sleep(0.4)

#             position += step

    def off(self):
        self.show([0] * 4 * 12)
