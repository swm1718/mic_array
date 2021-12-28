# Adapted from https://github.com/respeaker/4mics_hat/blob/master/interfaces/pixels.py

import apa102
import time
import threading
from gpiozero import LED
try:
    import queue as Queue
except ImportError:
    import Queue as Queue

from doa_led_pattern import DOALEDPattern
    
class Pixels:
    PIXELS_N = 12

    def __init__(self, pattern=DOALEDPattern):
        self.pattern = pattern(show=self.show)

        self.dev = apa102.APA102(num_led=self.PIXELS_N)
        
        self.power = LED(5)
        self.power.on()

        self.queue = Queue.Queue()
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()

        self.last_direction = None

    def wakeup(self, direction=0):
        self.last_direction = direction
        def f():
            self.pattern.wakeup(direction)

        self.put(f)

    def listen(self):
        if self.last_direction:
            def f():
                self.pattern.wakeup(self.last_direction)
            self.put(f)
        else:
            def f():
                self.pattern.listen(self.last_direction)
            self.put(f)

    def think(self):
        self.put(self.pattern.think)

    def speak(self):
        self.put(self.pattern.speak)
        
    def set_direction(self, direction):
        self.last_direction = direction

    def off(self):
        self.put(self.pattern.off)

    def put(self, func):
        self.pattern.stop = True
        self.queue.put(func)

    def _run(self):
        while True:
            func = self.queue.get()
            self.pattern.stop = False
            func()

    def show(self, data):
        for i in range(self.PIXELS_N):
            self.dev.set_pixel(i, int(data[4*i + 1]), int(data[4*i + 2]), int(data[4*i + 3]))

        self.dev.show()


pixels = Pixels()


if __name__ == '__main__':
    
    pixels.wakeup()
    time.sleep(3)
        
    while True:

        try:
            print("looping")
            pixels.listen()
            time.sleep(1)
        except KeyboardInterrupt:
            break


    pixels.off()
    time.sleep(1)
