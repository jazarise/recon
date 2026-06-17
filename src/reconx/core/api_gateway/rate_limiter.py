import time
from collections import defaultdict


class RateLimiter:
    def __init__(self, limit: int = 10, window: int = 60):
        # user -> [(timestamp)]
        self.requests = defaultdict(list)
        self.limit = limit
        self.window = window

    def is_allowed(self, user: str) -> bool:
        current_time = time.time()

        # Filter out old requests outside the window
        self.requests[user] = [
            t for t in self.requests[user] if current_time - t < self.window
        ]

        if len(self.requests[user]) >= self.limit:
            return False

        self.requests[user].append(current_time)
        return True


rate_limiter = RateLimiter(limit=10, window=60)  # 10 requests per minute
