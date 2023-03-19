import time

class TimerService:
    def __init__(self):
        self._start_time = time.time()
        self.stopped = False
    
    def _stop(self):
        self.timedelta = round((time.time() - self._start_time), 3)
        self.stopped = True

    def __repr__(self):
        self._stop()
        return f"{self.timedelta} с"
