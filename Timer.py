import time


class Timer:
    def reset(self):
        self.start_time = time.time()

    def get_time(self):
        return time.time() - self.start_time
