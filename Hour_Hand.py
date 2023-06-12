import time


class Hand:
    def __init__(self):
        self.width = 21
        self.height = 195
        self.angle = -5
        self.hour_angle = 30 / 60

    def update(self):
        current_time = time.localtime()
        self.angle = 30 * current_time.tm_hour + self.hour_angle * current_time.tm_min
        if self.angle > 360:
            self.angle -= 360
        self.angle = -self.angle
