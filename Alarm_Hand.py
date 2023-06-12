class Hand:
    def __init__(self):
        self.width = 21
        self.height = 195
        self.angle = 0
        self.positive_angle = 0

    def rotate(self):
        self.positive_angle += 5
        if self.positive_angle == 365:
            self.positive_angle = 5
        self.angle = -(360 - self.positive_angle)
