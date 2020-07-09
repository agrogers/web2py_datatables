import time

class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""

class Timer:
    
    def __init__(self):
        self._start_time = None
        self._state = 'stopped'
        self._TotalTime = 0
        self._ElapsedTime = 0

    def start(self):
        """Start a new timer"""
        self._state = 'running'
        self._start_time = time.perf_counter()

    def pause(self):
        """Pause the timer"""
        self._state = 'paused'
        self._ElapsedTime = time.perf_counter() - self._start_time
        self._TotalTime += self._ElapsedTime
    
    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._state == 'stopped':
            raise TimerError(f"Timer is not running. Use .start() to start it")
        
        if self._state != 'paused':
            self._TotalTime += time.perf_counter() - self._start_time
        self._start_time = None
        self._state = 'stopped'
        print(f"Elapsed time: {self._TotalTime:0.4f} seconds")
        return self._TotalTime

    def getElapsedTime(self):
        return f"{self._TotalTime:0.4f}"

    Time = property(getElapsedTime)


