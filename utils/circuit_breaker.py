import time
from functools import wraps


class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 3,
        recovery_timeout: int = 30,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout

        self.failure_count = 0
        self.last_failure_time = None
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def call(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            # -----------------
            # OPEN STATE
            # -----------------
            if self.state == "OPEN":
                if (
                    time.time() - self.last_failure_time
                    > self.recovery_timeout
                ):
                    self.state = "HALF_OPEN"
                else:
                    raise Exception(
                        "Circuit breaker OPEN: Service unavailable"
                    )

            try:
                result = func(*args, **kwargs)

                # Success resets breaker
                self.failure_count = 0
                self.state = "CLOSED"

                return result

            except Exception as e:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.failure_count >= self.failure_threshold:
                    self.state = "OPEN"

                raise e

        return wrapper
