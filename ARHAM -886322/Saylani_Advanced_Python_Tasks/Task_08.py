import time
from functools import wraps

def ttl_cache(seconds: float):
    def decorator(func):
        cache = {}
        hits = 0
        misses = 0

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal hits, misses
            try:
                key = (args, tuple(sorted(kwargs.items())))
            except TypeError:
                return func(*args, **kwargs)

            now = time.monotonic()
            if key in cache:
                result, timestamp = cache[key]
                if now - timestamp < seconds:
                    hits += 1
                    return result

            misses += 1
            result = func(*args, **kwargs)
            cache[key] = (result, now)
            return result

        wrapper.hits = lambda: hits
        wrapper.misses = lambda: misses
        wrapper.clear = cache.clear
        return wrapper
    return decorator

if __name__ == "__main__":
    @ttl_cache(seconds=2)
    def add(x, y):
        return x + y

    print(add(x=2, y=3))
    print(add(y=3, x=2))  
    print(f"Hits: {add.hits()}, Misses: {add.misses()}")