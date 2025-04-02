import time
from functools import wraps

class CircuitBreaker:
    def __init__(self, max_failures = 3, reset_timeout = 60) -> None:
        self.max_failures = max_failures
        self.reset_timeouts = reset_timeout
        self.failures = 0
        self.last_failures = 0
        self.state = "closed" # "open", "half-open"

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self.state == "open":
                if time.time() - self.last_failures > self.reset_timeouts:
                    self.state = "half_open"
                else:
                    raise Exception("Circuit breaker is open")
            try:
                result  = func(*args, **kwargs)
                if self.state == "half-open":
                    self.state = "closed"
                    self.failures = 0
                return  result
            except Exception as e:
                self.failures =+ 1
                self.last_failures = time.time()
                if self.failures >= self.max_failures:
                    self.state = "open"
                raise
        return wrapper

#1.Closed State: Normal operation where requests flow to the service
#2.Open State: When failures exceed a threshold, the circuit "trips" and stops sending requests
#3.Half-Open State: After a timeout, limited requests are allowed to test if the service has recovered