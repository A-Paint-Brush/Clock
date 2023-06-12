import time


class Hand:
    def __init__(self):
        self.width = 21
        self.height = 195
        self.angle = 0

    def update(self):
        current_time = time.localtime()
        self.angle = 6 * current_time.tm_sec
        self.angle = -self.angle
