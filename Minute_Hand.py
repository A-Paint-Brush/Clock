import time


class Hand:
    def __init__(self):
        self.width = 21
        self.height = 117
        self.angle = 0
        self.minute_angle = 6 / 60

    def update(self):
        current_time = time.localtime()
        self.angle = 6 * current_time.tm_min + self.minute_angle * current_time.tm_sec
        self.angle = -self.angle
